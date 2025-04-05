"""Client for interacting with LLMs."""

import importlib
import json
import logging
from collections.abc import Callable
from typing import Any

from openai import AzureOpenAI
from openai.types.responses import ResponseFunctionToolCall

from booking.ai.tools import get_tool_definition
from booking.repository import AbstractRepository


logger = logging.getLogger("app")


class LLMClient:
    """Client for interacting with LLMs."""

    def __init__(
        self,
        openai_client: AzureOpenAI,
        model: str,
        repository: AbstractRepository,
        tools: list[tuple[str, str]],
    ):
        self.client = openai_client
        self.model = model
        self.repository = repository

        self.tools = self._resolve_tools(tools) if tools else {}

        tools_definition = []
        for tool in self.tools.values():
            tools_definition.append(get_tool_definition(tool))

        self.tools_definition = tools_definition
        self.conversation_id = None

    def chat(self, user_message: str, system_prompt: str = None) -> str:
        """Process a user message and return the LLM response."""
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_message,
            previous_response_id=self.conversation_id,
            tools=self.tools_definition,
        )

        # Process tool calls if any
        tool_messages = []

        for output in response.output:
            if isinstance(output, ResponseFunctionToolCall):
                function_name = output.name
                arguments = json.loads(output.arguments)

                # Process function call
                result = self._process_tool_call(function_name, arguments)

                tool_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": json.dumps(result),
                    }
                )

        # If there were tool calls, send their results back to the LLM
        if tool_messages:
            response = self.client.responses.create(
                model=self.model,
                input=tool_messages,
                previous_response_id=response.id,
            )

        self.conversation_id = response.id

        return response.output_text

    def _resolve_tools(self, tools: list[tuple[str, str]]) -> dict[str, Callable]:
        """Resolve functions from the provided tool definitions.
        This method imports the specified modules and retrieves the specified
        functions and returns a dictionary of function names and their corresponding
        Callable function.

        Args:
            tools (list[tuple[str, str]]): A list of tuples containing the module
                and function names.
            Example: [("module.name", "function_name")]

        Raises:
            ValueError: When the tool definition is not in the expected format.
            ModuleNotFoundError: When the specified module cannot be found.
            AttributeError: When the specified function cannot be found in the module.

        Returns:
            dict[str, Callable]: A dictionary of function names and their corresponding
                Callable function.
        """
        exc_msg = (
            "Tool definition should be an Iterable in the format (module, function)."
        )

        resolved_tools = {}

        if not isinstance(tools, list):
            raise ValueError(exc_msg)

        for tool in tools:
            if not isinstance(tool, tuple) or len(tool) < 2:
                raise ValueError(exc_msg)

            module_name = tool[0]
            function_name = tool[1]

            try:
                tool_module = importlib.import_module(module_name)
            except ModuleNotFoundError as exc:
                logger.error(
                    "Module %s not found. The tool cannot be resolved.", module_name
                )
                raise exc

            try:
                tool_function = getattr(tool_module, function_name)
            except AttributeError as exc:
                logger.error(
                    "Function %s not found in module %s. The tool cannot be resolved.",
                    function_name,
                    module_name,
                )
                raise exc

            resolved_tools[function_name] = tool_function
            logger.debug("Resolved tool %s from module %s", function_name, module_name)

        return resolved_tools

    def _process_tool_call(self, function_name: str, arguments: dict[str, Any]) -> Any:
        """Call the specified tool with the provided arguments and returns its result.

        Args:
            function_name (str): The name of the tool to call.
            arguments (dict[str, Any]): The keyword arguments to pass to the tool.

        Returns:
            Any: The result of the tool call.
        """
        func = self.tools.get(function_name)

        if "repo" in arguments:
            arguments["repo"] = self.repository

        return func(**arguments)

"""Tools for OpenAI API integration."""

import re

from enum import Enum
from typing import Callable, Any, Iterable


class ToolDataType(str, Enum):
    """Enum for tool data types."""

    STRING = "string"
    INT = "integer"
    FLOAT = "number"
    BOOL = "boolean"


def get_doctring_arguments(func: Callable) -> dict[str, str]:
    """Extract the arguments and their descriptions from a function's docstring.

    Args:
        func (Callable): The function to extract docstring arguments from.

    Returns:
        dict[str, str]: A dictionary mapping argument names to their descriptions in
            the format `{"arg_name": "description"}`.
    """
    docstring = func.__doc__

    if not docstring:
        raise ValueError("The Function does not have a docstring.")

    docstring_sections = {
        "Args:",
        "Returns:",
        "Yields:",
        "Raises:",
        "Note:",
        "Examples:",
    }

    args_docstring = {}
    current_section = None

    for line in docstring.split("\n"):
        current_line = line.strip()

        # Capture current section.
        if current_line in docstring_sections:
            current_section = current_line
            continue

        if current_line and current_section == "Args:":
            arg_name = ""
            arg_description = ""

            pos = current_line.find(":")
            if pos != -1:
                # Remove the type hint, if any.
                arg_name = re.sub(r"\(.*\)", "", current_line[:pos]).strip()
                arg_description = current_line[pos + 1 :].strip()

            if arg_name:
                args_docstring[arg_name] = arg_description

    return args_docstring


def get_tool_definition(func: Callable) -> dict[str, Any]:
    """Get an OpenAI tool definition for a given function.

    Args:
        func (Callable): The function to convert into a tool definition.

    Returns:
        dict[str, Any]: A dictionary representing the tool definition.
    """
    parameters = {"type": "object", "properties": {}, "required": []}

    args_annotations = func.__annotations__
    args_doctring = get_doctring_arguments(func)
    func_docstring = func.__doc__ if func.__doc__ else ""

    for arg_name, arg_type in args_annotations.items():
        if arg_name in ["return"]:
            continue

        parent_type = ""
        python_data_type = "str"

        if isinstance(arg_type, Iterable):
            parent_type = "array"

            if hasattr(arg_type, "__args__") and len(arg_type.__args__) > 0:
                python_data_type = arg_type.__args__[0].__name__
        elif hasattr(arg_type, "__name__"):
            python_data_type = arg_type.__name__

        try:
            json_data_type = ToolDataType[python_data_type.upper()].value
        except (AttributeError, KeyError):
            json_data_type = ToolDataType.STRING.value

        parameters["properties"][arg_name] = {
            "type": "array" if parent_type else json_data_type,
            "description": args_doctring.get(arg_name, ""),
        }
        if parent_type:
            parameters["properties"][arg_name]["items"] = {"type": json_data_type}

        parameters["additionalProperties"] = False
        parameters["required"].append(arg_name)

    return {
        "type": "function",
        "name": func.__name__,
        "description": func_docstring.split("\n\n", maxsplit=1)[0],
        "parameters": parameters,
        "strict": True,
    }

"""Tests for the ai.client module."""

import pytest

from booking.ai.client import LLMClient


def tool_function() -> None:
    """This is a test function."""
    return True


def tool_function_with_args(arg1: str, arg2: int) -> str:
    """This is a test function with arguments.

    Args:
        arg1 (str): The first argument.
        arg2 (int): The second argument.

    Returns:
        str: The result of the function.
    """
    return f"arg1: {arg1}, arg2: {arg2}"


def tool_function_secret(key: str, repo: str) -> str:
    """Return a secret code based on the key.

    Args:
        key (str): The key to use for generating the secret code.
        repo (Any): A repository. Pass None as a default.

    Returns:
        str: The secret code.
    """
    return key[::-1]


@pytest.mark.parametrize(
    "test_tools, expected",
    [
        (
            [
                ("tests.ai.test_client", "tool_function"),
                ("tests.ai.test_client", "tool_function_with_args"),
            ],
            {
                "tool_function": tool_function,
                "tool_function_with_args": tool_function_with_args,
            },
        ),
        (None, {}),
        ([], {}),
    ],
)
def test_client_resolve_tools_correctly(test_tools: list, expected: dict):
    """Test the LLMClient resolves tools correctly."""
    llm_client = LLMClient(None, None, None, test_tools)

    assert llm_client.tools == expected


@pytest.mark.parametrize(
    "test_tools",
    [("some_tool"), "Module", ["module", "function"]],
)
def test_client_resolve_tools_fails_with_invalid_inputs(test_tools):
    """Test the LLMClient fails with invalid inputs."""
    with pytest.raises(ValueError):
        _ = LLMClient(None, None, None, test_tools)


def test_client_resolve_tools_fails_with_invalid_modules():
    """Test the LLMClient fails with invalid modules."""
    test_tools = [("does.not.exist", "tool_function")]

    with pytest.raises(ModuleNotFoundError):
        _ = LLMClient(None, None, None, test_tools)


def test_client_resolve_tools_fails_with_invalid_function():
    """Test the LLMClient fails with invalid modules."""
    test_tools = [("booking", "tool_function_not_exist_23")]

    with pytest.raises(AttributeError):
        _ = LLMClient(None, None, None, test_tools)


@pytest.mark.integration
def test_client_can_use_tools(openai_client):
    """Test that the LLM client can use a provided tool."""
    tools = [("tests.ai.test_client", "tool_function_secret")]
    llm_client = LLMClient(openai_client, "gpt-4o-mini", None, tools)

    test_key = "Snowdon is Yr Wyddfa in Welsh"
    expected = test_key[::-1]

    response = llm_client.chat(
        f"What is the secret code for the key `{test_key}`?",
        system_prompt="You can only answer with a function call.",
    )

    assert expected in response

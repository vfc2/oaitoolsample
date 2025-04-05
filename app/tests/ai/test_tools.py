"""Tests for the ai.tools module."""

import pytest

from booking.ai.tools import get_doctring_arguments, get_tool_definition

# pylint: disable=unused-argument


@pytest.mark.parametrize(
    "test_doctring, expected",
    [
        (
            """Test function.

        Args:
            arg1: Description for arg1.
            arg2: Description for arg2.

        Returns:
            None
        """,
            {"arg1": "Description for arg1.", "arg2": "Description for arg2."},
        ),
        (
            """Test function.

        Args:
            arg1 (str): Description for arg1.
            arg2 (int): Description for arg2.
            arg3 (list[str]): No description.
            arg4 (dict[str, float]):

        Returns:
            None
        """,
            {
                "arg1": "Description for arg1.",
                "arg2": "Description for arg2.",
                "arg3": "No description.",
                "arg4": "",
            },
        ),
        (
            """Test function.

        Returns:
            str: A string.
        """,
            {},
        ),
    ],
)
def test_docstring_mapping_is_correct(
    test_doctring: str, expected: dict[str, str]
) -> None:
    """Test that a correct doctring mapping is returned."""

    def test_func():
        "return"

    test_func.__doc__ = test_doctring

    test_value = get_doctring_arguments(test_func)

    assert test_value == expected


@pytest.mark.parametrize("test_doctring", ["", None])
def test_doctring_mapping_raises_exception_when_empty_or_none(
    test_doctring: str | None,
) -> None:
    """Test that a ValueError is raised when the docstring is None."""

    def test_func():
        "return"

    test_func.__doc__ = test_doctring

    with pytest.raises(ValueError):
        get_doctring_arguments(test_func)


def test_tool_definition_is_correct():
    """Test that the get_tool_definition."""

    def test_func(arg1: list[str], arg2: int, arg3: bool) -> None:
        """Test function.

        Args:
            arg1: Description for arg1.
            arg2: Description for arg2.
            arg3: Description for arg3.

        Returns:
            None
        """

    expected = {
        "type": "function",
        "name": "test_func",
        "description": "Test function.",
        "parameters": {
            "type": "object",
            "properties": {
                "arg1": {
                    "type": "array",
                    "description": "Description for arg1.",
                    "items": {"type": "string"},
                },
                "arg2": {
                    "type": "integer",
                    "description": "Description for arg2.",
                },
                "arg3": {
                    "type": "boolean",
                    "description": "Description for arg3.",
                },
            },
            "required": ["arg1", "arg2", "arg3"],
            "additionalProperties": False,
        },
        "strict": True,
    }

    test_value = get_tool_definition(test_func)

    assert test_value == expected

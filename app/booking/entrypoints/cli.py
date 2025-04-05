"""Command Line Interface (CLI) for the Booking Assistant application."""

import logging
import sys
import os

from booking.ai.client import LLMClient
from booking.config import get_openai_client, get_database_connection
from booking.repository import SqlRepository


# Register all service functions as tools
TOOLS = [
    ("booking.services", "check_availability"),
]


def get_logger() -> logging.Logger:
    """
    Create a logger for the application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("app")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger


def main() -> None:
    """Main function to execute the CLI application."""
    logger = get_logger()
    logger.debug("Starting the booking application...")

    # Load system prompt
    prompt_path = os.path.join(
        os.path.dirname(__file__), "../../assets/prompts/booking.system.md"
    )
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    # Initialize dependencies
    openai_client = get_openai_client()
    db_connection = get_database_connection()
    repo = SqlRepository(db_connection)

    # Create LLM client
    llm_client = LLMClient(openai_client, "gpt-4o-mini", repo, TOOLS)

    # Interactive mode
    print("Booking Assistant (type 'exit' to quit)")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ("exit", "quit"):
            break

        response = llm_client.chat(user_input, system_prompt)
        print(f"\nAssistant: {response}")
    # Is the room available on 16/10/2025?
    # Is the room available on 2023-10-05?


if __name__ == "__main__":
    main()

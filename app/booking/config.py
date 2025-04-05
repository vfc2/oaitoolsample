"""Config file for the booking app."""

import os
import struct

import pyodbc
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

# This connection option is defined by microsoft in msodbcsql.h
SQL_COPT_SS_ACCESS_TOKEN = 1256
OPENAI_API_VERSION = "2025-03-01-preview"


def get_database_connection() -> pyodbc.Connection:
    """Get a connection to the SQL database using Azure AD authentication.

    Returns:
        pyodbc.Connection: A connection to the SQL database.

    Raises:
        ValueError: If the connection string is not set in the environment
            variable AZURE_SQL_CONNECTIONSTRING.
    """
    connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
    if not connection_string:
        raise ValueError(
            "The AZURE_SQL_CONNECTIONSTRING environment variable is not set."
        )

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token(
        "https://database.windows.net/.default"
    ).token.encode("UTF-16-LE")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

    connection = pyodbc.connect(
        connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct}
    )

    return connection


def get_openai_client() -> AzureOpenAI:
    """Get an Azure OpenAI client.

    Returns:
        AzureOpenAI: An Azure OpenAI client.
    """
    endpoint = os.getenv("OPENAI_ENDPOINT")
    if not endpoint:
        raise ValueError("The OPENAI_ENDPOINT environment variable is not set.")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    openai_client = AzureOpenAI(
        api_version=OPENAI_API_VERSION,
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
    )

    return openai_client

from pathlib import Path
from dotenv import load_dotenv

import azure.functions as func
import os
import logging

from routes.health import health
from routes.auth_config import check_auth, assistant_type
from routes.history import (
    history_list,
    history_read,
    history_update,
    history_rename,
    history_delete,
    history_delete_all,
    frontend_settings_get,
)
from routes.conversation import conversation_custom, conversation_history
from routes.speech_token import speech_token

# from autogen_agentchat.agents import AssistantAgent
# from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_agentchat.conditions import MaxMessageTermination
# from autogen_agentchat.messages import TextMessage
from services.models import create_model_factory

# Load .env from workspace root (two levels up)
env_path = Path(__file__).parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# initialize model factory
model_factory = create_model_factory()
# default_client is created per-request to avoid missing credential errors during startup

# Configure logging for Azure Functions (uses the standard logging module)
logger = logging.getLogger("azure.functions")
logger.setLevel(logging.INFO)

# Log model factory info (but not API keys or secrets)
try:
    model_info = getattr(model_factory, "info", None)
    if callable(model_info):
        logger.info(f"Model factory info: {model_info()}")
    else:
        logger.info(f"Model factory: {model_factory}")
except Exception as e:
    logger.warning(f"Could not log model factory info: {e}")


# Determine if Azure auth is enforced (via AZURE_AUTH_ENABLED); default false for local dev
AUTH_ENABLED = os.getenv("AZURE_AUTH_ENABLED", "false").lower() in ("1", "true")
# Set the auth level for all routes: Function key required if AUTH_ENABLED, else anonymous
AUTH_LEVEL = func.AuthLevel.FUNCTION if AUTH_ENABLED else func.AuthLevel.ANONYMOUS

# create the FunctionApp
app = func.FunctionApp()


# Register routes
@app.route(route="health", methods=["GET"], auth_level=AUTH_LEVEL)
def health_route(req: func.HttpRequest) -> func.HttpResponse:
    return health(req)


@app.route(route="checkauth", methods=["GET"], auth_level=AUTH_LEVEL)
def check_auth_route(req: func.HttpRequest) -> func.HttpResponse:
    return check_auth(req)


# stub out history/frontend_settings
@app.route(route="history/frontend_settings", methods=["GET"], auth_level=AUTH_LEVEL)
def frontend_settings_get_route(req: func.HttpRequest) -> func.HttpResponse:
    return frontend_settings_get(req)


@app.route(route="assistanttype", methods=["GET"], auth_level=AUTH_LEVEL)
def assistant_type_route(req: func.HttpRequest) -> func.HttpResponse:
    return assistant_type(req)


@app.route(route="history/list", methods=["GET"], auth_level=AUTH_LEVEL)
async def history_list_route(req: func.HttpRequest) -> func.HttpResponse:
    return await history_list(req)


@app.route(route="history/read", methods=["POST"], auth_level=AUTH_LEVEL)
async def history_read_route(req: func.HttpRequest) -> func.HttpResponse:
    return await history_read(req)


@app.route(route="history/update", methods=["POST"], auth_level=AUTH_LEVEL)
def history_update_route(req: func.HttpRequest) -> func.HttpResponse:
    return history_update(req)


@app.route(route="history/rename", methods=["POST"], auth_level=AUTH_LEVEL)
def history_rename_route(req: func.HttpRequest) -> func.HttpResponse:
    return history_rename(req)


@app.route(route="history/delete", methods=["DELETE"], auth_level=AUTH_LEVEL)
def history_delete_route(req: func.HttpRequest) -> func.HttpResponse:
    return history_delete(req)


@app.route(route="history/delete_all", methods=["DELETE"], auth_level=AUTH_LEVEL)
def history_delete_all_route(req: func.HttpRequest) -> func.HttpResponse:
    return history_delete_all(req)


@app.route(route="conversation/custom", methods=["POST", "GET"], auth_level=AUTH_LEVEL)
async def conversation_custom_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        return await conversation_custom(req)
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)


@app.route(route="conversation/history", methods=["GET", "POST"], auth_level=AUTH_LEVEL)
async def conversation_history_route(req: func.HttpRequest) -> func.HttpResponse:
    return await conversation_history(req)


@app.route(route="speech/token", methods=["GET"], auth_level=AUTH_LEVEL)
def speech_token_route(req: func.HttpRequest) -> func.HttpResponse:
    return speech_token(req)


# CORS preflight handler for all routes
@app.route(route="{*all}", methods=["OPTIONS"])
def options_handler(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS,DELETE",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
        },
    )

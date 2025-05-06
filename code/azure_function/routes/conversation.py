import json
import azure.functions as func
import logging
import os
from services.db import get_postgres_pool
from services.models import create_model_factory


async def conversation_custom(req: func.HttpRequest) -> func.HttpResponse:
    logger = logging.getLogger("azure.functions")
    logger.info("conversation_custom called")
    # Initialize model client factory and load the 'primary' model
    factory = create_model_factory()
    client = factory.get_client("primary")
    # Try to get some info from the model client for debugging
    try:
        model_debug_info = (
            client.get_model_info()
            if hasattr(client, "get_model_info")
            else str(client)
        )
    except Exception as e:
        model_debug_info = f"Error getting model info: {e}"
    # Build response with model information
    model_info = {
        "model_name": os.getenv("AZURE_OPENAI_MODEL"),
        "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
    }

    logger.info(f"Model Info: {model_info}")
    # Mock choices array format for assistant message
    stubbed = {
        "choices": [
            {
                "messages": [
                    {
                        "role": "assistant",
                        "content": f"Stubbed response! Model debug info: {model_debug_info}",
                        "id": "",
                        "date": "",
                    }
                ]
            }
        ]
    }

    try:
        logger.info("conversation_custom processing request")
        logger.info("conversation_custom success, returning response")
        return func.HttpResponse(
            json.dumps(stubbed),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"},
        )
    except Exception as e:
        import traceback

        logger.error(f"conversation_custom exception: {e}")
        logger.error(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": str(e), "trace": traceback.format_exc()}),
            status_code=500,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"},
        )


async def conversation_history(req: func.HttpRequest) -> func.HttpResponse:
    session_id = req.params.get("sessionId") or (await req.get_json()).get("sessionId")
    pool = get_postgres_pool()
    history = await pool.fetch(
        "SELECT role, content, created_at FROM chat_history WHERE session_id=$1 ORDER BY created_at",
        session_id,
    )
    return func.HttpResponse(
        json.dumps([dict(r) for r in history]),
        status_code=200,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )

import json
import azure.functions as func
from services.db import get_postgres_pool


async def conversation_custom(req: func.HttpRequest) -> func.HttpResponse:
    stubbed = {
        "choices": [
            {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "This is a sample response from the stubbed conversation endpoint.",
                        "id": "",
                        "date": "",
                    }
                ]
            }
        ]
    }
    return func.HttpResponse(
        json.dumps(stubbed),
        status_code=200,
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

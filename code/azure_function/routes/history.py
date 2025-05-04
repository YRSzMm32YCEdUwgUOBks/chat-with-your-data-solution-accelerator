import json
import azure.functions as func
from services.db import get_postgres_pool


async def history_list(req: func.HttpRequest) -> func.HttpResponse:
    pool = get_postgres_pool()
    rows = await pool.fetch(
        "SELECT session_id AS id, MAX(created_at) AS created_at "
        "FROM chat_history GROUP BY session_id ORDER BY created_at DESC"
    )
    conversations = [
        {"id": r["id"], "title": r["id"], "createdAt": r["created_at"], "messages": []}
        for r in rows
    ]
    return func.HttpResponse(
        json.dumps(conversations), status_code=200, mimetype="application/json"
    )


async def history_read(req: func.HttpRequest) -> func.HttpResponse:
    body = await req.get_json()
    session_id = body.get("conversation_id")
    pool = get_postgres_pool()
    history = await pool.fetch(
        "SELECT role, content, created_at FROM chat_history WHERE session_id=$1 ORDER BY created_at",
        session_id,
    )
    return func.HttpResponse(
        json.dumps([dict(r) for r in history]),
        status_code=200,
        mimetype="application/json",
    )


def history_update(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(status_code=200)


def history_rename(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(status_code=200)


def history_delete(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(status_code=200)


def history_delete_all(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(status_code=200)


def frontend_settings_get(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"DummyAttrib": "Dummy Value"}),
        status_code=200,
        mimetype="application/json",
    )

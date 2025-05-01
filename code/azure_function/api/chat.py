# api/chat.py   (renamed from query_rag.py to reflect its true intent)
import json
import asyncio
import azure.functions as func
from orchestration.chat_handler import run_chat


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # TODO: validate Content-Type header (expect application/json), return 415 if not
    # TODO: enforce max JSON payload size to avoid large requests
    try:
        payload = await req.get_json()
    except Exception as e:  # noqa: F841
        # logging.error(f"Exception: {e}")  # Uncomment for debugging
        return {"error": "Internal server error"}, 500
    user_message = payload.get("message", "Hello?")
    # TODO: handle missing message key or invalid types

    loop = asyncio.get_running_loop()
    # TODO: consider offloading to thread pool if run_chat is CPU-bound
    reply = await loop.run_in_executor(None, run_chat, user_message)

    # TODO: sanitize and validate reply content

    return func.HttpResponse(
        json.dumps({"response": reply}), headers={"Content-Type": "application/json"}
    )

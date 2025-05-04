import json
import azure.functions as func


def check_auth(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"is_auth_enforced": False}),
        status_code=200,
        mimetype="application/json",
    )


def assistant_type(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"assistantType": "simple"}),
        status_code=200,
        mimetype="application/json",
    )

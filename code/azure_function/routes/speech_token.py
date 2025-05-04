import azure.functions as func


def speech_token(req: func.HttpRequest) -> func.HttpResponse:
    # TODO: generate & return Azure Speech token + region
    return func.HttpResponse(
        status_code=501, headers={"Access-Control-Allow-Origin": "*"}
    )

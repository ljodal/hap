from .request import Request
from .response import BadRequest, JSONResponse, Response


async def index(_: Request) -> JSONResponse:
    return JSONResponse(data={"foo": "bar"})


async def accessories(_: Request) -> Response:
    return JSONResponse(data={"accessories": []})


async def characteristics(request: Request) -> Response:
    if "id" not in request.query:
        return BadRequest(b'The "id" query parameter must be specified')

    ids = ",".split(",".join(request.query["ids"]))
    if not ids:
        return JSONResponse(data=[])

    raise NotImplementedError

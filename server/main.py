import asyncio
from os import listdir
from os.path import isfile, join
from typing import AsyncGenerator

from quart import Quart, render_template, request, send_from_directory, websocket


class Broker:
    def __init__(self) -> None:
        self.connections = set()

    async def publish(self, message: str) -> None:
        for connection in self.connections:
            await connection.put(message)

    async def subscribe(self) -> AsyncGenerator[str, None]:
        connection = asyncio.Queue()
        self.connections.add(connection)
        try:
            while True:
                yield await connection.get()
        finally:
            self.connections.remove(connection)


app = Quart(
    __name__,
    template_folder="public",
    static_folder="public",
    static_url_path="/static",
)

broker = Broker()


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/pp")
async def powerpoint_files():
    files = [f for f in listdir("powerpoint") if isfile(join("powerpoint", f))]
    return {"files": files}


@app.route("/pp/<path:file>")
async def powerpoint_file(file):
    return await send_from_directory("powerpoint", file)


@app.route("/pp/upload", methods=["POST"])
async def powerpoint_upload():
    file = (await request.files).get("file")
    if file is None:
        return ""
    await file.save(join("powerpoint", file.filename))
    return ""


async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)


@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task

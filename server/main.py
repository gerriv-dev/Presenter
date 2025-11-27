from os import listdir
from os.path import isfile, join

from quart import Quart, render_template, request, send_from_directory, websocket

app = Quart(
    __name__,
    template_folder="public",
    static_folder="public",
    static_url_path="/static",
)

presenter = None
controller = None


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


@app.websocket("/ws/presenter")
async def presenter_ws():
    global presenter, controller
    presenter = websocket
    try:
        while True:
            message = await websocket.receive()
            if controller is not None:
                controller.send(message)
    finally:
        presenter = None


@app.websocket("/ws/controller")
async def ws():
    global presenter, controller
    controller = websocket
    try:
        while True:
            message = await websocket.receive()
            if presenter is not None:
                presenter.send(message)
    finally:
        controller = None

from quart import Quart, render_template

app = Quart(
    __name__,
    template_folder="public",
    static_folder="public",
    static_url_path="/static",
)


@app.route("/")
async def index():
    return await render_template("index.html")

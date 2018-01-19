from server import app


@app.route("/platform")
def platform():
    return "Platform"

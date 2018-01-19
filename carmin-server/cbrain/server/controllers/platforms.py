from server import app


@app.route("/platforms")
def platforms():
    return "Hello World Platforms"

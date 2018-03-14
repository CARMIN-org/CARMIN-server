from server.server_helper import create_app, declare_api

app = create_app()


def main():
    declare_api(app)
    app.run(host='0.0.0.0', port=int(8080))

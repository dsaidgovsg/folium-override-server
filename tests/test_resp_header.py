from flask import Blueprint


def test_build_proxy(app):
    api_blueprint = Blueprint('service_name', __name__)

    @api_blueprint.route("/")
    def generate():
        return "pong"

    app.register_blueprint(api_blueprint, url_prefix='/prefix')

    client = app.test_client()
    resp = client.get('/prefix/')

    assert resp.status_code == 200
    assert resp.data == b"pong"
    assert resp.headers.get("X-Frame-Options") == "DENY"

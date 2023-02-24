import gc
import re
import time
import uuid
import warnings
import weakref
from datetime import datetime
from datetime import timezone
from platform import python_implementation
from threading import Thread

import pytest
import werkzeug.serving
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import NotFound
from werkzeug.http import parse_date
from werkzeug.routing import BuildError
from werkzeug.routing import RequestRedirect

import flask


require_cpython_gc = pytest.mark.skipif(
    python_implementation() != "CPython",
    reason="Requires CPython GC behavior",
)


def test_options_work(app, client):
    @app.route("/", methods=["GET", "POST"])
    def index():
        return "Hello World"

    rv = client.open("/", method="OPTIONS")
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS", "POST"]
    assert rv.data == b""


def test_options_on_multiple_rules(app, client):
    @app.route("/", methods=["GET", "POST"])
    def index():
        return "Hello World"

    @app.route("/", methods=["PUT"])
    def index_put():
        return "Aha!"

    rv = client.open("/", method="OPTIONS")
    assert sorted(rv.allow) == ["GET", "HEAD", "OPTIONS", "POST", "PUT"]


@pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch"])
def test_method_route(app, client, method):
    method_route = getattr(app, method)
    client_method = getattr(client, method)

    @method_route("/")
    def hello():
        return "Hello"

    assert client_method("/").data == b"Hello"


def test_method_route_no_methods(app):
    with pytest.raises(TypeError):
        app.get("/", methods=["GET", "POST"])


def test_provide_automatic_options_attr():
    app = flask.Flask(__name__)

    def index():
        return "Hello World!"

    index.provide_automatic_options = False
    app.route("/")(index)
    rv = app.test_client().open("/", method="OPTIONS")
    assert rv.status_code == 405

    app = flask.Flask(__name__)

    def index2():
        return "Hello World!"

    index2.provide_automatic_options = True
    app.route("/", methods=["OPTIONS"])(index2)
    rv = app.test_client().open("/", method="OPTIONS")
    assert sorted(rv.allow) == ["OPTIONS"]


def test_provide_automatic_options_kwarg(app, client):
    def index():
        return flask.request.method

    def more():
        return flask.request.method

    app.add_url_rule("/", view_func=index, provide_automatic_options=False)
    app.add_url_rule(
        "/more",
        view_func=more,
        methods=["GET", "POST"],
        provide_automatic_options=False,
    )
    assert client.get("/").data == b"GET"

    rv = client.post("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD"]

    rv = client.open("/", method="OPTIONS")
    assert rv.status_code == 405

    rv = client.head("/")
    assert rv.status_code == 200
    assert not rv.data  # head truncates
    assert client.post("/more").data == b"POST"
    assert client.get("/more").data == b"GET"

    rv = client.delete("/more")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD", "POST"]

    rv = client.open("/more", method="OPTIONS")
    assert rv.status_code == 405
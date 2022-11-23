from flask import Flask, Response, session, redirect, request
from urllib.parse import unquote
from werkzeug.datastructures import Headers
from requests import get, post

from logging import getLogger, ERROR
getLogger("werkzeug").setLevel(ERROR)

app = Flask("Cupcake")
app.secret_key = "super secret key"

@app.route("/cupcake_init/<path:variable>")
def init(variable):
	variable = unquote(variable)
	if not variable.endswith("/"): variable+="/"
	session["domain"] = variable
	return redirect("https://cupcake.ninjadev64.repl.co/", code=302)

@app.route("/<path:variable>", methods = ["GET", "POST"])
def proxy(variable):
	if session.get("domain") is None: return "Please initialise Cupcake first!"
	if request.method == "GET":
		response = get("https://" + session.get("domain") + variable)
	elif request.method == "POST":
		response = post("https://" + session.get("domain") + variable, json = request.form)
	headers = Headers()
	headers.add("Content-Type", response.headers.get("Content-Type") or "text/html")
	headers.add("Via", "HTTP/1.1 Cupcake")
	return Response(response.content, headers=headers)

@app.route("/")
def root(): return proxy("")

app.run("0.0.0.0", "8080")
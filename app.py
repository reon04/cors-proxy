import os
import ipaddress
import socket
from urllib.parse import urlparse, unquote

import requests
from flask import Flask, Response, request

app = Flask(__name__)

BLOCKED_NETWORKS = [
  ipaddress.ip_network("127.0.0.0/8"),
  ipaddress.ip_network("10.0.0.0/8"),
  ipaddress.ip_network("172.16.0.0/12"),
  ipaddress.ip_network("192.168.0.0/16"),
  ipaddress.ip_network("169.254.0.0/16"),
  ipaddress.ip_network("0.0.0.0/8"),
  ipaddress.ip_network("::1/128"),
  ipaddress.ip_network("fc00::/7"),
  ipaddress.ip_network("fe80::/10"),
]

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]


def is_allowed_origin() -> bool:
  origin = request.headers.get("Origin")

  if not origin:
    return False
  
  if not ALLOWED_ORIGINS:
    return True

  return origin in ALLOWED_ORIGINS


def is_blocked_host(hostname: str) -> bool:
  try:
    infos = socket.getaddrinfo(hostname, None)

    for info in infos:
      ip = ipaddress.ip_address(info[4][0])

      for network in BLOCKED_NETWORKS:
        if ip in network:
          return True

    return False

  except Exception:
    return True


def is_allowed_url(url: str) -> bool:
  parsed = urlparse(url)

  if parsed.scheme not in ("http", "https"):
    return False

  if not parsed.hostname:
    return False

  if is_blocked_host(parsed.hostname):
    return False

  return True


HELP_TEXT = f"""Simple CORS Proxy

Usage:
  /        Shows help
  /<url>   Create a request to <url> (must include scheme)

Features:
  - Adds Access-Control-Allow-Origin: *
  - Supports redirects
  - Strips cookies from request
  - Blocks local/private network targets
  - Supports GET, POST, PUT, PATCH and DELETE

Source code:
  https://github.com/reon04/cors-poxy
"""


@app.route("/", methods=["GET"])
def index():
    return Response(HELP_TEXT, mimetype="text/plain")


@app.route("/<path:target>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
def proxy(target):
  if not is_allowed_origin():
    return "Missing or blocked Origin", 403
  
  if request.method == "OPTIONS":
    response = Response(status=204)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

  target = unquote(target)

  if not is_allowed_url(target):
    return "Blocked or invalid URL", 403

  try:
    headers = {
      key: value
      for key, value in request.headers
      if key.lower() != "host"
    }

    session = requests.Session()

    resp = session.request(
      method=request.method,
      url=target,
      headers=headers,
      data=request.get_data(),
      #cookies=request.cookies, # disable cookies
      allow_redirects=True,
      stream=True,
      timeout=15
    )

    for redirect_response in resp.history + [resp]:
      if not is_allowed_url(redirect_response.url):
        return "Blocked redirect target", 403

    excluded_headers = {
      "content-encoding",
      "transfer-encoding",
      "connection",
      "set-cookie"
    }

    response_headers = [
      (name, value)
      for name, value in resp.headers.items()
      if name.lower() not in excluded_headers
    ]

    response = Response(
      response=resp.content,
      status=resp.status_code,
      headers=response_headers
    )

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"

    return response

  except Exception as e:
    return f"Proxy error: {e}", 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="80")
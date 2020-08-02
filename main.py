import uuid
from datetime import datetime
from prometheus_client import start_http_server, Gauge
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests


class Target:
    def __init__(self, url, frequency=60, **params):
        self.id = str(uuid.uuid1())
        self.url = url
        self.frequency = frequency
        self.params = params
        db.add(self)

    def delete(self, uuid):
        db.delete(self)

    def update(self, **params):
        db.update(self, params)


class Check:
    def execute(self, target):
        r = requests.get(target.url, target.params)
        timestamp = datetime.now()
        if r.status_code != target.params["acceptable_codes"] and target.params["payload"] not in r.text:
            Incident(target, timestamp)
        self._store_(timestamp, target, r.status_code, r.text, r.headers)

    def _store_(self, timestamp, target, status, payload, headers):
        pass


class Incident:
    def __init__(self, target, timestamp):
        self.target = target
        self.timestamp = timestamp
        self._store_()

    def _store_(self):
        pass

    def close(self, target):
        pass


class DB:
    def add(self, target):
        g = Gauge(target.id, labelnames=(target.id, target.url))

    def init(self):
        pass


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(self.path.encode())


if __name__ == '__main__':
    # init()
    db = DB()
    # Start up the server to expose the metrics.
    start_http_server(8100)

    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

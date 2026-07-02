import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

COURSE_SERVICE = "http://127.0.0.1:5001"
STUDENT_SERVICE = "http://127.0.0.1:5002"

@app.route("/api/courses/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_course_traffic(path):
    return forward_request(f"{COURSE_SERVICE}/api/courses/{path}")

@app.route("/api/students/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_student_traffic(path):
    return forward_request(f"{STUDENT_SERVICE}/api/students/{path}")

def forward_request(url):
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    try:
        resp = requests.request(
            method=request.method, url=url, headers=headers, 
            data=request.get_data(), params=request.args, stream=True, timeout=5.0
        )
        return (resp.content, resp.status_code, resp.headers.items())
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Bad Gateway: Target microservice down"}), 502

if __name__ == "__main__":
    app.run(port=5000, debug=True)
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
import random
import os

app = Flask(__name__)

logs = []

@app.route("/")
def dashboard():

    parsed_alerts = []

    for log in logs:
        severity = "LOW"

        if "FAILED" in log.upper() or "DENIED" in log.upper():
            severity = "HIGH"
        elif "ERROR" in log.upper():
            severity = "MEDIUM"

        parsed_alerts.append({
            "ip": "dynamic",
            "event": log,
            "severity": severity
        })

    return render_template("dashboard.html", alerts=parsed_alerts)

@app.route("/help")
def help_page():
    return render_template("help.html")

@app.route("/generate-demo")
def generate_demo():
    logs.clear()
    sample_events = [
        "Failed login from 192.168.1.5",
        "Accepted login for admin",
        "ERROR invalid request",
        "DENIED connection attempt",
        "Successful login"
    ]
    

    for i in range(15):
        logs.append(random.choice(sample_events))

    return jsonify({"status":"demo logs added"})

@app.route("/upload", methods=["POST"])
def upload_logs():
    file = request.files.get("logfile")

    if not file:
        return redirect(url_for("dashboard"))

    content = file.read().decode("utf-8", errors="ignore")

    for line in content.splitlines():
        if line.strip():
            logs.append(line)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
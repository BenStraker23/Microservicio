from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return f"Hola desde e microservicio {hostname}!"
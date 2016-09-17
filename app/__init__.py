from flask import Flask
from routes import add_routes

app = Flask(__name__)
add_routes(app)
from app import views

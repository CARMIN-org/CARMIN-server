"""
Launching Flask
"""
import os
from flask import Flask

app = Flask(__name__)

import server.controllers.platform

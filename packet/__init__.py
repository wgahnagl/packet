"""
The application setup and initialization code lives here.
"""

import os
from flask import Flask
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_saml

app = Flask(__name__)

# Load default configuration and any environment variable overrides
app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

# Load file based configuration overrides if present
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

# Initialize the extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

auth = OIDCAuthentication(app, issuer=app.config["OIDC_ISSUER"], client_registration_info={
    "client_id": app.config["OIDC_CLIENT_ID"],
    "client_secret": app.config["OIDC_CLIENT_SECRET"]
})

flask_saml.FlaskSAML(app)

# pylint: disable=wrong-import-position
from . import routes
from . import commands
from . import models

from app.api import api_bp


# register blueprint
def register(app):
    app.register_blueprint(api_bp)

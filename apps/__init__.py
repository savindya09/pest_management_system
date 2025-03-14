from flask import Flask
from importlib import import_module

def register_blueprints(app):
    modules = ['pestmanagement']
    for module_name in modules:
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint)

def create_app(config_class='config.Config'):
    print("📌 Creating Flask app...")  # Debugging print
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    print("📌 Registering blueprints...")  # Debugging print
    register_blueprints(app)
    
    print("✅ App Created Successfully")  # Debugging print
    return app

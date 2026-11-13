from flask import Flask # import Flask

def create_app(): # create application factory - create and configure Flask application 
  app = Flask(__name__) # create Flask instance
  
  from app.routes import inventory_bp
  app.register_blueprint(inventory_bp) # tells Flask to include routes defined in app/routes.py
  
  return app # return the application
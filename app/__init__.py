from flask import Flask # import Flask

def create_app(): # create application factory - create and configure Flask application 
  app = Flask(__name__) # create Flask instance
  
  return app # return the application
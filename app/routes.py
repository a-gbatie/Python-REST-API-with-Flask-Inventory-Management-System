# Blueprint allows organization of Flask routes in a separate file outside of app.py
from flask import Blueprint, jsonify

inventory_bp = Blueprint("inventory", __name__) # create Blueprint named inventory

@inventory_bp.route("/inventory", methods=["GET"]) # registers a route to HTTP GET /inventory
def get_inventory():
  return jsonify([]), 200
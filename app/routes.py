# Blueprint allows organization of Flask routes in a separate file outside of app.py
from flask import Blueprint, jsonify, request
from app.inventory import inventory_items

inventory_bp = Blueprint("inventory", __name__) # create Blueprint named inventory

@inventory_bp.route("/inventory", methods=["GET"]) # registers a route to HTTP GET /inventory
def get_inventory():
  return jsonify(inventory_items), 200

@inventory_bp.route("/inventory", methods=["POST"])
def add_inventory_item():
  data = request.get_json(silent=True)
  
  if not isinstance(data, dict):
    return jsonify({"error": "A JSON object is required."}), 400
  
  name = data.get("name")
  
  if not isinstance(name, str) or not name.strip():
    return jsonify({"error": "Product name must be a non-empty string."}), 400
  
  name = name.strip()
  
  quantity = data.get("quantity")
  
  if type(quantity) is not int or quantity < 0:
    return jsonify({"error": "Quantity must be a non-negative integer."}), 400
  
  price = data.get("price")
  
  if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
    return jsonify({"error": "Price must be a non-negative number."}), 400
  
  new_id = max(
    (item["id"] for item in inventory_items),
    default=0
  ) + 1
  
  new_item = {
    "id": new_id,
    "name": name,
    "quantity": quantity,
    "price": price
  }
  
  inventory_items.append(new_item)
  return jsonify(new_item), 201
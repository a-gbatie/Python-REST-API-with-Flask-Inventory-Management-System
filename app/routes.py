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

@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
  for item in inventory_items:
    if item["id"] == item_id:
      return jsonify(item), 200
    
  return jsonify({"error": "Inventory item not found."}), 404

@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
  item = next(
    (item for item in inventory_items if item["id"] == item_id),
    None
  )
  
  if item is None:
    return jsonify({"error": "Inventory item not found."}), 404
  
  data = request.get_json(silent=True)
  
  if not isinstance(data, dict):
    return jsonify({"error": "A JSON object is required"}), 400
  
  if "name" in data:
    if not isinstance(data["name"], str) or not data["name"].strip():
      return jsonify({"error": "Invalid product name."}), 400
  
  if "quantity" in data:
    if type(data["quantity"]) is not int or data["quantity"] < 0:
      return jsonify({"error": "Invalid quantity."}), 400
    
  if "price" in data:
    if type(data["price"]) not in (int, float) or data["price"] < 0:
      return jsonify({"error": "Invalid price."}), 400
    
  for field in ("name", "quantity", "price"):
    if field in data:
      item[field] = data[field].strip() if field == "name" else data[field]
  
  return jsonify(item), 200

@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
  for item in inventory_items:
    if item["id"] == item_id:
      inventory_items.remove(item)
      return jsonify({"message": "Item successfully deleted."})
  
  return jsonify({"error": "Inventory item not found."}), 404
  
  
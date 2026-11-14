
import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"


def send_request(method, endpoint, data=None):
  try:
    res = requests.request(
      method,
      f"{BASE_URL}{endpoint}",
      params=data if method == "GET" else None,
      json=data if method != "GET" else None,
      timeout=10
    )

    print(f"Status: {res.status_code}")
    print(res.json())

  except requests.RequestException as error:
    print(f"Request failed: {error}")
  except ValueError:
    print("Server returned an invalid JSON response.")


def main():
  parser = argparse.ArgumentParser(
    description="Inventory Management CLI"
  )

  subparsers = parser.add_subparsers(
    dest="command",
    required=True
  )

  # View all inventory items
  subparsers.add_parser("list", help="List inventory items")

  # View one inventory item
  view_parser = subparsers.add_parser("view", help="View an item")
  view_parser.add_argument("id", type=int)

  # Add an inventory item
  add_parser = subparsers.add_parser("add", help="Add an item")
  add_parser.add_argument("name")
  add_parser.add_argument("quantity", type=int)
  add_parser.add_argument("price", type=float)

  # Update an inventory item
  update_parser = subparsers.add_parser("update", help="Update an item")
  update_parser.add_argument("id", type=int)
  update_parser.add_argument("--name")
  update_parser.add_argument("--quantity", type=int)
  update_parser.add_argument("--price", type=float)

  # Delete an inventory item
  delete_parser = subparsers.add_parser("delete", help="Delete an item")
  delete_parser.add_argument("id", type=int)

  # Search OpenFoodFacts by product name
  search_parser = subparsers.add_parser("search", help="Search products")
  search_parser.add_argument("name")

  # Add an item using its barcode
  barcode_parser = subparsers.add_parser(
    "barcode",
    help="Add an item using OpenFoodFacts"
  )
  barcode_parser.add_argument("barcode")
  barcode_parser.add_argument("quantity", type=int)
  barcode_parser.add_argument("price", type=float)

  args = parser.parse_args()

  if args.command == "list":
    send_request("GET", "/inventory")

  elif args.command == "view":
    send_request("GET", f"/inventory/{args.id}")

  elif args.command == "add":
    send_request("POST", "/inventory", {
      "name": args.name,
      "quantity": args.quantity,
      "price": args.price
    })

  elif args.command == "update":
    data = {
      key: value
      for key, value in {
        "name": args.name,
        "quantity": args.quantity,
        "price": args.price
      }.items()
      if value is not None
    }

    send_request("PATCH", f"/inventory/{args.id}", data)

  elif args.command == "delete":
    send_request("DELETE", f"/inventory/{args.id}")

  elif args.command == "search":
    send_request("GET", "/products/search", {"name": args.name})

  elif args.command == "barcode":
    send_request("POST", "/inventory/barcode", {
      "barcode": args.barcode,
      "quantity": args.quantity,
      "price": args.price
    })


if __name__ == "__main__":
  main()


import pytest

from app import create_app
from app.inventory import inventory_items
from unittest.mock import patch


@pytest.fixture # reusable resources for tests
def client():
  app = create_app()
  app.config["TESTING"] = True

  inventory_items.clear()

  with app.test_client() as client:
    yield client

  inventory_items.clear()


def test_get_empty_inventory(client):
  response = client.get("/inventory")

  assert response.status_code == 200
  assert response.get_json() == []


def test_add_inventory_item(client):
  response = client.post("/inventory", json={
    "name": "Milk",
    "quantity": 5,
    "price": 3.99
  })

  assert response.status_code == 201

  data = response.get_json()
  assert data["id"] == 1
  assert data["name"] == "Milk"
  assert data["quantity"] == 5
  assert data["price"] == 3.99


def test_get_inventory_item(client):
  client.post("/inventory", json={
    "name": "Bread",
    "quantity": 3,
    "price": 2.50
  })

  response = client.get("/inventory/1")

  assert response.status_code == 200
  assert response.get_json()["name"] == "Bread"


def test_update_inventory_item(client):
  client.post("/inventory", json={
    "name": "Eggs",
    "quantity": 12,
    "price": 4.99
  })

  response = client.patch("/inventory/1", json={
    "quantity": 24
  })

  assert response.status_code == 200
  assert response.get_json()["quantity"] == 24


def test_delete_inventory_item(client):
  client.post("/inventory", json={
    "name": "Cheese",
    "quantity": 2,
    "price": 6.99
  })

  response = client.delete("/inventory/1")

  assert response.status_code == 200
  assert inventory_items == []


def test_get_missing_item(client):
  response = client.get("/inventory/999")

  assert response.status_code == 404


def test_add_invalid_item(client):
  response = client.post("/inventory", json={
    "name": "",
    "quantity": -1,
    "price": 3.99
  })

  assert response.status_code == 400
  assert inventory_items == []

@patch("app.routes.fetch_product_by_barcode")
def test_barcode_lookup_route(mock_fetch, client):
  mock_fetch.return_value = {
    "barcode": "3017620422003",
    "name": "Nutella",
    "brand": "Ferrero",
    "ingredients": "Sugar, hazelnuts"
  }

  response = client.get("/products/barcode/3017620422003")

  assert response.status_code == 200
  assert response.get_json()["name"] == "Nutella"


@patch("app.routes.search_products_by_name")
def test_product_search_route(mock_search, client):
  mock_search.return_value = [
    {
      "barcode": "123456789",
      "name": "Chocolate",
      "brand": "Test Brand",
      "ingredients": "Cocoa"
    }
  ]

  response = client.get("/products/search?name=Chocolate")

  assert response.status_code == 200
  assert len(response.get_json()) == 1
  mock_search.assert_called_once_with("Chocolate")


@patch("app.routes.fetch_product_by_barcode")
def test_add_inventory_by_barcode(mock_fetch, client):
  mock_fetch.return_value = {
    "barcode": "3017620422003",
    "name": "Nutella",
    "brand": "Ferrero",
    "ingredients": "Sugar, hazelnuts"
  }

  response = client.post("/inventory/barcode", json={
    "barcode": "3017620422003",
    "quantity": 10,
    "price": 5.99
  })

  assert response.status_code == 201

  data = response.get_json()
  assert data["name"] == "Nutella"
  assert data["quantity"] == 10
  assert data["brand"] == "Ferrero"

  assert len(inventory_items) == 1


@patch("app.routes.fetch_product_by_barcode")
def test_add_inventory_by_barcode_not_found(mock_fetch, client):
  mock_fetch.return_value = None

  response = client.post("/inventory/barcode", json={
    "barcode": "0000000000000",
    "quantity": 5,
    "price": 2.99
  })

  assert response.status_code == 404
  assert inventory_items == []

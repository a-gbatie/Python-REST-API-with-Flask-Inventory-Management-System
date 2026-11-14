
import pytest

from app import create_app
from app.inventory import inventory_items


@pytest.fixture
def client():
  app = create_app()
  app.config["TESTING"] = True

  inventory_items.clear()

  with app.test_client() as client:
    yield client

  inventory_items.clear()


def test_inventory_starts_empty(client):
  assert inventory_items == []


def test_multiple_items_have_unique_ids(client):
  first = client.post("/inventory", json={
    "name": "Milk",
    "quantity": 5,
    "price": 3.99
  })

  second = client.post("/inventory", json={
    "name": "Bread",
    "quantity": 2,
    "price": 2.99
  })

  first_id = first.get_json()["id"]
  second_id = second.get_json()["id"]

  assert first_id != second_id
  assert len(inventory_items) == 2


def test_deleting_item_updates_inventory(client):
  client.post("/inventory", json={
    "name": "Eggs",
    "quantity": 12,
    "price": 4.99
  })

  client.delete("/inventory/1")

  assert len(inventory_items) == 0


def test_invalid_quantity_is_rejected(client):
  response = client.post("/inventory", json={
    "name": "Juice",
    "quantity": -5,
    "price": 3.50
  })

  assert response.status_code == 400
  assert inventory_items == []

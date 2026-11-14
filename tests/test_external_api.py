
from unittest.mock import patch, Mock

import requests

from app.external_api import (
  fetch_product_by_barcode,
  search_products_by_name
)


@patch("app.external_api.requests.get")
def test_fetch_product_by_barcode(mock_get):
  mock_response = Mock()
  mock_response.json.return_value = {
    "status": 1,
    "product": {
      "product_name": "Nutella",
      "brands": "Ferrero",
      "ingredients_text": "Sugar, hazelnuts, cocoa"
    }
  }

  mock_get.return_value = mock_response

  product = fetch_product_by_barcode("3017620422003")

  assert product is not None
  assert product["name"] == "Nutella"
  assert product["brand"] == "Ferrero"
  assert product["barcode"] == "3017620422003"


@patch("app.external_api.requests.get")
def test_fetch_missing_product(mock_get):
  mock_response = Mock()
  mock_response.json.return_value = {
    "status": 0,
    "product": {}
  }

  mock_get.return_value = mock_response

  product = fetch_product_by_barcode("0000000000000")

  assert product is None


@patch("app.external_api.requests.get")
def test_search_products_by_name(mock_get):
  mock_response = Mock()
  mock_response.json.return_value = {
    "products": [
      {
        "code": "123456789",
        "product_name": "Chocolate",
        "brands": "Test Brand",
        "ingredients_text": "Cocoa"
      }
    ]
  }

  mock_get.return_value = mock_response

  products = search_products_by_name("Chocolate")

  assert len(products) == 1
  assert products[0]["name"] == "Chocolate"
  assert products[0]["brand"] == "Test Brand"


@patch("app.external_api.requests.get")
def test_external_api_network_error(mock_get):
  mock_get.side_effect = requests.RequestException("Connection failed")

  product = fetch_product_by_barcode("3017620422003")

  assert product is None


@patch("app.external_api.requests.get")
def test_search_network_error(mock_get):
  mock_get.side_effect = requests.RequestException("Connection failed")

  products = search_products_by_name("Nutella")

  assert products == []

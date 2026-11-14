
import sys
from unittest.mock import Mock, patch

from cli.commands import main, send_request


@patch("cli.commands.requests.request")
def test_cli_list(mock_request):
  mock_request.return_value = Mock(
    status_code=200
  )
  mock_request.return_value.json.return_value = []

  with patch.object(sys, "argv", ["cli", "list"]):
    main()

  mock_request.assert_called_once_with(
    "GET",
    "http://127.0.0.1:5000/inventory",
    params=None,
    json=None,
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_add(mock_request):
  mock_request.return_value = Mock(status_code=201)
  mock_request.return_value.json.return_value = {
    "id": 1,
    "name": "Milk",
    "quantity": 5,
    "price": 3.99
  }

  with patch.object(
    sys, "argv", ["cli", "add", "Milk", "5", "3.99"]
  ):
    main()

  mock_request.assert_called_once_with(
    "POST",
    "http://127.0.0.1:5000/inventory",
    params=None,
    json={
      "name": "Milk",
      "quantity": 5,
      "price": 3.99
    },
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_update(mock_request):
  mock_request.return_value = Mock(status_code=200)
  mock_request.return_value.json.return_value = {
    "id": 1,
    "quantity": 8
  }

  with patch.object(
    sys, "argv", ["cli", "update", "1", "--quantity", "8"]
  ):
    main()

  mock_request.assert_called_once_with(
    "PATCH",
    "http://127.0.0.1:5000/inventory/1",
    params=None,
    json={"quantity": 8},
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_delete(mock_request):
  mock_request.return_value = Mock(status_code=200)
  mock_request.return_value.json.return_value = {
    "message": "Inventory item deleted successfully."
  }

  with patch.object(sys, "argv", ["cli", "delete", "1"]):
    main()

  mock_request.assert_called_once_with(
    "DELETE",
    "http://127.0.0.1:5000/inventory/1",
    params=None,
    json=None,
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_search(mock_request):
  mock_request.return_value = Mock(status_code=200)
  mock_request.return_value.json.return_value = []

  with patch.object(
    sys, "argv", ["cli", "search", "Nutella"]
  ):
    main()

  mock_request.assert_called_once_with(
    "GET",
    "http://127.0.0.1:5000/products/search",
    params={"name": "Nutella"},
    json=None,
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_barcode(mock_request):
  mock_request.return_value = Mock(status_code=201)
  mock_request.return_value.json.return_value = {
      "id": 1,
      "name": "Nutella"
  }

  with patch.object(
    sys,
    "argv",
    ["cli", "barcode", "3017620422003", "10", "5.99"]
  ):
    main()

  mock_request.assert_called_once_with(
    "POST",
    "http://127.0.0.1:5000/inventory/barcode",
    params=None,
    json={
      "barcode": "3017620422003",
      "quantity": 10,
      "price": 5.99
    },
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_cli_view(mock_request):
  mock_request.return_value = Mock(status_code=200)
  mock_request.return_value.json.return_value = {
    "id": 1,
    "name": "Milk"
  }

  with patch.object(sys, "argv", ["cli", "view", "1"]):
    main()

  mock_request.assert_called_once_with(
    "GET",
    "http://127.0.0.1:5000/inventory/1",
    params=None,
    json=None,
    timeout=10
  )


@patch("cli.commands.requests.request")
def test_send_request_network_error(mock_request, capsys):
  import requests

  mock_request.side_effect = requests.RequestException(
    "Connection failed"
  )

  send_request("GET", "/inventory")

  captured = capsys.readouterr()

  assert "Request failed" in captured.out

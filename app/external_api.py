import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2"

def fetch_product_by_barcode(barcode):
  url = f"{BASE_URL}/product/{barcode}.json"
  
  try:
    res = requests.get( # sends HTTP GET request to external server
      url,
      timeout=10, # prevents app from waiting indefinitely if API doesn't respond
      headers={"User-Agent": "FlaskInventoryManagement/1.0"} # tells external API which app is making the HTTP request
    )
    res.raise_for_status() # raises an exception if server returns an error
    
    data = res.json()
    
    if data.get("status") != 1:
      return None
    
    product = data.get("product", {})
    
    return {
      "barcode": barcode,
      "name": product.get("product_name", "Unknown"),
      "brand": product.get("brands", "Unknown"),
      "ingredients": product.get("ingredients_text", "")
    }
  
  except (requests.RequestException, ValueError):
    return None
  
def search_products_by_name(name):
  url = f"{BASE_URL}/search"
  
  params = {
    "search_terms": name,
    "fields": "code,product_name,brands,ingredients_text",
    "page_size": 5
  }
  
  try:
    res = requests.get(
      url,
      params=params,
      timeout=10,
      headers={"User-Agent": "FlaskInventoryManagement/1.0"}
    )
    res.raise_for_status()
    
    data = res.json()
    products = []
    
    for product in data.get("products", []):
      products.append({
        "barcode": product.get("code", ""),
        "name": product.get("product_name", "Unknown"),
        "brand": product.get("brands", "Unknown"),
        "ingredients": product.get("ingredients_text", "")
      })
      
    return products
  
  except (requests.RequestException, ValueError):
    return []
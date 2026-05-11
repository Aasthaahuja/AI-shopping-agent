import requests
import os
from dotenv import load_dotenv

load_dotenv()

STORE_URL = os.getenv("SHOPIFY_STORE_URL")
TOKEN = os.getenv("SHOPIFY_STOREFRONT_TOKEN")
API_URL = f"https://{STORE_URL}/api/2024-01/graphql.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Storefront-Access-Token": TOKEN
}

def search_products(query, max_results=5):
    # Fetch all products and filter client-side for better matching
    graphql_query = """
    {
      products(first: 20) {
        edges {
          node {
            id
            title
            description
            priceRange {
              minVariantPrice {
                amount
                currencyCode
              }
            }
            variants(first: 5) {
              edges {
                node {
                  id
                  title
                  availableForSale
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
             tags
            images(first: 1) {
              edges {
                node {
                  url
                }
              }
            }
          }
        }
      }
    }
    """

    try:
        response = requests.post(API_URL, json={"query": graphql_query}, headers=HEADERS)
        data = response.json()
        products = data.get("data", {}).get("products", {}).get("edges", [])
        result = []
        for edge in products:
            node = edge["node"]
            variants = [v["node"] for v in node["variants"]["edges"]]
            images = node.get("images", {}).get("edges", [])
            image_url = images[0]["node"]["url"] if images else ""
            result.append({
                "id": node["id"],
                "title": node["title"],
                "description": node["description"],
                "price": node["priceRange"]["minVariantPrice"]["amount"],
                "currency": node["priceRange"]["minVariantPrice"]["currencyCode"],
                "variants": variants,
                "tags": node["tags"],
                "image": image_url
            })
        return result
    except Exception as e:
        return {"error": str(e)}


def get_all_products():
    return search_products("*", max_results=50)


def create_cart(variant_id):
    graphql_query = """
    mutation {
      cartCreate(input: {
        lines: [{ quantity: 1, merchandiseId: "%s" }]
      }) {
        cart {
          id
          checkoutUrl
        }
        userErrors {
          field
          message
        }
      }
    }
    """ % variant_id

    try:
        response = requests.post(API_URL, json={"query": graphql_query}, headers=HEADERS)
        data = response.json()
        cart = data.get("data", {}).get("cartCreate", {}).get("cart", {})
        errors = data.get("data", {}).get("cartCreate", {}).get("userErrors", [])
        if errors:
            return {"error": errors[0]["message"]}
        return {
            "cart_id": cart.get("id"),
            "checkout_url": cart.get("checkoutUrl")
        }
    except Exception as e:
        return {"error": str(e)}
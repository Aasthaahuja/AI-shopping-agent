from flask import Flask, render_template, request, jsonify
from agent import chat, handle_add_to_cart
from shopify_tools import search_products

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        if any(phrase in user_message.lower() for phrase in ["add to cart", "buy", "purchase", "order"]):
            response = handle_add_to_cart(user_message)
            return jsonify({"response": response, "products": []})

        response = chat(user_message)

        # fetch products to show as cards
        products_raw = search_products(user_message, max_results=4)
        products = []
        if isinstance(products_raw, list):
            for p in products_raw:
                # skip non-fashion items
                if any(skip in p['title'].lower() for skip in ['snowboard', 'gift card', 'ski']):
                    continue
                products.append({
                    "title": p["title"],
                    "price": f"{float(p['price']):.0f}",
                    "image": ""
                })

        return jsonify({"response": response, "products": products})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
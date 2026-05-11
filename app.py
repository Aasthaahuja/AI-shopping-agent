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

        if any(phrase in user_message.lower() for phrase in ["add to cart", "buy", "purchase", "order", "i want"]):
            response = handle_add_to_cart(user_message)
            return jsonify({"response": response, "products": []})
        else:
            response = chat(user_message)
            # Fetch products to show images
            all_products = search_products(user_message, max_results=50)
            products = [p for p in all_products if not any(word in p['title'].lower() for word in ['snowboard', 'ski', 'gift card', 'hydrogen', 'oxygen', 'liquid'])]
            product_cards = [{"title": p["title"], "price": p["price"], "image": p.get("image", "")} for p in products[:4]]
            return jsonify({"response": response, "products": product_cards})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
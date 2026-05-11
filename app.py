from flask import Flask, render_template, request, jsonify
from agent import chat, handle_add_to_cart

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

        # Check if user wants to add to cart
        if any(phrase in user_message.lower() for phrase in ["add to cart", "buy", "purchase", "order"]):
            response = handle_add_to_cart(user_message)
        else:
            response = chat(user_message)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
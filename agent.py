from groq import Groq
import os
from dotenv import load_dotenv
from shopify_tools import search_products, create_cart

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a smart AI shopping assistant for a fashion store called Kasparro Fashion.
You help users find the perfect clothing based on their needs.

You have access to a fashion store with these types of products:
- Men's shirts, jeans, polos, blazers, track pants, cargo shorts
- Women's dresses, leggings, skirts, kurtis, crop tops
- Unisex hoodies, denim jackets, sweaters

Your job is to:
1. Understand what the user actually needs (occasion, budget, style, size)
2. Ask smart follow-up questions if needed (max 1-2 questions)
3. Search and recommend the most relevant products
4. Compare products when asked (price, style, occasion)
5. Explain WHY you recommend each product
6. Help them add to cart when they decide

When you have product data always:
- Mention the product name and price clearly
- Explain why it fits their need
- Handle tradeoffs (e.g. "this is pricier but better for formal occasions")

Always be conversational, helpful and concise.
"""

def format_products_for_ai(products):
    if not products or (isinstance(products, dict) and "error" in products):
        return "No products found."
    formatted = []
    for p in products:
        variants_text = ", ".join([v["title"] for v in p["variants"] if v["availableForSale"]])
        formatted.append(
            f"- {p['title']} | Price: ₹{float(p['price']):.0f} | "
            f"Available sizes: {variants_text or 'Check store'} | "
            f"Description: {p['description'][:100] if p['description'] else 'Fashion item'}"
        )
    return "\n".join(formatted)


def chat(user_message):
    try:
        products = search_products(user_message, max_results=5)
        products_text = format_products_for_ai(products)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""
User message: {user_message}

Available products from store that match:
{products_text}

Respond helpfully. Recommend products with clear reasoning. Be concise and friendly.
"""}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try again."


def handle_add_to_cart(product_title):
    try:
        products = search_products(product_title, max_results=1)
        if not products or isinstance(products, dict):
            return "Sorry, I couldn't find that product. Can you try again?"

        product = products[0]
        available_variants = [v for v in product["variants"] if v["availableForSale"]]

        if not available_variants:
            return "Sorry, this product is currently out of stock."

        variant_id = available_variants[0]["id"]
        cart_result = create_cart(variant_id)

        if "error" in cart_result:
            return f"Sorry, couldn't add to cart: {cart_result['error']}"

        checkout_url = cart_result.get("checkout_url", "")
        return f"Added **{product['title']}** to cart! 🛒\n\n[Click here to checkout]({checkout_url})"

    except Exception as e:
        return f"Error adding to cart: {str(e)}"


if __name__ == "__main__":
    print("AI Shopping Agent started! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue
        response = chat(user_input)
        print(f"\nAgent: {response}\n")
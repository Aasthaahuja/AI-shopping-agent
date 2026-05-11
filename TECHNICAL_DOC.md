# Technical Document — Kasparro Fashion AI Shopping Agent

## Architecture Overview
User (Browser)
↓
index.html (Chat UI)
↓ POST /chat
app.py (Flask Server)
↓
agent.py (LLM Brain)
↓                    ↓
Groq API            shopify_tools.py
(Llama 3.3-70b)     (Shopify Storefront API)
↓
Shopify Dev Store

## Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | HTML/CSS/JS | Lightweight, no framework needed |
| Backend | Python + Flask | Simple REST API, fast setup |
| AI Model | Llama 3.3-70b via Groq | Free, fast, high quality |
| Commerce | Shopify Storefront API (GraphQL) | Real inventory + cart/checkout |
| Config | python-dotenv | Secure API key management |

## File Structure
ai-shopping-agent/
├── .env                  # API keys (not committed to git)
├── agent.py              # LLM logic, conversation history, prompt
├── shopify_tools.py      # Shopify GraphQL queries
├── app.py                # Flask server, routing
├── templates/
│   └── index.html        # Chat UI
├── DECISION_LOG.md
├── PRODUCT_DOC.md
└── TECHNICAL_DOC.md

## Key Components

### agent.py
- Initializes Groq client with Llama 3.3-70b model
- Maintains conversation history across turns
- Fetches products from Shopify and injects them into context
- Filters out demo/non-clothing products
- System prompt engineers the response format

### shopify_tools.py
- Connects to Shopify Storefront API via GraphQL
- `search_products()` — fetches all products with variants
- `create_cart()` — creates a Shopify cart and returns checkout URL

### app.py
- Flask server with two routes:
  - `GET /` — serves the chat UI
  - `POST /chat` — receives user message, returns AI response
- Detects purchase intent and routes to cart handler

### index.html
- Single-page chat interface
- Suggestion buttons for common queries
- Typing indicator while AI responds
- Markdown rendering for bold/italic/links

## API Integrations

### Groq API
- Endpoint: chat completions
- Model: llama-3.3-70b-versatile
- Conversation history passed on every request for context

### Shopify Storefront API
- GraphQL endpoint: `https://{store}.myshopify.com/api/2024-01/graphql.json`
- Auth: Storefront Access Token in header
- Queries: product listing, cart creation

## How the AI Reasoning Works
1. User sends message
2. All clothing products fetched from Shopify
3. Products + user message combined into a single prompt
4. Llama 3.3 reasons over products and generates recommendation
5. Response streamed back to UI

## Limitations & Future Improvements
- Conversation history resets on server restart (fix: Redis)
- No user authentication (fix: Shopify customer accounts)
- No product images in chat (fix: add image URLs to GraphQL query)
- Single store only (fix: multi-tenant architecture)
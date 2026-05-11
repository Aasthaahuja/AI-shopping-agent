# Decision Log — Kasparro Fashion AI Shopping Agent

## Decision 1: Groq (Llama 3.3) over OpenAI/Gemini
**Date:** May 10, 2026  
**Decision:** Used Groq API with Llama 3.3-70b instead of GPT-4 or Gemini  
**Reason:** Groq offers genuinely free API access with no credit card required, making the project accessible and reproducible. Gemini free tier hit rate limits during testing. Llama 3.3-70b performs comparably to GPT-4 for conversational tasks.  
**Tradeoff:** Slightly less brand recognition than OpenAI, but better reliability for free-tier development.

## Decision 2: Fetch all products, filter client-side
**Date:** May 10, 2026  
**Decision:** Instead of passing user query directly to Shopify's search API, we fetch all products and let the LLM do the filtering/reasoning.  
**Reason:** Shopify's storefront search matches on exact keywords. A user saying "something for the gym" wouldn't match "Black Yoga Leggings". The LLM understands intent far better.  
**Tradeoff:** Slightly more data sent per request, but much better recommendation quality.

## Decision 3: Flask over FastAPI or Next.js
**Date:** May 10, 2026  
**Decision:** Used Flask for the backend web server.  
**Reason:** Flask is lightweight, fast to set up, and sufficient for a hackathon prototype. The project needed a simple REST endpoint — Flask does this in under 20 lines.  
**Tradeoff:** Not production-scalable, but perfect for demo purposes.

## Decision 4: Conversation history in memory
**Date:** May 10, 2026  
**Decision:** Stored conversation history in a Python list (in-memory) rather than a database.  
**Reason:** For a hackathon demo, persistence across sessions isn't required. In-memory storage keeps the codebase simple and fast.  
**Tradeoff:** History resets on server restart. A production version would use Redis or a database.

## Decision 5: System prompt engineering for product display
**Date:** May 10, 2026  
**Decision:** Explicitly instructed the LLM in the system prompt to always list products with name, price, and reasoning.  
**Reason:** Without explicit formatting instructions, the LLM sometimes gave vague answers without showing products. Prompt engineering solved this without any code changes.  
**Tradeoff:** Prompt length increases slightly, but response quality improved dramatically.
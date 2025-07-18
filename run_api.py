import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from salesgpt.salesgpt import SalesGPT
from product_catalog import COFFEE_MACHINES, get_product_info, search_products
from coffee_sales_agent import SALES_AGENT_PROMPT, COMPANY_INFO

app = FastAPI(title="Kahve Makinesi Satış Chatbot")

# Pydantic modeller
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    agent_name: str

# SalesGPT ajanını başlat
sales_agent = SalesGPT.from_llm(
    llm_name="gpt-3.5-turbo",
    verbose=True,
    salesperson_name="Ali - Kahve Uzmanı",
    salesperson_role="Kahve makinesi satış uzmanı",
    company_name="Kahve Dünyası",
    company_business="Profesyonel kahve makinesi satışı",
    company_values="Müşteri memnuniyeti ve kaliteli kahve deneyimi",
    conversation_purpose="Müşterilere kahve makinesi satışı konusunda yardım etmek",
    conversation_history=[],
    use_tools=True,
    product_catalog=str(COFFEE_MACHINES)
)

@app.get("/")
async def root():
    return {
        "message": "Kahve Makinesi Satış Chatbot API",
        "company": COMPANY_INFO["name"],
        "business": COMPANY_INFO["business"],
        "endpoints": {
            "chat": "/chat",
            "products": "/products",
            "product_info": "/product/{product_id}"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    try:
        # Müşteri mesajını SalesGPT'ye gönder
        sales_agent.step(message.message)
        
        # Yanıtı al
        response = sales_agent.conversation_history[-1]['content']
        
        return ChatResponse(
            response=response,
            agent_name="Ali - Kahve Uzmanı"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_all_products():
    """Tüm ürünleri listele"""
    return {
        "products": [
            {
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "stock": product["stock"]
            }
            for product_id, product in COFFEE_MACHINES.items()
        ]
    }

@app.get("/product/{product_id}")
async def get_product_details(product_id: str):
    """Belirli bir ürünün detaylarını getir"""
    product = get_product_info(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product

@app.get("/search")
async def search_products_endpoint(q: str):
    """Ürün araması yap"""
    results = search_products(q)
    return {"query": q, "results": results}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Kahve Chatbot API"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

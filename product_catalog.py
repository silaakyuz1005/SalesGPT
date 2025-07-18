# Kahve Makinesi Ürün Kataloğu
COFFEE_MACHINES = {
    "delonghi_magnifica": {
        "name": "DeLonghi Magnifica S",
        "water_capacity": "1.8 litre",
        "price": "15.999 TL",
        "warranty": "2 yıl",
        "stock": True,
        "features": [
            "Otomatik cappuccino yapma",
            "Çift boiler sistemi", 
            "15 bar basınç",
            "Entegre değirmen"
        ],
        "description": "Profesyonel kahve deneyimi için ideal otomatik espresso makinesi"
    },
    "nespresso_vertuo": {
        "name": "Nespresso Vertuo Next",
        "water_capacity": "1.1 litre",
        "price": "3.299 TL", 
        "warranty": "2 yıl",
        "stock": False,
        "features": [
            "Bluetooth bağlantı",
            "4 farklı fincan boyutu",
            "Centrifusion teknolojisi"
        ],
        "description": "Pratik kullanım için kapsüllü kahve makinesi"
    },
    "breville_barista": {
        "name": "Breville Barista Express",
        "water_capacity": "2.0 litre",
        "price": "24.999 TL",
        "warranty": "3 yıl",
        "stock": True,
        "features": [
            "Manuel espresso yapma",
            "Entegre değirmen",
            "Süt buharı wand",
            "Pressure gauge"
        ],
        "description": "Barista seviyesi kahve yapma deneyimi"
    }
}

def get_product_info(product_id):
    """Ürün bilgilerini getir"""
    return COFFEE_MACHINES.get(product_id)

def search_products(query):
    """Ürün araması yap"""
    results = []
    query_lower = query.lower()
    
    for product_id, product in COFFEE_MACHINES.items():
        if (query_lower in product['name'].lower() or 
            query_lower in product['description'].lower()):
            results.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price']
            })
    
    return results

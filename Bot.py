import requests
import time

# --- CONFIGURAÇÕES DO SEU BOT ---
TOKEN_TELEGRAM = "8810409529:AAHwecVL79jo75irUDZRBXXVZaL9Ff-gr7I"
ID_CANAL = "-1004421977793" 

NICHOS = {
    "📱 CELULARES": "MLB1055",
    "📺 SMART TVs": "MLB1002",
    "🖥️ PLACAS DE VÍDEO": "MLB1658"
}

def enviar_mensagem_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": ID_CANAL,
        "text": texto,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def buscar_ofertas(nome_nicho, id_categoria):
    print(f"Verificando {nome_nicho}...")
    url = f"https://api.mercadolibre.com/sites/MLB/search?category={id_categoria}&condition=new&limit=15"
    
    try:
        resposta = requests.get(url).json()
        for item in resposta.get('results', []):
            titulo = item.get('title')
            preco_atual = item.get('price')
            link = item.get('permalink')
            preco_original = item.get('original_price')
            
            if preco_original:
                desconto = int(((preco_original - preco_atual) / preco_original) * 100)
                
                if desconto >= 1:  
                    mensagem = (
                        f"🔥 *{nome_nicho} EM OFERTA!* 🔥\n"
                        f"_____________________________________\n\n"
                        f"📦 *{titulo}*\n"
                        f"❌ De: R$ {preco_original:,.2f}\n"
                        f"✅ Por: *R$ {preco_atual:,.2f}* ({desconto}% OFF)\n\n"
                        f"🛒 *Compre aqui:* {link}\n"
                        f"_____________________________________\n"
                    )
                    enviar_mensagem_telegram(mensagem)
                    print(f"Postado: {titulo[:20]}...")
                    time.sleep(4)
    except Exception as e:
        print(f"Erro no Mercado Livre: {e}")

while True:
    for nome, id_cat in NICHOS.items():
        buscar_ofertas(nome, id_cat)
        time.sleep(3) 
    print("Aguardando próxima verredura...")
    time.sleep(1800)

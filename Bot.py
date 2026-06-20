import urllib.request
import xml.etree.ElementTree as ET
import requests
import json
import time
import sys

# Garante que todos os prints aparecem no Render na hora!
def print_instantaneo(texto):
    print(texto)
    sys.stdout.flush()

TOKEN_TELEGRAM = "8810409529:AAHwecVL79jo75irUDZRBXXVZaL9Ff-gr7I"
ID_CANAL = "-1004421977793" 

TERMOS_TECH = [
    "celular", "smartphone", "iphone", "galaxy", "xiaomi", "moto",
    "tv", "smart tv", "televisao", "monitor", "placa de video", 
    "notebook", "laptop", "computador", "pc", "gamer", "rtx",
    "playstation", "xbox", "nintendo", "console", "fone"
]

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": ID_CANAL, "text": texto, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print_instantaneo(f"Erro Telegram: {e}")

def buscar_ofertas_feed():
    print_instantaneo("Acessando o Feed de Ofertas do Mercado Livre...")
    url = "https://rss.mercadolivre.com.br/jm/rss?reid=MLB"
    try:
        # Usando requests que o Render aceita muito bem
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(response.content)
        
        itens = root.findall('.//item')
        print_instantaneo(f"Produtos encontrados no feed: {len(itens)}. Filtrando tech...")
        
        for item in itens:
            titulo = item.find('title').text
            link = item.find('link').text
            
            if any(termo in titulo.lower() for termo in TERMOS_TECH):
                msg = (
                    f"🔥 *PRODUTO EM DESTAQUE!* 🔥\n"
                    f"_____________________________________\n\n"
                    f"📦 *{titulo}*\n\n"
                    f"🛒 *Confira o preço e compre aqui:*\n"
                    f"{link}\n"
                    f"_____________________________________\n"
                )
                enviar_mensagem(msg)
                print_instantaneo(f"Postado: {titulo[:25]}...")
                time.sleep(5)
    except Exception as e:
        print_instantaneo(f"Erro ao ler o Feed: {e}")

# Loop Principal
while True:
    buscar_ofertas_feed()
    print_instantaneo("Aguardando 15 minutos para a próxima varredura...")
    time.sleep(900)

import os
import random
import requests

ML_SEARCH_URL = "https://api.mercadolibre.com/sites/MLB/search"


def buscar_produtos(keywords: list[str], tracking_id: str = "", limite: int = 5) -> list[dict]:
    """Busca produtos no Mercado Livre e retorna lista formatada."""
    keyword = random.choice(keywords)
    params = {
        "q": keyword,
        "limit": 20,
    
    }
    try:
        resp = requests.get(ML_SEARCH_URL, params=params, timeout=15, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Erro ao buscar produtos no ML: {e}")
        return []

    resultados = []
    for item in data.get("results", []):
        preco = item.get("price", 0)
        preco_original = item.get("original_price") or preco
        desconto = 0
        if preco_original and preco_original > preco:
            desconto = round((1 - preco / preco_original) * 100)

        thumbnail = item.get("thumbnail", "")
        thumbnail = thumbnail.replace("I.jpg", "O.jpg") if thumbnail else ""

        link = item.get("permalink", "")
        if tracking_id:
            sep = "&" if "?" in link else "?"
            link = f"{link}{sep}tracking_id={tracking_id}"

        resultados.append({
            "titulo": item.get("title", ""),
            "preco": preco,
            "preco_original": preco_original,
            "desconto": desconto,
            "thumbnail": thumbnail,
            "link": link,
        })

        if len(resultados) >= limite:
            break

    return resultados

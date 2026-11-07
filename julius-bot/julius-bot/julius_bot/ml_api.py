"""
Busca produtos no Mercado Livre via API pública.
Sem necessidade de autenticação para busca básica.
"""

import requests
import random


def buscar_produtos(query: str, preco_max: int = 150, limit: int = 8) -> list[dict]:
    """
    Busca produtos no ML com frete grátis e bom preço.
    Retorna lista de dicts com título, preço, thumbnail e link.
    """
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {
        "q": query,
        "sort": "relevance",
        "price": f"0-{preco_max}",
        "condition": "new",
        "shipping": "free",
        "limit": 20
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erro ao buscar '{query}' no ML: {e}")
        return []

    produtos = []
    for item in data.get("results", []):
        # pula sem thumbnail
        if not item.get("thumbnail"):
            continue

        # filtra por vendas mínimas (relevância)
        vendas = item.get("sold_quantity", 0)
        if vendas < 10:
            continue

        produtos.append({
            "id": item["id"],
            "titulo": item["title"][:60],
            "preco": item["price"],
            "thumbnail": item["thumbnail"].replace("-I.", "-O."),
            "link": item["permalink"],
            "vendas": vendas,
            "plataforma": "ML"
        })

        if len(produtos) >= limit:
            break

    return produtos


def gerar_link_afiliado(item_id: str, tracking_id: str) -> str:
    """
    Gera link de afiliado do Mercado Livre.
    tracking_id é o seu ID no painel de afiliados do ML.
    """
    if not tracking_id:
        return f"https://www.mercadolivre.com.br/p/{item_id}"
    return (
        f"https://produto.mercadolivre.com.br/{item_id}"
        f"?matt_from=aff&matt_word=&matt_source=google"
        f"&tracking_id={tracking_id}"
    )


def buscar_multiplos_termos(termos: list[str], preco_max: int) -> list[dict]:
    """
    Busca por vários termos e retorna os melhores produtos combinados.
    Embaralha para variar os posts.
    """
    todos = []
    for termo in termos:
        produtos = buscar_produtos(termo, preco_max, limit=3)
        todos.extend(produtos)

    # remove duplicatas por ID
    vistos = set()
    unicos = []
    for p in todos:
        if p["id"] not in vistos:
            vistos.add(p["id"])
            unicos.append(p)

    random.shuffle(unicos)
    return unicos[:8]

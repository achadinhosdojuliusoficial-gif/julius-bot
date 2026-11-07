"""
Faz upload das imagens para o Imgur e retorna URLs públicas.
O Instagram Graph API precisa de URLs HTTPS acessíveis publicamente.
Imgur é gratuito e gera URLs públicas instantâneas.
"""

import base64
import requests


def upload_imagem(caminho: str, client_id: str) -> str | None:
    """
    Faz upload de uma imagem para o Imgur.
    Retorna a URL pública da imagem ou None em caso de erro.
    """
    with open(caminho, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    try:
        response = requests.post(
            "https://api.imgur.com/3/image",
            headers={"Authorization": f"Client-ID {client_id}"},
            data={"image": image_data, "type": "base64"},
            timeout=30
        )
        response.raise_for_status()
        url = response.json()["data"]["link"]
        print(f"Upload OK: {url}")
        return url
    except Exception as e:
        print(f"Erro no upload para Imgur: {e}")
        return None


def upload_multiplas(caminhos: list[str], client_id: str) -> list[str]:
    """
    Faz upload de múltiplas imagens.
    Retorna lista de URLs (pula as que falharem).
    """
    urls = []
    for caminho in caminhos:
        url = upload_imagem(caminho, client_id)
        if url:
            urls.append(url)
    return urls

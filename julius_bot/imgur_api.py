"""
Faz upload de imagens no ImgBB e retorna a URL pública.
"""
import requests
import base64
import os


IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def upload_imagem(caminho_imagem: str) -> str | None:
    """Faz upload de uma imagem no ImgBB e retorna a URL pública."""
    api_key = os.environ.get("IMGUR_CLIENT_ID", "")
    if not api_key:
        print("[ImgBB] IMGUR_CLIENT_ID não definido")
        return None

    with open(caminho_imagem, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    try:
        resp = requests.post(
            IMGBB_UPLOAD_URL,
            data={"key": api_key, "image": image_data},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        url = data["data"]["url"]
        print(f"[ImgBB] Upload OK: {url}")
        return url
    except Exception as e:
        print(f"[ImgBB] Erro no upload: {e}")
        return None

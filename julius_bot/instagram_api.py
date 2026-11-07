"""
Publica carroussel no Instagram usando a Graph API.
"""
import os
import requests
import time


GRAPH_URL = "https://graph.instagram.com/v21.0"


def _token() -> str:
    return os.environ.get("IG_ACCESS_TOKEN", "")


def _user_id() -> str:
    return os.environ.get("IG_USER_ID", "")


def _criar_container_imagem(url_imagem: str, is_carousel_item: bool = True) -> str | None:
    """Cria um container de mídia para um item do carousel."""
    params = {
        "image_url": url_imagem,
        "is_carousel_item": "true" if is_carousel_item else "false",
        "access_token": _token(),
    }
    try:
        resp = requests.post(f"{GRAPH_URL}/{_user_id()}/media", data=params, timeout=30)
        resp.raise_for_status()
        container_id = resp.json().get("id")
        print(f"[IG] Container criado: {container_id}")
        return container_id
    except Exception as e:
        print(f"[IG] Erro ao criar container: {e} | {getattr(e, 'response', None) and e.response.text}")
        return None


def publicar_carousel(urls_imagens: list[str], legenda: str) -> bool:
    """Publica um carousel no Instagram com as imagens e legenda fornecidas."""
    if not _token() or not _user_id():
        print("[IG] IG_ACCESS_TOKEN ou IG_USER_ID não definidos")
        return False

    container_ids = []
    for url in urls_imagens:
        cid = _criar_container_imagem(url)
        if cid:
            container_ids.append(cid)
        time.sleep(1)

    if len(container_ids) < 2:
        print(f"[IG] Poucos containers criados ({len(container_ids)}), abortando")
        return False

    children = ",".join(container_ids)
    params = {
        "media_type": "CAROUSEL",
        "children": children,
        "caption": legenda,
        "access_token": _token(),
    }
    try:
        resp = requests.post(f"{GRAPH_URL}/{_user_id()}/media", data=params, timeout=30)
        resp.raise_for_status()
        carousel_id = resp.json().get("id")
        print(f"[IG] Carousel container criado: {carousel_id}")
    except Exception as e:
        print(f"[IG] Erro ao criar carousel: {e} | {getattr(e, 'response', None) and e.response.text}")
        return False

    time.sleep(5)

    try:
        resp = requests.post(
            f"{GRAPH_URL}/{_user_id()}/media_publish",
            data={"creation_id": carousel_id, "access_token": _token()},
            timeout=30,
        )
        resp.raise_for_status()
        post_id = resp.json().get("id")
        print(f"[IG] Post publicado! ID: {post_id}")
        return True
    except Exception as e:
        print(f"[IG] Erro ao publicar: {e} | {getattr(e, 'response', None) and e.response.text}")
        return False

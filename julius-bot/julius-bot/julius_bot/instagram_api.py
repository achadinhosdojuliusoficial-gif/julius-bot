"""
Publica posts no Instagram via Graph API.
Suporta post único e carrossel.
"""

import time
import requests


GRAPH_URL = "https://graph.facebook.com/v19.0"


def _post(endpoint: str, data: dict) -> dict:
    """Faz requisição POST para a Graph API."""
    response = requests.post(
        f"{GRAPH_URL}/{endpoint}",
        data=data,
        timeout=30
    )
    result = response.json()
    if "error" in result:
        raise Exception(f"Graph API erro: {result['error']}")
    return result


def criar_container_imagem(ig_user_id: str, access_token: str,
                            image_url: str, is_carousel_item: bool = False,
                            caption: str = "") -> str:
    """Cria um container de mídia no Instagram. Retorna o ID do container."""
    data = {
        "image_url": image_url,
        "access_token": access_token,
    }
    if is_carousel_item:
        data["is_carousel_item"] = "true"
    else:
        data["caption"] = caption

    result = _post(f"{ig_user_id}/media", data)
    return result["id"]


def criar_container_carrossel(ig_user_id: str, access_token: str,
                               item_ids: list[str], caption: str) -> str:
    """Cria o container do carrossel com os IDs dos itens."""
    data = {
        "media_type": "CAROUSEL",
        "children": ",".join(item_ids),
        "caption": caption,
        "access_token": access_token
    }
    result = _post(f"{ig_user_id}/media", data)
    return result["id"]


def publicar_container(ig_user_id: str, access_token: str,
                        creation_id: str) -> str:
    """Publica o container criado. Retorna o ID do post publicado."""
    data = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    result = _post(f"{ig_user_id}/media_publish", data)
    return result["id"]


def verificar_status_container(container_id: str, access_token: str) -> str:
    """Verifica o status de processamento de um container."""
    response = requests.get(
        f"{GRAPH_URL}/{container_id}",
        params={
            "fields": "status_code,status",
            "access_token": access_token
        },
        timeout=10
    )
    data = response.json()
    return data.get("status_code", "UNKNOWN")


def publicar_carrossel(ig_user_id: str, access_token: str,
                        image_urls: list[str], caption: str) -> str:
    """
    Fluxo completo de publicação de carrossel.
    1. Cria container para cada imagem
    2. Cria container do carrossel
    3. Aguarda processamento
    4. Publica
    Retorna o ID do post publicado.
    """
    if not image_urls:
        raise ValueError("Nenhuma URL de imagem fornecida")

    if len(image_urls) > 10:
        image_urls = image_urls[:10]

    print(f"Criando {len(image_urls)} containers de imagem...")
    item_ids = []
    for i, url in enumerate(image_urls, 1):
        print(f"  Container {i}/{len(image_urls)}: {url[:60]}...")
        item_id = criar_container_imagem(ig_user_id, access_token, url,
                                          is_carousel_item=True)
        item_ids.append(item_id)
        time.sleep(1)

    print("Criando container do carrossel...")
    carousel_id = criar_container_carrossel(ig_user_id, access_token,
                                             item_ids, caption)

    # aguarda processamento (pode levar alguns segundos)
    print("Aguardando processamento...")
    for tentativa in range(10):
        time.sleep(3)
        status = verificar_status_container(carousel_id, access_token)
        print(f"  Status: {status}")
        if status == "FINISHED":
            break
        if status == "ERROR":
            raise Exception("Erro no processamento do carrossel pelo Instagram")

    print("Publicando...")
    post_id = publicar_container(ig_user_id, access_token, carousel_id)
    print(f"Post publicado! ID: {post_id}")
    return post_id

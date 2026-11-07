"""
JuliusBot — Robô de postagem automática no Instagram.
Orquestra busca de produtos, geração de imagens e publicação.
"""

import os
import json
import shutil
import datetime

from ml_api import buscar_multiplos_termos, gerar_link_afiliado
from image_generator import gerar_carrossel
from imgur_api import upload_multiplas
from instagram_api import publicar_carrossel
from caption_generator import gerar_legenda


def carregar_config() -> dict:
    """Carrega variáveis de ambiente necessárias."""
    config = {
        "access_token": os.environ.get("IG_ACCESS_TOKEN"),
        "ig_user_id": os.environ.get("IG_USER_ID", "17841445236163606"),
        "imgur_client_id": os.environ.get("IMGUR_CLIENT_ID"),
        "ml_tracking_id": os.environ.get("ML_TRACKING_ID", ""),
    }
    erros = [k for k, v in config.items() if not v and k != "ml_tracking_id"]
    if erros:
        raise EnvironmentError(f"Variáveis de ambiente faltando: {', '.join(erros)}")
    return config


def carregar_nichos() -> list[dict]:
    """Carrega lista de nichos do arquivo de configuração."""
    caminho = os.path.join(os.path.dirname(__file__), "..", "nichos.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)["nichos"]


def escolher_nicho(nichos: list[dict]) -> dict:
    """
    Escolhe o nicho do dia com base na data.
    Rotação circular — cada dia um nicho diferente.
    """
    dia_do_ano = datetime.date.today().timetuple().tm_yday
    indice = dia_do_ano % len(nichos)
    nicho = nichos[indice]
    print(f"Nicho do dia: {nicho['nome']} (índice {indice})")
    return nicho


def run():
    """Execução principal do robô."""
    print("=" * 50)
    print(f"JuliusBot iniciando — {datetime.datetime.now()}")
    print("=" * 50)

    config = carregar_config()
    nichos = carregar_nichos()
    nicho = escolher_nicho(nichos)

    # 1. Busca produtos
    print(f"\n[1/5] Buscando produtos para: {nicho['nome']}")
    produtos = buscar_multiplos_termos(nicho["termos_ml"], nicho["preco_max"])

    if len(produtos) < 3:
        print(f"Poucos produtos encontrados ({len(produtos)}). Abortando.")
        return

    # adiciona links de afiliado
    for p in produtos:
        p["link_afiliado"] = gerar_link_afiliado(p["id"], config["ml_tracking_id"])

    print(f"Produtos encontrados: {len(produtos)}")
    for p in produtos:
        print(f"  - {p['titulo'][:50]} | R$ {p['preco']:.2f}")

    # 2. Gera imagens
    print(f"\n[2/5] Gerando imagens do carrossel...")
    output_dir = "/tmp/julius_slides"
    arquivos = gerar_carrossel(nicho, produtos, output_dir)
    print(f"Slides gerados: {len(arquivos)}")

    # 3. Faz upload para Imgur
    print(f"\n[3/5] Fazendo upload das imagens...")
    urls = upload_multiplas(arquivos, config["imgur_client_id"])

    if len(urls) < 2:
        print("Falha no upload das imagens. Abortando.")
        return

    print(f"URLs geradas: {len(urls)}")

    # 4. Gera legenda
    print(f"\n[4/5] Gerando legenda...")
    legenda = gerar_legenda(nicho, produtos)
    print("Legenda:")
    print(legenda[:200] + "...")

    # 5. Publica no Instagram
    print(f"\n[5/5] Publicando no Instagram...")
    post_id = publicar_carrossel(
        config["ig_user_id"],
        config["access_token"],
        urls,
        legenda
    )

    print(f"\n✅ Post publicado com sucesso! ID: {post_id}")
    print(f"Nicho: {nicho['nome']} | Produtos: {len(produtos)} | Slides: {len(urls)}")

    # limpa arquivos temporários
    shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    run()

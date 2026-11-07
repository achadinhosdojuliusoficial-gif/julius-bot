"""
Ponto de entrada principal do JuliusBot.
Fluxo: busca produtos -> gera imagens -> faz upload -> publica no Instagram.
"""
import json
import os
import random
import shutil
import sys
import tempfile

from julius_bot.ml_api import buscar_produtos
from julius_bot.image_generator import gerar_carousel
from julius_bot.imgur_api import upload_imagem
from julius_bot.caption_generator import gerar_legenda
from julius_bot.instagram_api import publicar_carousel


def carregar_nichos(caminho: str = "nichos.json") -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)["nichos"]


def main() -> None:
    print("=" * 60)
    print("🛒  JuliusBot — Achadinhos do Julius  iniciando...")
    print("=" * 60)

    tracking_id = os.environ.get("ML_TRACKING_ID", "")

    nichos = carregar_nichos()
    nicho = random.choice(nichos)
    print(f"[main] Nicho selecionado: {nicho['nome']}")

    produtos = buscar_produtos(nicho["keywords"], tracking_id=tracking_id, limite=5)
    if not produtos:
        print("[main] Nenhum produto encontrado. Encerrando.")
        sys.exit(0)
    print(f"[main] {len(produtos)} produtos encontrados.")
h
    pasta_tmp = tempfile.mkdtemp(prefix="julius_")
    try:h
        imagens = gerar_carousel(nicho["nome"], produtos, pasta=pasta_tmp)
        print(f"[main] {len(imagens)} imagens geradas.")

        urls = []
        for img_path in imagens:
            url = upload_imagem(img_path)
            if url:
                urls.append(url)

        if len(urls) < 2:
            print(f"[main] Upload insuficiente ({len(urls)} imagens). Encerrando.")
            sys.exit(0)
        print(f"[main] {len(urls)} imagens no ar.")

        hashtags = " ".join(nicho.get("hashtags", []))
        legenda = gerar_legenda(nicho["nome"], produtos, hashtags)

        sucesso = publicar_carousel(urls, legenda)
        if sucesso:
            print("[main] ✅ Post publicado com sucesso!")
        else:
            print("[main] ❌ Falha ao publicar.")
            sys.exit(0)
    finally:
        shutil.rmtree(pasta_tmp, ignore_errors=True)


if __name__ == "__main__":
    main()

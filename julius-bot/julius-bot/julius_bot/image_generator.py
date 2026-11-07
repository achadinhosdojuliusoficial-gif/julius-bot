"""
Gera imagens do carrossel no estilo Achadinhos do Julius.
Dimensão padrão Instagram: 1080x1080px
"""

import os
import io
import textwrap
import requests
from PIL import Image, ImageDraw, ImageFont


# Paleta de cores do Julius
FUNDO = (18, 18, 18)        # preto
DESTAQUE = (255, 200, 0)    # amarelo
TEXTO = (255, 255, 255)     # branco
CINZA = (80, 80, 80)        # cinza escuro
VERDE = (0, 200, 100)       # preço


def _fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    """Tenta carregar fonte do sistema, cai para padrão se não encontrar."""
    candidatos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if negrito
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if negrito
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidatos:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, tamanho)
            except Exception:
                continue
    return ImageFont.load_default()


def _baixar_imagem(url: str) -> Image.Image | None:
    """Baixa imagem de URL e retorna objeto PIL."""
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)).convert("RGBA")
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return None


def gerar_slide_capa(nicho: dict, num_produtos: int) -> Image.Image:
    """Slide 1: capa do nicho."""
    img = Image.new("RGB", (1080, 1080), FUNDO)
    draw = ImageDraw.Draw(img)

    # faixa amarela no topo
    draw.rectangle([0, 0, 1080, 12], fill=DESTAQUE)

    # emoji grande
    f_emoji = _fonte(120, negrito=True)
    draw.text((540, 220), nicho["emoji"], font=f_emoji, fill=DESTAQUE, anchor="mm")

    # título
    f_titulo = _fonte(72, negrito=True)
    draw.text((540, 380), nicho["nome"], font=f_titulo, fill=TEXTO, anchor="mm")

    # subtítulo
    f_sub = _fonte(38)
    linhas = textwrap.wrap(nicho["descricao"], width=28)
    y = 480
    for linha in linhas:
        draw.text((540, y), linha, font=f_sub, fill=CINZA, anchor="mm")
        y += 55

    # badge produtos
    draw.rounded_rectangle([340, 620, 740, 700], radius=20, fill=DESTAQUE)
    f_badge = _fonte(36, negrito=True)
    draw.text((540, 660), f"🔥 {num_produtos} produtos no preço", font=f_badge,
              fill=FUNDO, anchor="mm")

    # rodapé
    f_rodape = _fonte(30)
    draw.text((540, 850), "@achadinhosdojuliusoficial", font=f_rodape,
              fill=DESTAQUE, anchor="mm")
    draw.text((540, 900), "Quanto custa por uso?", font=f_rodape,
              fill=CINZA, anchor="mm")

    # faixa amarela no fundo
    draw.rectangle([0, 1068, 1080, 1080], fill=DESTAQUE)

    return img


def gerar_slide_produto(produto: dict, numero: int, total: int) -> Image.Image:
    """Slide de produto individual."""
    img = Image.new("RGB", (1080, 1080), FUNDO)
    draw = ImageDraw.Draw(img)

    # faixa topo
    draw.rectangle([0, 0, 1080, 8], fill=DESTAQUE)

    # numeração
    f_num = _fonte(28)
    draw.text((54, 40), f"{numero}/{total}", font=f_num, fill=CINZA, anchor="lm")
    draw.text((1026, 40), "@achadinhosdojuliusoficial", font=f_num,
              fill=DESTAQUE, anchor="rm")

    # imagem do produto
    img_produto = _baixar_imagem(produto["thumbnail"])
    if img_produto:
        img_produto = img_produto.resize((500, 500), Image.LANCZOS)
        # fundo branco circular para o produto
        fundo_prod = Image.new("RGB", (520, 520), (240, 240, 240))
        fundo_prod.paste(img_produto, (10, 10), img_produto if img_produto.mode == "RGBA" else None)
        img.paste(fundo_prod, (280, 100))
    else:
        # placeholder
        draw.rounded_rectangle([280, 100, 800, 620], radius=20, fill=CINZA)
        draw.text((540, 360), produto.get("plataforma", "ML"), font=_fonte(60),
                  fill=FUNDO, anchor="mm")

    # título do produto
    f_titulo = _fonte(38, negrito=True)
    linhas = textwrap.wrap(produto["titulo"], width=30)
    y = 660
    for linha in linhas[:2]:
        draw.text((540, y), linha, font=f_titulo, fill=TEXTO, anchor="mm")
        y += 55

    # preço
    preco_str = f"R$ {produto['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    f_preco = _fonte(64, negrito=True)
    draw.text((540, 820), preco_str, font=f_preco, fill=VERDE, anchor="mm")

    # custo por uso (estilo Julius)
    usos = max(1, int(produto["preco"] / 2))
    f_julius = _fonte(28)
    draw.text((540, 900), f"Quanto custa por uso? R$ {produto['preco']/usos:.2f} 🤔",
              font=f_julius, fill=CINZA, anchor="mm")

    # faixa fundo
    draw.rectangle([0, 1068, 1080, 1080], fill=DESTAQUE)

    return img


def gerar_slide_cta(nicho: dict) -> Image.Image:
    """Último slide: chamada para ação."""
    img = Image.new("RGB", (1080, 1080), FUNDO)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 1080, 8], fill=DESTAQUE)

    f_grande = _fonte(80, negrito=True)
    draw.text((540, 300), "👆", font=f_grande, fill=DESTAQUE, anchor="mm")
    draw.text((540, 420), "LINK NA BIO!", font=f_grande, fill=DESTAQUE, anchor="mm")

    f_med = _fonte(42)
    draw.text((540, 540), "Todos os produtos com link", font=f_med, fill=TEXTO, anchor="mm")
    draw.text((540, 600), "de afiliado lá no Linktree 👆", font=f_med, fill=TEXTO, anchor="mm")

    f_small = _fonte(34)
    draw.text((540, 700), f"🔥 {nicho['nome']}", font=f_small, fill=CINZA, anchor="mm")

    draw.rounded_rectangle([200, 780, 880, 860], radius=25, fill=DESTAQUE)
    f_btn = _fonte(38, negrito=True)
    draw.text((540, 820), "Salva esse post! 🔖", font=f_btn, fill=FUNDO, anchor="mm")

    f_user = _fonte(32)
    draw.text((540, 940), "@achadinhosdojuliusoficial", font=f_user,
              fill=DESTAQUE, anchor="mm")
    draw.text((540, 990), '"Quanto custa por uso?"', font=_fonte(26),
              fill=CINZA, anchor="mm")

    draw.rectangle([0, 1068, 1080, 1080], fill=DESTAQUE)

    return img


def gerar_carrossel(nicho: dict, produtos: list[dict], output_dir: str) -> list[str]:
    """
    Gera todos os slides do carrossel e salva em output_dir.
    Retorna lista de caminhos dos arquivos.
    """
    os.makedirs(output_dir, exist_ok=True)
    arquivos = []

    # slide capa
    capa = gerar_slide_capa(nicho, len(produtos))
    path_capa = os.path.join(output_dir, "slide_00_capa.jpg")
    capa.save(path_capa, "JPEG", quality=92)
    arquivos.append(path_capa)
    print(f"Slide capa salvo: {path_capa}")

    # slides de produtos
    for i, produto in enumerate(produtos, 1):
        slide = gerar_slide_produto(produto, i, len(produtos))
        path = os.path.join(output_dir, f"slide_{i:02d}_produto.jpg")
        slide.save(path, "JPEG", quality=92)
        arquivos.append(path)
        print(f"Slide {i} salvo: {path}")

    # slide CTA
    cta = gerar_slide_cta(nicho)
    path_cta = os.path.join(output_dir, f"slide_{len(produtos)+1:02d}_cta.jpg")
    cta.save(path_cta, "JPEG", quality=92)
    arquivos.append(path_cta)
    print(f"Slide CTA salvo: {path_cta}")

    return arquivos

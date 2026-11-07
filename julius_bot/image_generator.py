"""
Gera imagem 1080x1080 estilo carousel para o Instagram.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


LARGURA = 1080
ALTURA = 1080
COR_FUNDO = (18, 18, 18)
COR_DESTAQUE = (255, 200, 0)
COR_TEXTO = (255, 255, 255)
COR_SUBTEXT = (180, 180, 180)
COR_BADGE = (220, 50, 50)


def _baixar_thumbnail(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        return img
    except Exception as e:
        print(f"[IMG] Erro ao baixar thumbnail: {e}")
        return None


def _formatar_preco(preco: float) -> str:
    return f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _get_font(size, bold=False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except Exception:
        return ImageFont.load_default()


def gerar_imagem_capa(nicho: str, caminho_saida: str) -> str:
    img = Image.new("RGB", (LARGURA, ALTURA), COR_FUNDO)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 400), (LARGURA, 680)], fill=COR_DESTAQUE)
    f_titulo = _get_font(90, bold=True)
    f_sub = _get_font(48)
    f_mini = _get_font(36)
    draw.text((LARGURA // 2, 300), "ACHADINHOS", font=f_titulo, fill=COR_DESTAQUE, anchor="mm")
    draw.text((LARGURA // 2, 540), nicho.upper(), font=f_titulo, fill=COR_FUNDO, anchor="mm")
    draw.text((LARGURA // 2, 750), "do JULIUS", font=f_sub, fill=COR_TEXTO, anchor="mm")
    draw.text((LARGURA // 2, 950), "🔥 Link na bio: linktr.ee/achadinhosdojuliusoficial", font=f_mini, fill=COR_SUBTEXT, anchor="mm")
    img.save(caminho_saida, "JPEG", quality=92)
    return caminho_saida


def gerar_imagem_produto(produto: dict, numero: int, caminho_saida: str) -> str:
    img = Image.new("RGB", (LARGURA, ALTURA), COR_FUNDO)
    draw = ImageDraw.Draw(img)
    f_num = _get_font(120, bold=True)
    f_titulo = _get_font(52, bold=True)
    f_preco = _get_font(80, bold=True)
    f_de = _get_font(36)
    f_mini = _get_font(32)
    draw.text((60, 60), f"#{numero}", font=f_num, fill=COR_DESTAQUE)
    thumb = _baixar_thumbnail(produto.get("thumbnail", ""))
    if thumb:
        thumb = thumb.convert("RGB")
        thumb.thumbnail((500, 500), Image.LANCZOS)
        x = (LARGURA - thumb.width) // 2
        img.paste(thumb, (x, 120))
    titulo = produto.get("titulo", "")
    linhas = textwrap.wrap(titulo, width=28)[:3]
    y_titulo = 650
    for linha in linhas:
        draw.text((LARGURA // 2, y_titulo), linha, font=f_titulo, fill=COR_TEXTO, anchor="mm")
        y_titulo += 65
    preco = produto.get("preco", 0)
    preco_original = produto.get("preco_original", preco)
    desconto = produto.get("desconto", 0)
    if desconto >= 5:
        draw.text((LARGURA // 2, 820), f"De: {_formatar_preco(preco_original)}", font=f_de, fill=COR_SUBTEXT, anchor="mm")
        draw.rounded_rectangle([(800, 60), (1000, 140)], radius=20, fill=COR_BADGE)
        draw.text((900, 100), f"-{desconto}%", font=f_de, fill=COR_TEXTO, anchor="mm")
    draw.text((LARGURA // 2, 900), _formatar_preco(preco), font=f_preco, fill=COR_DESTAQUE, anchor="mm")
    draw.text((LARGURA // 2, 990), "👉 Link na bio!", font=f_mini, fill=COR_SUBTEXT, anchor="mm")
    img.save(caminho_saida, "JPEG", quality=92)
    return caminho_saida


def gerar_carousel(nicho: str, produtos: list[dict], pasta: str = "/tmp") -> list[str]:
    os.makedirs(pasta, exist_ok=True)
    imagens = [gerar_imagem_capa(nicho, os.path.join(pasta, "slide_00_capa.jpg"))]
    for i, produto in enumerate(produtos[:5], 1):
        path = os.path.join(pasta, f"slide_{i:02d}_produto.jpg")
        gerar_imagem_produto(produto, i, path)
        imagens.append(path)
    return imagens

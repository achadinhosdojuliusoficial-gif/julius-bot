"""
Gera a legenda do post no estilo do Julius de 'Todo Mundo Odeia o Chris'.
"""
import random


BORDOES = [
    "Quanto custa por uso? 🤔",
    "Isso aqui vale cada centavo! 💰",
    "Se durar 10 anos, sai baratinho! 😂",
    "Na época do meu pai, isso custava uma semana de salário.",
    "Compra agora antes de subir o dólar! 📈",
]

ABERTURAS = [
    "🛒 ACHADO DO DIA, família!",
    "🔥 Olha esse preço absurdo!",
    "💡 Dica de ouro do Julius:",
    "🎯 Quem é esperto aproveita!",
    "⚡ Achadinho imperdível hoje!",
]


def gerar_legenda(nicho: str, produtos: list[dict], hashtags: str) -> str:
    abertura = random.choice(ABERTURAS)
    bordao = random.choice(BORDOES)

    linhas = [
        f"{abertura}",
        f"",
        f"Nicho: {nicho} 🏠",
        f"",
    ]

    for i, p in enumerate(produtos[:5], 1):
        preco_fmt = f"R$ {p['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        linha = f"{i}. {p['titulo']} — {preco_fmt}"
        if p.get("desconto", 0) >= 5:
            linha += f" (-{p['desconto']}% OFF 🔥)"
        linhas.append(linha)

    linhas += [
        f"",
        f'👉 Link na bio: linktr.ee/achadinhosdojuliusoficial',
        f"",
        f'"{bordao}" — Julius',
        f"",
        hashtags,
    ]

    return "\n".join(linhas)

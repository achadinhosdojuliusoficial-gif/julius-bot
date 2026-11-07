"""
Gera legendas no estilo do Julius (Todo Mundo Odeia o Chris).
Sem dependência de API externa — usa templates com variações.
"""

import random


ABERTURAS = [
    "Ei, eu, o Julius, tô aqui pra te salvar de pagar caro 🤑",
    "Quanto custa por uso? Hoje eu calculei por você 🧮",
    "Julius aprovado. Fiz as contas e esses itens passaram no teste 📊",
    "Ninguém economiza mais do que eu. Olha o que achei 🔍",
    "Meu lema é: se tá caro, tem um jeito. Olha esses preços 👀",
]

FECHAMENTOS = [
    "🔗 Link completo na bio | Linktree: linktr.ee/achadinhosdojuliusoficial",
    "👆 Acessa o link na bio pra pegar todos os links de afiliado",
    "💾 Salva esse post antes de esquecer | Link na bio",
    "📌 Fixa esse post no perfil do seu melhor amigo sem dinheiro",
    "🛒 Todos os links organizados no Linktree — link na bio",
]

HASHTAGS_BASE = [
    "#achadinhos", "#dicasdecompras", "#economize",
    "#mercadolivre", "#shopee", "#produtosbaratos",
    "#dicasdomercadolivre", "#achadinhosdojulius"
]

HASHTAGS_NICHOS = {
    "primeiro_ape": ["#primeiroape", "#apartamento", "#casanova", "#organizacao", "#decoracao"],
    "home_office": ["#homeoffice", "#trabalhoremoto", "#escritorioemcasa", "#produtividade"],
    "estudante": ["#estudante", "#faculdade", "#universitario", "#material escolar"],
    "treino_casa": ["#treinoencasa", "#fitness", "#academia", "#exercicio", "#saude"],
    "cozinha": ["#cozinha", "#gastronomia", "#cozinhando", "#tempero", "#receita"],
    "pet_ape": ["#petlovers", "#gatos", "#cachorros", "#animaisdeestimacao", "#pet"],
    "organizacao": ["#organizacao", "#minimalismo", "#casaorganizada", "#marie kondo"],
}


def gerar_legenda(nicho: dict, produtos: list[dict]) -> str:
    """Gera legenda completa para o post."""
    abertura = random.choice(ABERTURAS)
    fechamento = random.choice(FECHAMENTOS)

    # lista dos produtos com preço
    linhas_produtos = []
    for p in produtos[:6]:
        preco = f"R$ {p['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        titulo_curto = p["titulo"][:45]
        linhas_produtos.append(f"✅ {titulo_curto} — {preco}")

    produtos_str = "\n".join(linhas_produtos)

    # hashtags
    hashtags_nicho = HASHTAGS_NICHOS.get(nicho.get("id", ""), [])
    todas_hashtags = HASHTAGS_BASE + hashtags_nicho
    random.shuffle(todas_hashtags)
    hashtags_str = " ".join(todas_hashtags[:18])

    legenda = f"""{abertura}

{nicho['emoji']} {nicho['nome'].upper()} — {nicho['descricao']}

{produtos_str}

{fechamento}

.
.
.
{hashtags_str}"""

    return legenda

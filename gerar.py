"""Gera dark.svg e light.svg do perfil AipeCorp no GitHub (molde GitAscii, marca AIPE)."""
import base64
import random
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).parent

TEMAS = {
    "dark": dict(bg="#08080a", borda="#222228", tinta="#f7f7f8", mudo="#8a8a93", luz="#c4b5ff",
                 chave="#9fb4ff", ponto="#34343c", secao="#f2dcec", ascii="#c4b5ff", fundo_ascii="#2a2a33",
                 jan="#0e0e12", logo="logo-branca.png", holo=("#e8e0ff", "#d6e0ff", "#f2dcec")),
    "light": dict(bg="#fafafa", borda="#e2e2e6", tinta="#0d0d0d", mudo="#6b6b73", luz="#4b3f7a",
                  chave="#2f3d6e", ponto="#c8c8ce", secao="#5a3550", ascii="#4b3f7a", fundo_ascii="#d9d9df",
                  jan="#f2f2f2", logo="logo-preta.png", holo=("#4b3f7a", "#2f3d6e", "#5a3550")),
}

MONO = "'Geist Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'DM Sans', 'Inter', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

INFO = [
    ("titulo", "AipeCorp@github"),
    ("Sigla", "Artificial Intelligence Performance Ecosystem"),
    ("Base", "Brasil"),
    ("Foco", "IA aplicada a operação e performance"),
    ("Stack", "Next.js · NestJS · Postgres · Docker"),
    ("titulo", "Produtos"),
    ("Tasks", "tasks.aipecorp.com"),
    ("Marketing", "mkt.aipecorp.com"),
    ("Recorder", "rec.aipecorp.com"),
    ("titulo", "Contato"),
    ("Site", "aipecorp.com"),
    ("GitHub", "github.com/AipeCorp"),
    ("WhatsApp", "+55 31 9938-2020"),
]

STACK = [("TypeScript", "#3178c6"), ("Next.js", None), ("NestJS", "#e0234e"), ("PostgreSQL", "#336791"),
         ("Docker", "#2496ed"), ("Python", "#3572a5"), ("Prisma", "#5a67d8"), ("Claude", "#d97757")]

LARG_LINHA = 56  # caracteres por linha no painel de informação


def ler_pgm(caminho):
    tokens = [t for linha in caminho.read_text().splitlines() if not linha.startswith("#") for t in linha.split()]
    w, h = int(tokens[1]), int(tokens[2])
    px = list(map(int, tokens[4:4 + w * h]))
    return [px[i * w:(i + 1) * w] for i in range(h)]


def ascii_glifo():
    rampa = " .:+#@@@@@"
    rng = random.Random(7)
    linhas = []
    for linha in ler_pgm(AQUI / "marca.pgm"):
        s = ""
        for v in linha:
            if v < 24:
                s += rng.choice("      .")  # textura de fundo, como o retrato do molde
            else:
                s += rampa[min(len(rampa) - 1, v * len(rampa) // 256)]
        linhas.append(s)
    return linhas


def cantos(w, t):
    return (f'<text x="6" y="14" font-family="{MONO}" font-size="10" fill="{t["luz"]}">+</text>'
            f'<text x="{w - 12}" y="14" font-family="{MONO}" font-size="10" fill="{t["luz"]}">+</text>')


def caixa(x, y, w, h, t, miolo):
    return (f'<g transform="translate({x}, {y})">'
            f'<rect width="{w}" height="{h}" fill="{t["bg"]}" stroke="{t["borda"]}" stroke-width="1"/>'
            f'{cantos(w, t)}{miolo}</g>')


def cabecalho(t):
    return caixa(0, 0, 800, 90, t,
                 f'<image x="24" y="16" height="30" width="{30 * 301 / 56:.0f}" href="data:image/png;base64,'
                 f'{base64.b64encode((AQUI / t["logo"]).read_bytes()).decode()}"/>'
                 f'<text x="24" y="72" font-family="{MONO}" font-size="14" fill="{t["luz"]}">@AipeCorp</text>'
                 f'<text x="776" y="46" text-anchor="end" font-family="{SANS}" font-size="12" '
                 f'fill="{t["mudo"]}">[ aipecorp.com ]</text>')


def terminal(t):
    w = h = 280
    partes = [f'<rect width="{w}" height="{h}" rx="12" fill="{t["jan"]}" stroke="{t["borda"]}"/>',
              f'<line x1="0" y1="30" x2="{w}" y2="30" stroke="{t["borda"]}"/>',
              '<circle cx="20" cy="15" r="5" fill="#ff5f56"/><circle cx="36" cy="15" r="5" fill="#ffbd2e"/>'
              '<circle cx="52" cy="15" r="5" fill="#27c93f"/>',
              f'<text x="{w / 2 + 14}" y="19" text-anchor="middle" font-family="{MONO}" font-size="10" '
              f'fill="{t["mudo"]}">AipeCorp@github: ~$ ./marca.sh</text>']
    linhas = ascii_glifo()
    x0, larg, y0, passo = 16, 248, 76, 4.4
    for i, s in enumerate(linhas):
        y = y0 + i * passo
        cor = t["ascii"]
        partes.append(
            f'<clipPath id="r{i}"><rect x="{x0}" y="{y - passo + 1:.1f}" height="{passo:.1f}" width="0">'
            f'<animate attributeName="width" from="0" to="{larg}" begin="{i * 0.06:.2f}s" dur="0.12s" '
            f'fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#r{i})"><text xml:space="preserve" x="{x0}" y="{y:.1f}" fill="{cor}" '
            f'font-family="{MONO}" font-size="4.1" textLength="{larg}" lengthAdjust="spacing">'
            f'{escape(s)}</text></g>')
    fim = len(linhas) * 0.06 + 0.2
    for j, frase in enumerate(("Artificial Intelligence", "Performance Ecosystem")):
        partes.append(
            f'<text x="16" y="{150 + j * 18}" font-family="{MONO}" font-size="12" fill="{t["tinta"]}" '
            f'opacity="0">{frase}<animate attributeName="opacity" from="0" to="1" '
            f'begin="{fim + j * 0.25:.2f}s" dur="0.3s" fill="freeze"/></text>')
    fim += 0.6
    for j, (linha, cor) in enumerate((("❯ ls produtos/", "mudo"), ("tasks/  mkt/  rec/", "chave"))):
        partes.append(
            f'<text x="16" y="{200 + j * 18}" font-family="{MONO}" font-size="11" fill="{t[cor]}" '
            f'opacity="0">{linha}<animate attributeName="opacity" from="0" to="1" '
            f'begin="{fim + j * 0.3:.2f}s" dur="0.2s" fill="freeze"/></text>')
    fim += 0.8
    partes.append(
        f'<text x="16" y="56" font-family="{MONO}" font-size="11" fill="{t["mudo"]}">'
        f'<tspan fill="{t["luz"]}">❯</tspan> ./marca.sh</text>')
    partes.append(
        f'<text x="16" y="258" font-family="{MONO}" font-size="11" fill="{t["mudo"]}" opacity="0">'
        f'<tspan fill="{t["luz"]}">❯</tspan> performance com IA'
        f'<animate attributeName="opacity" from="0" to="1" begin="{fim:.2f}s" dur="0.3s" fill="freeze"/></text>'
        f'<rect x="168" y="249" width="7" height="12" fill="{t["luz"]}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1s" '
        f'begin="{fim:.2f}s" repeatCount="indefinite"/></rect>')
    return f'<g transform="translate(8, 106)">{"".join(partes)}</g>'


def info(t):
    partes, y = [], 30
    for chave, valor in INFO:
        if chave == "titulo":
            if y > 30:
                y += 8
            resto = LARG_LINHA - len(valor) - 3
            partes.append(
                f'<text x="12" y="{y}" font-family="{MONO}" font-size="13" xml:space="preserve">'
                f'<tspan fill="{t["ponto"]}">─</tspan><tspan fill="{t["secao"]}"> {escape(valor)} </tspan>'
                f'<tspan fill="{t["ponto"]}">{"─" * resto}</tspan></text>')
        else:
            pontos = LARG_LINHA - len(chave) - len(valor) - 5
            partes.append(
                f'<text x="12" y="{y}" font-family="{MONO}" font-size="13" xml:space="preserve">'
                f'<tspan fill="{t["chave"]}">. {escape(chave)}: </tspan>'
                f'<tspan fill="{t["ponto"]}">{"." * pontos}</tspan>'
                f'<tspan fill="{t["tinta"]}"> {escape(valor)}</tspan></text>')
        y += 18
    return caixa(296, 106, 504, 280, t, "".join(partes))


def stack(t):
    partes = [f'<text x="24" y="32" font-family="{SANS}" font-size="11" font-weight="500" '
              f'fill="{t["mudo"]}" letter-spacing="2">[ STACK ]</text>',
              f'<rect x="24" y="50" width="576" height="2" fill="{t["borda"]}"/>'
              f'<rect x="24" y="50" width="0" height="2" fill="{t["luz"]}">'
              f'<animate attributeName="width" from="0" to="576" begin="0.3s" dur="1.6s" fill="freeze"/></rect>']
    for i, (nome, cor) in enumerate(STACK):
        x, y = 24 + (i % 4) * 148, 84 + (i // 4) * 30
        partes.append(f'<circle cx="{x + 6}" cy="{y - 4}" r="4" fill="{cor or t["tinta"]}"/>'
                      f'<text x="{x + 16}" y="{y}" font-family="{SANS}" font-size="12" '
                      f'fill="{t["tinta"]}">{nome}</text>')
    return caixa(8, 402, 624, 160, t, "".join(partes))


def cartao(t):
    w, h = 144, 160
    return (f'<g transform="translate(648, 402)">'
            f'<defs><linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{t["holo"][0]}"/><stop offset="0.5" stop-color="{t["holo"][1]}"/>'
            f'<stop offset="1" stop-color="{t["holo"][2]}"/></linearGradient>'
            f'<linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" '
            f'stop-opacity="0.35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="cc"><rect width="{w}" height="{h}" rx="10"/></clipPath></defs>'
            f'<rect width="{w}" height="{h}" rx="10" fill="{t["jan"]}" stroke="url(#holo)" stroke-width="1.5"/>'
            f'<path d="M44 104 L68 60 Q72 53 76 60 L100 104" fill="none" stroke="url(#holo)" stroke-width="9" '
            f'stroke-linecap="butt" stroke-linejoin="round"/>'
            f'<text x="{w / 2}" y="132" text-anchor="middle" font-family="{MONO}" font-size="10" '
            f'letter-spacing="4" fill="{t["mudo"]}">AIPE</text>'
            f'<text x="12" y="22" font-family="{MONO}" font-size="8" fill="{t["mudo"]}">BR</text>'
            f'<text x="{w - 12}" y="22" text-anchor="end" font-family="{MONO}" font-size="8" '
            f'fill="{t["mudo"]}">IA</text>'
            f'<g clip-path="url(#cc)"><rect x="-80" y="-20" width="60" height="{h + 40}" fill="url(#brilho)" '
            f'transform="skewX(-20)"><animate attributeName="x" values="-80;260;260" keyTimes="0;0.4;1" '
            f'dur="5s" repeatCount="indefinite"/></rect></g></g>')


def rodape(t):
    return caixa(0, 578, 800, 50, t,
                 f'<text x="24" y="30" font-family="{SANS}" font-size="11" font-weight="500" '
                 f'fill="{t["mudo"]}" letter-spacing="2">[ ARTIFICIAL INTELLIGENCE PERFORMANCE ECOSYSTEM ]</text>'
                 f'<text x="776" y="30" text-anchor="end" font-family="{MONO}" font-size="11" '
                 f'fill="{t["luz"]}">aipecorp.com</text>')


def svg(t):
    return ('<svg width="800" height="636" viewBox="0 0 800 636" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<style>text{user-select:none}</style>'
            f'<rect width="800" height="636" fill="{t["bg"]}"/>'
            f'{cabecalho(t)}{terminal(t)}{info(t)}{stack(t)}{cartao(t)}{rodape(t)}</svg>\n')


if __name__ == "__main__":
    for nome, tema in TEMAS.items():
        (AQUI / f"{nome}.svg").write_text(svg(tema))
        print(nome, len(svg(tema)), "bytes")

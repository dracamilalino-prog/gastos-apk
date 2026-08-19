"""Gera os ícones do launcher (legado, redondo e adaptativo) na paleta do app."""
from PIL import Image, ImageDraw, ImageFont
import os

RES = "/home/claude/gastos-apk/android/app/src/main/res"
BG = (23, 16, 32, 255)        # --bg  #171020
LILAC = (201, 167, 230, 255)  # --lilac
GOLD = (217, 180, 91, 255)    # --gold

DENS = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
SS = 8  # supersampling

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def carregar_fonte(tamanho):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, tamanho)
    return ImageFont.load_default()


def gradiente_vertical(tamanho, topo, base):
    """Faixa de gradiente do lilás ao dourado."""
    grad = Image.new("RGBA", (1, tamanho))
    for y in range(tamanho):
        t = y / max(tamanho - 1, 1)
        grad.putpixel((0, y), tuple(
            int(topo[i] * (1 - t) + base[i] * t) for i in range(4)))
    return grad.resize((tamanho, tamanho))


def desenhar_simbolo(tam, escala_fonte=0.52, dy=0.0):
    """Camada transparente com 'R$' em gradiente lilás→dourado."""
    camada = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    fonte = carregar_fonte(int(tam * escala_fonte))
    texto = "R$"
    cx, cy, dx2, dy2 = d.textbbox((0, 0), texto, font=fonte)
    x = (tam - (dx2 - cx)) / 2 - cx
    y = (tam - (dy2 - cy)) / 2 - cy + tam * dy
    d.text((x, y), texto, font=fonte, fill=(255, 255, 255, 255))

    grad = gradiente_vertical(tam, LILAC, GOLD)
    grad.putalpha(camada.split()[3])
    return grad


def icone_quadrado(px):
    """Ícone legado: fundo escuro com cantos arredondados + símbolo."""
    tam = px * SS
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, tam - 1, tam - 1], radius=int(tam * 0.22), fill=BG)
    d.rounded_rectangle([0, 0, tam - 1, tam - 1], radius=int(tam * 0.22),
                        outline=GOLD, width=max(int(tam * 0.02), SS))
    img.alpha_composite(desenhar_simbolo(tam, escala_fonte=0.44))
    return img.resize((px, px), Image.LANCZOS)


def icone_redondo(px):
    tam = px * SS
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=BG)
    d.ellipse([0, 0, tam - 1, tam - 1], outline=GOLD, width=max(int(tam * 0.025), SS))
    img.alpha_composite(desenhar_simbolo(tam, escala_fonte=0.40))
    return img.resize((px, px), Image.LANCZOS)


def icone_foreground(px):
    """Camada de frente do ícone adaptativo (só o símbolo, na zona segura)."""
    tam = px * SS
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    # o adaptativo corta as bordas: o símbolo fica menor e centralizado
    img.alpha_composite(desenhar_simbolo(tam, escala_fonte=0.34))
    return img.resize((px, px), Image.LANCZOS)


for dens, base in DENS.items():
    pasta = os.path.join(RES, f"mipmap-{dens}")
    os.makedirs(pasta, exist_ok=True)
    icone_quadrado(base).save(os.path.join(pasta, "ic_launcher.png"))
    icone_redondo(base).save(os.path.join(pasta, "ic_launcher_round.png"))
    # o foreground adaptativo é 108dp contra 48dp do ícone legado
    fg = int(base * 108 / 48)
    icone_foreground(fg).save(os.path.join(pasta, "ic_launcher_foreground.png"))
    print(f"mipmap-{dens}: {base}px + foreground {fg}px")

# fundo do ícone adaptativo na cor do app
with open(os.path.join(RES, "values", "ic_launcher_background.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            '    <color name="ic_launcher_background">#171020</color>\n</resources>\n')

# pré-visualização
icone_quadrado(432).save("/home/claude/gastos-apk/tools/preview_icone.png")
print("ok")

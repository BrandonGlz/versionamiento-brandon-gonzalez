from PIL import Image, ImageDraw, ImageFont

W, H = 1240, 1754
MAROON = "#6B1F3A"
GOLD = "#B08D57"
DARK = "#2B2B2B"
FONT_DIR = "/usr/share/fonts/julietaula-montserrat-fonts/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def centered(draw, text, y, f, fill):
    box = draw.textbbox((0, 0), text, font=f)
    x = (W - (box[2] - box[0])) / 2
    draw.text((x, y), text, font=f, fill=fill)
    return y + (box[3] - box[1])


canvas = Image.new("RGB", (W, H), "white")
fg = Image.open("docs/img/portada-fondo.png").convert("RGBA").resize((W, H), Image.LANCZOS)
canvas.paste(fg, (0, 0), fg)
draw = ImageDraw.Draw(canvas)

logo = Image.open("docs/img/utt-logo.png").convert("RGBA")
logo.thumbnail((820, 288), Image.LANCZOS)
canvas.paste(logo, ((W - logo.width) // 2, 110), logo)

draw.rectangle([(W - 420) // 2, 430, (W + 420) // 2, 436], fill=GOLD)

y = 500
y = centered(draw, "Actividad: Pruebas y liberación", y, font("Montserrat-Bold.otf", 58), MAROON) + 12
y = centered(draw, "del desarrollo WEB", y, font("Montserrat-Bold.otf", 58), MAROON) + 22
y = centered(draw, "Docker · GitHub · Render · Selenium", y, font("Montserrat-Medium.otf", 30), GOLD) + 70

y = centered(draw, "PRESENTADO POR", y, font("Montserrat-SemiBold.otf", 24), GOLD) + 10
y = centered(draw, "González González Brandon", y, font("Montserrat-Bold.otf", 40), MAROON) + 45

for label, value in [
    ("GRUPO", "9C"),
    ("MATERIA", "Desarrollo web profesional"),
    ("PROFESOR(A)", "Yakko Miguel Olivo Najera"),
]:
    y = centered(draw, label, y, font("Montserrat-SemiBold.otf", 22), GOLD) + 4
    y = centered(draw, value, y, font("Montserrat-Medium.otf", 30), DARK) + 32

y = centered(draw, "Tijuana, Baja California", y + 25, font("Montserrat-Regular.otf", 24), DARK) + 4
centered(draw, "03 de noviembre del 2026", y, font("Montserrat-Regular.otf", 24), DARK)

canvas.save("docs/img/portada.png")
print("Portada generada: docs/img/portada.png", canvas.size)

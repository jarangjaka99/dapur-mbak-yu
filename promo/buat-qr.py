#!/usr/bin/env python3
"""Membuat QR situs Dapur Mbak Yu + materi promosi siap cetak."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, os

BASE = os.path.expanduser("~/Documents/Dapur-Mbak-Yu")
OUT = os.path.join(BASE, "promo")
os.makedirs(OUT, exist_ok=True)

URL = "https://dapur-mbak-yu.vercel.app"
HIJAU = (14, 59, 44)
HIJAU2 = (23, 96, 63)
KREM = (251, 243, 228)
KUNING = (242, 184, 48)
MERAH = (200, 52, 31)
COKLAT = (74, 44, 23)
PUTIH = (255, 255, 255)

F_BALOO = os.path.join(OUT, "fonts", "Baloo2.ttf")
F_JKT = os.path.join(OUT, "fonts", "PlusJakarta.ttf")


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


# ---------- 1. QR mentah (galat koreksi H = tahan 30% tertutup) ----------
qr_raw = os.path.join(OUT, "_qr_raw.png")
subprocess.run([
    "qrencode", "-o", qr_raw, "-s", "20", "-l", "H", "-m", "4",
    "--foreground=0E3B2C", "--background=FFFFFF", URL
], check=True)
qr = Image.open(qr_raw).convert("RGB")
print("QR mentah:", qr.size)


def qr_with_logo(size, plate=0.20):
    """QR + logo di tengah di atas piringan putih."""
    q = qr.resize((size, size), Image.NEAREST)   # NEAREST: tepi modul tetap tajam
    logo = Image.open(os.path.join(BASE, "img", "logo-dmy.png")).convert("RGBA")
    lp = int(size * plate)
    logo = logo.resize((lp, lp), Image.LANCZOS)
    plate_px = int(lp * 1.16)
    layer = Image.new("RGBA", (plate_px, plate_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([0, 0, plate_px - 1, plate_px - 1], radius=int(plate_px * 0.2), fill=(255, 255, 255, 255))
    layer.paste(logo, ((plate_px - lp) // 2, (plate_px - lp) // 2), logo)
    q = q.convert("RGBA")
    q.paste(layer, ((size - plate_px) // 2, (size - plate_px) // 2), layer)
    return q.convert("RGB")


# ---------- 2. QR polos untuk dipakai di mana-mana ----------
qr_with_logo(1024).save(os.path.join(OUT, "qr-website.png"), quality=95)
subprocess.run(["qrencode", "-o", os.path.join(OUT, "qr-website.svg"), "-t", "SVG",
                "-l", "H", "-m", "4", "--foreground=0E3B2C", "--background=FFFFFF", URL], check=True)
print("QR polos + SVG dibuat")


def shadow_card(img, box, radius, blur=28, alpha=70, offset=12):
    """Bayangan lembut di belakang kotak."""
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0 + offset, x1, y1 + offset], radius=radius, fill=(43, 27, 16, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(sh)


# ---------- 3. Kartu A5 siap cetak (300 dpi) ----------
W, H = 1748, 2480
card = Image.new("RGBA", (W, H), KREM + (255,))
d = ImageDraw.Draw(card)

# hiasan sudut
d.ellipse([-260, -300, 460, 300], fill=(242, 184, 48, 45))
d.ellipse([W - 380, H - 520, W + 260, H + 120], fill=(200, 52, 31, 28))

# logo + nama
logo = Image.open(os.path.join(BASE, "img", "logo-dmy.png")).convert("RGBA")
ls = 360
logo = logo.resize((ls, ls), Image.LANCZOS)
card.alpha_composite(logo, ((W - ls) // 2, 120))

f_brand = font(F_BALOO, 118, 800)
f_tag = font(F_JKT, 40, 700)
f_head = font(F_BALOO, 118, 800)
f_sub = font(F_JKT, 46, 400)
f_url = font(F_JKT, 58, 800)
f_foot = font(F_JKT, 44, 700)

d.text((W // 2, 500), "Dapur Mbak Yu", font=f_brand, fill=HIJAU, anchor="ma")
d.text((W // 2, 640), "CITARASA OTENTIK  ·  BEKASI", font=f_tag, fill=COKLAT, anchor="ma")

# judul
d.text((W // 2, 745), "Scan & Pesan", font=f_head, fill=MERAH, anchor="ma")
d.text((W // 2, 885), "Menu, harga, dan pesanan langsung dari HP", font=f_sub, fill=(74, 60, 45), anchor="ma")

# kartu QR putih
qs = 940
qx, qy = (W - qs) // 2, 1010
box = [qx - 40, qy - 40, qx + qs + 40, qy + qs + 40]
shadow_card(card, box, 56)
d = ImageDraw.Draw(card)
d.rounded_rectangle(box, radius=56, fill=PUTIH + (255,), outline=(235, 216, 182, 255), width=3)
card.alpha_composite(qr_with_logo(qs).convert("RGBA"), (qx, qy))

# URL + ajakan
d.text((W // 2, qy + qs + 105), URL.replace("https://", ""), font=f_url, fill=HIJAU, anchor="ma")
d.text((W // 2, qy + qs + 180), "Kamera HP → arahkan ke QR → pesan via WhatsApp", font=f_sub, fill=(90, 74, 56), anchor="ma")

# pita bawah (konten wajib selesai di atas y = H-280)
d.rounded_rectangle([0, H - 260, W, H], radius=0, fill=HIJAU + (255,))
d.text((W // 2, H - 190), "HALAL  ·  HIGIENIS  ·  HOMEMADE  ·  TANPA PENGAWET",
       font=f_foot, fill=KREM, anchor="ma")
d.text((W // 2, H - 110), "Cabang Cikunir (Bekasi Selatan)  &  Cabang Harapan Jaya (Bekasi Utara)",
       font=font(F_JKT, 34, 400), fill=(200, 214, 205), anchor="ma")

card.convert("RGB").save(os.path.join(OUT, "qr-card-a5.png"), quality=94)
card.convert("RGB").save(os.path.join(OUT, "qr-card-a5.pdf"), "PDF", resolution=300.0)
print("Kartu A5 dibuat")

# ---------- 4. Stiker persegi (status WA / IG) ----------
S = 1400
st = Image.new("RGBA", (S, S), HIJAU + (255,))
ds = ImageDraw.Draw(st)
ds.ellipse([-200, -260, 520, 460], fill=(242, 184, 48, 38))
ds.ellipse([S - 420, S - 380, S + 260, S + 300], fill=(200, 52, 31, 60))

f1 = font(F_BALOO, 132, 800)
f2 = font(F_JKT, 44, 700)
f3 = font(F_JKT, 40, 400)
ds.text((S // 2, 110), "SCAN & PESAN", font=f1, fill=KREM, anchor="ma")
ds.text((S // 2, 262), "Sambel Pecel · Tahu Gejrot · Mie Jebew · Es Cendol", font=f2, fill=(240, 226, 200), anchor="ma")

qs2 = 800
qx2 = (S - qs2) // 2
qy2 = 340
shadow_card(st, [qx2 - 26, qy2 - 26, qx2 + qs2 + 26, qy2 + qs2 + 26], 44, blur=22, alpha=90)
ds = ImageDraw.Draw(st)
ds.rounded_rectangle([qx2 - 26, qy2 - 26, qx2 + qs2 + 26, qy2 + qs2 + 26], radius=44, fill=PUTIH + (255,))
st.alpha_composite(qr_with_logo(qs2).convert("RGBA"), (qx2, qy2))
ds.text((S // 2, qy2 + qs2 + 70), "dapur-mbak-yu.vercel.app", font=font(F_JKT, 50, 800), fill=KUNING, anchor="ma")
ds.text((S // 2, qy2 + qs2 + 140), "Halal · Higienis · Homemade", font=f3, fill=(205, 220, 210), anchor="ma")
st.convert("RGB").save(os.path.join(OUT, "qr-sticker.png"), quality=94)
print("Stiker dibuat")

os.remove(qr_raw)
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p):
        print(f"  {f:24s} {os.path.getsize(p)//1024:>5} KB")

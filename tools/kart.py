#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Micousta Reel sahne ureteci.

Her Reel 3 sahneden olusur:
  1) Kanca  - 3-6 kelimelik buyuk ifade (saha fotografi varsa uzerine)
  2) Icerik - 3-4 maddelik liste
  3) CTA    - kaydet + @micousta2026

Kullanim: iceri aktarip sahne(...) ve reel(...) cagir.
"""
import os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920

LACIVERT = (0x0E, 0x2A, 0x4C)
TURUNCU  = (0xED, 0x73, 0x2F)
KAGIT    = (0xF7, 0xF5, 0xF2)
MAVI     = (0xE8, 0xF0, 0xF7)
KREM     = (0xFD, 0xF0, 0xE6)
GRI      = (0x7C, 0x8A, 0x99)
BEYAZ    = (255, 255, 255)

FD = "/usr/share/fonts/opentype/inter/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

DISP_BOLD  = "InterDisplay-Bold.otf"
DISP_BLACK = "InterDisplay-Black.otf"
DISP_SEMI  = "InterDisplay-SemiBold.otf"
TXT_REG    = "Inter-Regular.otf"
TXT_MED    = "Inter-Medium.otf"
TXT_SEMI   = "Inter-SemiBold.otf"
TXT_BOLD   = "Inter-Bold.otf"


def sar(draw, text, font, max_w):
    """Metni max_w genisligine gore satirlara boler."""
    kelimeler = text.split()
    satirlar, cur = [], ""
    for k in kelimeler:
        dene = (cur + " " + k).strip()
        if draw.textlength(dene, font=font) <= max_w:
            cur = dene
        else:
            if cur:
                satirlar.append(cur)
            cur = k
    if cur:
        satirlar.append(cur)
    return satirlar


def yaz(draw, xy, text, font, fill, max_w, lh=1.18, ortala=False):
    x, y = xy
    for s in sar(draw, text, font, max_w):
        wpx = draw.textlength(s, font=font)
        sx = x + (max_w - wpx) / 2 if ortala else x
        draw.text((sx, y), s, font=font, fill=fill)
        y += font.size * lh
    return y


def foto_doldur(yol, w=W, h=H):
    """Fotografi 1080x1920'ye kirparak doldurur (cover)."""
    im = Image.open(yol).convert("RGB")
    iw, ih = im.size
    olcek = max(w / iw, h / ih)
    yeni = (int(iw * olcek + 0.5), int(ih * olcek + 0.5))
    im = im.resize(yeni, Image.LANCZOS)
    sol = (im.width - w) // 2
    ust = int((im.height - h) * 0.38)          # ust-orta kirpim, yuzler kalsin
    ust = max(0, min(ust, im.height - h))
    return im.crop((sol, ust, sol + w, ust + h))


def gradyan(im, ust_ogu=0.30, alt_ogu=0.92):
    """Alttan lacivere giden gradyan; metin okunakli olsun."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(H):
        t = y / H
        if t < 0.34:
            a = int(255 * ust_ogu * (1 - t / 0.34) + 255 * 0.18 * (t / 0.34))
        else:
            k = (t - 0.34) / 0.66
            a = int(255 * (0.18 + (alt_ogu - 0.18) * (k ** 1.5)))
        d.line([(0, y), (W, y)], fill=LACIVERT + (min(a, 255),))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")


def rozet(d, x, y, metin, bg=TURUNCU, fg=BEYAZ, fs=34):
    f = F(TXT_BOLD, fs)
    pw = d.textlength(metin, font=f)
    w, h = pw + 56, fs + 34
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + 28, y + 15), metin, font=f, fill=fg)
    return y + h


def altbilgi(d, renk=None, saydam=False):
    f = F(TXT_SEMI, 34)
    c = renk or (BEYAZ if saydam else GRI)
    d.text((72, H - 108), "@micousta2026", font=f, fill=c)
    w = d.textlength("micousta.com", font=f)
    d.text((W - 72 - w, H - 108), "micousta.com", font=f, fill=c)


# ---------------------------------------------------------------- sahneler

def sahne_kanca(cikis, kanca, etiket, foto=None, vurgu=None):
    """Sahne 1: buyuk kanca ifadesi."""
    if foto:
        im = gradyan(foto_doldur(foto))
        metin_rengi, alt_saydam = BEYAZ, True
    else:
        im = Image.new("RGB", (W, H), LACIVERT)
        metin_rengi, alt_saydam = BEYAZ, True
    d = ImageDraw.Draw(im)

    rozet(d, 72, 210, etiket)

    f = F(DISP_BLACK, 104)
    satirlar = sar(d, kanca, f, W - 144)
    yuk = len(satirlar) * f.size * 1.1
    y = H * 0.56 - yuk / 2
    for s in satirlar:
        # vurgu kelimesi turuncu
        if vurgu and vurgu.lower() in s.lower():
            i = s.lower().index(vurgu.lower())
            once, orta, sonra = s[:i], s[i:i + len(vurgu)], s[i + len(vurgu):]
            x = 72
            for parca, renk in ((once, metin_rengi), (orta, TURUNCU), (sonra, metin_rengi)):
                if parca:
                    d.text((x, y), parca, font=f, fill=renk)
                    x += d.textlength(parca, font=f)
        else:
            d.text((72, y), s, font=f, fill=metin_rengi)
        y += f.size * 1.1

    altbilgi(d, saydam=alt_saydam)
    im.save(cikis, quality=95)
    return cikis


def sahne_icerik(cikis, baslik, maddeler, foto=None):
    """Sahne 2: 3-4 maddelik liste."""
    if foto:
        im = foto_doldur(foto)
        im = im.filter(ImageFilter.GaussianBlur(26))
        ov = Image.new("RGBA", (W, H), LACIVERT + (232,))
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        kart_bg, bas_renk, md_renk, ac_renk = (255, 255, 255), BEYAZ, LACIVERT, GRI
    else:
        im = Image.new("RGB", (W, H), KAGIT)
        kart_bg, bas_renk, md_renk, ac_renk = BEYAZ, LACIVERT, LACIVERT, GRI
    d = ImageDraw.Draw(im)

    fb = F(DISP_BOLD, 66)
    y = yaz(d, (72, 250), baslik, fb, bas_renk, W - 144, lh=1.14)

    y += 70
    n = len(maddeler)
    kart_h = (H - 300 - y) / n
    fm = F(TXT_BOLD, 46)
    fa = F(TXT_REG, 38)
    for i, (md, ac) in enumerate(maddeler):
        ky = y + i * kart_h
        kh = kart_h - 30
        d.rounded_rectangle([72, ky, W - 72, ky + kh], radius=28, fill=kart_bg)
        d.rounded_rectangle([72, ky + 24, 84, ky + kh - 24], radius=6, fill=TURUNCU)
        ty = ky + (kh - (fm.size * 1.2 + fa.size * 1.25)) / 2
        ty = yaz(d, (124, ty), md, fm, md_renk, W - 220, lh=1.2)
        yaz(d, (124, ty + 8), ac, fa, ac_renk, W - 220, lh=1.25)

    altbilgi(d, renk=BEYAZ if foto else GRI)
    im.save(cikis, quality=95)
    return cikis


def sahne_cta(cikis, ust, alt, foto=None):
    """Sahne 3: kapanis + kaydet."""
    if foto:
        im = foto_doldur(foto).filter(ImageFilter.GaussianBlur(9))
        ov = Image.new("RGBA", (W, H), LACIVERT + (196,))
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    else:
        im = Image.new("RGB", (W, H), LACIVERT)
    d = ImageDraw.Draw(im)

    f1 = F(DISP_BOLD, 82)
    y = H * 0.40
    y = yaz(d, (72, y), ust, f1, BEYAZ, W - 144, lh=1.14)

    f2 = F(TXT_MED, 44)
    y = yaz(d, (72, y + 36), alt, f2, MAVI, W - 144, lh=1.35)

    rozet(d, 72, y + 56, "KAYDET, LAZIM OLUR", bg=TURUNCU, fs=40)

    altbilgi(d, saydam=True)
    im.save(cikis, quality=95)
    return cikis


# ---------------------------------------------------------------- video

def reel(cikis, kareler, sahne_sure=3.3, gecis=0.45):
    """Kareleri yavas zoom + xfade ile 1080x1920 Reel'e cevirir."""
    n = len(kareler)
    d = int(sahne_sure * 30)
    giris, filtre = [], []
    for i, k in enumerate(kareler):
        giris += ["-i", k]
        yon = 1 if i % 2 == 0 else -1
        if yon > 0:
            z = "min(zoom+0.00055,1.08)"
        else:
            z = "if(eq(on,1),1.08,max(zoom-0.00055,1.0))"
        filtre.append(
            f"[{i}:v]scale=1296:-2,"
            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={d}:s={W}x{H}:fps=30,format=yuv420p,setpts=PTS-STARTPTS[v{i}]"
        )
    son = "v0"
    for i in range(1, n):
        ofs = sahne_sure * i - gecis * i
        filtre.append(
            f"[{son}][v{i}]xfade=transition=fade:duration={gecis}:offset={ofs:.2f}[x{i}]"
        )
        son = f"x{i}"
    cmd = (["ffmpeg", "-y", "-v", "error"] + giris +
           ["-filter_complex", ";".join(filtre), "-map", f"[{son}]", "-an",
            "-r", "30", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", cikis])
    subprocess.run(cmd, check=True)
    return cikis

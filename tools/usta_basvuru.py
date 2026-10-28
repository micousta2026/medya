#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4 Kasim usta basvuru Reel'i - kurumsal dil."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import kart as K

OUT = "/home/claude/medya"
TMP = "/tmp/claude-0/usta"
os.makedirs(TMP, exist_ok=True)


def cta_basvuru(cikis, ust, alt, rozet_metni):
    im = Image.new("RGB", (K.W, K.H), K.LACIVERT)
    d = ImageDraw.Draw(im)
    f1 = K.F(K.DISP_BOLD, 82)
    y = K.H * 0.38
    y = K.yaz(d, (72, y), ust, f1, K.BEYAZ, K.W - 144, lh=1.14)
    f2 = K.F(K.TXT_MED, 44)
    y = K.yaz(d, (72, y + 36), alt, f2, K.MAVI, K.W - 144, lh=1.35)
    K.rozet(d, 72, y + 56, rozet_metni, bg=K.TURUNCU, fs=40)
    K.altbilgi(d, saydam=True)
    im.save(cikis, quality=95)
    return cikis


s1 = K.sahne_kanca(
    f"{TMP}/s1.jpg",
    "İşi siz aramayın, iş size atansın.",
    "USTA BAŞVURUSU",
    vurgu="atansın",
)

s2 = K.sahne_icerik(
    f"{TMP}/s2.jpg",
    "Süreç nasıl işliyor?",
    [
        ("1. Başvuru",
         "Uzmanlık alanınızı, hizmet verdiğiniz ilçeleri ve müsait günlerinizi bildirirsiniz."),
        ("2. Değerlendirme",
         "İş geçmişiniz ve referanslarınız incelenir. Uygun bulunan ustalar ağa dahil edilir."),
        ("3. İş ataması",
         "Talepler; uzmanlık alanı, konum ve müsaitlik durumuna göre eşleştirilir."),
        ("4. Ödeme",
         "Fiyat iş öncesinde netleşir. Ödeme, iş tamamlandıktan sonra yapılır."),
    ],
)

s3 = cta_basvuru(
    f"{TMP}/s3.jpg",
    "Kendi işinizi sürdürerek çalışın.",
    "Mevcut düzeninizi değiştirmenizi beklemiyoruz. Miço Usta, boş günlerinizi değerlendirebileceğiniz ek bir iş kanalıdır.",
    "BAŞVURU İÇİN DM",
)

K.reel(f"{OUT}/reels/ev5b-usta-basvuru.mp4", [s1, s2, s3])
for i, s in enumerate([s1, s2, s3], 1):
    Image.open(s).save(f"{OUT}/ig/ev5b-usta-basvuru-{i}.jpg", quality=92)
print("ok")

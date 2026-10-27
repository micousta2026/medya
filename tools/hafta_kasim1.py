#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3-10 Kasim 2026 haftasinin Reel'lerini uretir."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kart import (sahne_kanca, sahne_icerik, sahne_cta, reel,
                  F, W, H, LACIVERT, TURUNCU, BEYAZ, MAVI, GRI, KAGIT,
                  yaz, altbilgi, DISP_BOLD, DISP_BLACK, TXT_MED, TXT_REG)
from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAHA = os.path.join(KOK, "saha")
IG = os.path.join(KOK, "ig")
REELS = os.path.join(KOK, "reels")
TMP = "/tmp/claude-0/-home-claude-medya/5d2379d8-c45f-5e6e-9b63-230e08d81a38/scratchpad/kare"
os.makedirs(TMP, exist_ok=True)

P = [
 dict(ad="k1-halat", etiket="TEKNE BAKIMI", foto="bot-marina-01.jpg",
   kanca="Halatınız kışı çıkarır mı?", vurgu="kışı",
   baslik="Kış bağlamasında bakılacak dört şey",
   maddeler=[
     ("Sürtünme noktaları", "Halat en çok mapada ve küpeştede incelir. Kopmadan önce orada incelir."),
     ("Usturmaça yeri", "Fırtınada kayan usturmaça teknenizi iskeleye vurdurur."),
     ("Çapraz bağlama", "Tek halata güvenmeyin. Çapraz bağlama yükü böler."),
     ("Esneme payı", "Gelgitte ve dalgada halatın gerilecek yeri kalmalı."),
   ],
   cta_ust="Kışı çıkaracak bağlama yirmi dakikalık iştir.",
   cta_alt="İstanbul'daki marinalarda kış takibi yapıyoruz. Halat ve usturmaça her ziyarette kontrol listemizde."),

 dict(ad="k2-su-kacagi", etiket="EV BAKIMI", foto=None,
   kanca="Evinizde su kaçağı var mı?", vurgu="su kaçağı",
   baslik="Sayaçla on dakikalık kaçak testi",
   maddeler=[
     ("Her şeyi kapatın", "Musluklar, çamaşır, bulaşık, rezervuar. Hiçbir şey akmasın."),
     ("Sayacı okuyun", "Rakamları ve ibreyi not edin ya da fotoğraflayın."),
     ("On dakika bekleyin", "Bu sürede evde hiç su kullanılmayacak."),
     ("Tekrar okuyun", "Rakam değiştiyse ya da ibre döndüyse kaçak vardır."),
   ],
   cta_ust="Kaçak su, faturaya yansımadan önce duvarı bozar.",
   cta_alt="Tuzla'da tesisat ve su kaçağı tespiti yapıyoruz. Kaçağı kırmadan bulmak işin asıl kısmı."),

 dict(ad="k3-makine-dairesi", etiket="TEKNE BAKIMI", foto="makine-dairesi-01.jpg",
   kanca="Fişte duran tekne güvende değildir", vurgu="güvende değildir",
   baslik="Kış boyunca makine dairesinde olanlar",
   maddeler=[
     ("Şarj cihazı durmaz", "Akü tipine göre ayarlı değilse aküyü kaynatır."),
     ("Nem yoğuşur", "Soğuk metalde su birikir, korozyon oradan başlar."),
     ("Sintine sessizce dolar", "Pompa kuru çalışıp yanar, kimse duymaz."),
     ("Hortum sertleşir", "Soğukta yorulan hortum ve kelepçe çatlar."),
   ],
   cta_ust="Makine dairesine kışın da bakan biri olmalı.",
   cta_alt="İstanbul'daki marinalarda düzenli ziyaret ediyoruz. Her kontrol fotoğraflı olarak teknenizin dijital karnesine işleniyor."),

 dict(ad="k4-kacak-akim", etiket="EV BAKIMI", foto=None,
   kanca="Panonuzda hayat kurtaran bir düğme var", vurgu="hayat kurtaran",
   baslik="Kaçak akım rölesi ve test butonu",
   maddeler=[
     ("Ne yapar", "Elektrik size geçmeden akımı keser. Milisaniyeler içinde."),
     ("Test butonu", "Üzerindeki T harfli düğme. Basınca şalter inmeli."),
     ("Ne sıklıkta", "Ayda bir. On saniyelik iş."),
     ("İnmiyorsa", "Röle görevini yapmıyordur. Değişmesi gerekir, ertelemeyin."),
   ],
   cta_ust="Ayda bir, on saniye.",
   cta_alt="Panonuzda kaçak akım rölesi yoksa ya da test butonu şalteri indirmiyorsa bakalım. Tuzla'da elektrik ve pano işleri yapıyoruz."),

 dict(ad="k5-soru", etiket="SORU", foto=None,
   kanca="Bu kış neyin bakımını erteliyorsunuz?", vurgu="erteliyorsunuz",
   baslik="Dürüst olalım — hangisi sizde duruyor?",
   maddeler=[
     ("Kombi bakımı", "Geçen yıldan beri yaptıracağım dediğiniz."),
     ("Teknenin kış hazırlığı", "Marinaya bir türlü inemediniz."),
     ("Şu damlayan musluk", "Aylar oldu, hâlâ damlıyor."),
     ("Panodaki eski sigorta", "Ara ara atıyor, idare ediyorsunuz."),
   ],
   cta_ust="Hangisi? Yoruma yazın.",
   cta_alt="Kimseyi ayıplamıyoruz, herkes erteliyor. En çok hangisi yazılırsa önümüzdeki hafta onu anlatacağız."),

 dict(ad="k6-nem-kuf", etiket="EV BAKIMI", foto=None,
   kanca="Camlar terliyorsa duvar da terliyordur", vurgu="duvar da",
   baslik="Kışın nem ve küf neden başlar",
   maddeler=[
     ("Nem nereden gelir", "Duş, çamaşır, yemek, nefes. Ev gün boyu nem üretir."),
     ("Neden camda görünür", "Cam evin en soğuk yüzeyidir. Nem önce orada yoğuşur."),
     ("Asıl risk", "Dış duvarın soğuk köşeleri. Küf orada, görünmeden başlar."),
     ("Çözüm ısıtmak değil", "Günde iki kez beş dakika karşılıklı havalandırma."),
   ],
   cta_ust="Küf bir temizlik işi değil, bir nem işidir.",
   cta_alt="Havalandırma, baca ve nem kaynağı kontrolü yapıyoruz. Tuzla'da evin bakımına bakıyoruz."),

 dict(ad="k7-salter", etiket="TEKNE BAKIMI", foto="konsol-kontrol-01.jpg",
   kanca="Hangi şalter açık kalmalı?", vurgu="açık kalmalı",
   baslik="Tekneyi kışa bırakırken pano düzeni",
   maddeler=[
     ("Açık kalacak", "Sintine pompası ve şamandırası. Hayati olan tek devre budur."),
     ("Kapanacak", "Buzdolabı, su pompası, inverter, aydınlatma."),
     ("Ana şalter", "Sintine ayrı beslenmiyorsa ana şalteri kapatamazsınız."),
     ("Şarj cihazı", "Açık kalacaksa akü tipine doğru ayarlanmış olmalı."),
   ],
   cta_ust="Yanlış kapatılan bir şalter, baharda su almış bir tekne demek.",
   cta_alt="Kış takibinde pano düzenini biz kuruyor, her ziyarette kontrol ediyoruz. İstanbul marinaları."),
]


def onuncu_kasim(ad):
    """10 Kasim icin sade, satis icermeyen uc sahne."""
    kareler = []
    # 1
    im = Image.new("RGB", (W, H), LACIVERT); d = ImageDraw.Draw(im)
    f = F(TXT_MED, 46)
    d.text((72, H * 0.40), "10 Kasım 1938", font=f, fill=MAVI)
    fb = F(DISP_BLACK, 170)
    d.text((72, H * 0.40 + 86), "09:05", font=fb, fill=BEYAZ)
    altbilgi(d, saydam=True)
    k = os.path.join(TMP, f"{ad}-1.jpg"); im.save(k, quality=95); kareler.append(k)
    # 2
    im = Image.new("RGB", (W, H), LACIVERT); d = ImageDraw.Draw(im)
    fb = F(DISP_BOLD, 88)
    yaz(d, (72, H * 0.33), "Aziz Atatürk'ü saygı, sevgi ve özlemle anıyoruz.",
        fb, BEYAZ, W - 144, lh=1.16)
    altbilgi(d, saydam=True)
    k = os.path.join(TMP, f"{ad}-2.jpg"); im.save(k, quality=95); kareler.append(k)
    # 3
    im = Image.new("RGB", (W, H), LACIVERT); d = ImageDraw.Draw(im)
    f = F(TXT_REG, 50)
    yaz(d, (72, H * 0.42), "Denizde ve karada, elinin emeğiyle çalışan herkesin anısına.",
        f, MAVI, W - 144, lh=1.4)
    d.rounded_rectangle([72, H * 0.42 - 40, 84, H * 0.42 - 10], radius=6, fill=TURUNCU)
    altbilgi(d, saydam=True)
    k = os.path.join(TMP, f"{ad}-3.jpg"); im.save(k, quality=95); kareler.append(k)
    return kareler


def main():
    for p in P:
        foto = os.path.join(SAHA, p["foto"]) if p["foto"] else None
        k1 = sahne_kanca(os.path.join(TMP, p["ad"] + "-1.jpg"),
                         p["kanca"], p["etiket"], foto, p["vurgu"])
        k2 = sahne_icerik(os.path.join(TMP, p["ad"] + "-2.jpg"),
                          p["baslik"], p["maddeler"], foto)
        k3 = sahne_cta(os.path.join(TMP, p["ad"] + "-3.jpg"),
                       p["cta_ust"], p["cta_alt"], foto)
        # kapak karesi arsive
        Image.open(k1).resize((1080, 1350), Image.LANCZOS).save(
            os.path.join(IG, p["ad"] + ".jpg"), quality=92)
        reel(os.path.join(REELS, p["ad"] + ".mp4"), [k1, k2, k3])
        print("bitti:", p["ad"])

    kareler = onuncu_kasim("k8-10kasim")
    Image.open(kareler[1]).resize((1080, 1350), Image.LANCZOS).save(
        os.path.join(IG, "k8-10kasim.jpg"), quality=92)
    reel(os.path.join(REELS, "k8-10kasim.mp4"), kareler, sahne_sure=3.6, gecis=0.7)
    print("bitti: k8-10kasim")


if __name__ == "__main__":
    main()

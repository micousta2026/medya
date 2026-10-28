#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuzla ev ustasi odagina gecis: tekne gonderilerinin yerine gelen Reel'ler.
30 Ekim - 9 Kasim 2026.  2 usta ilani + 5 musteri icerigi.

Branslar (Burcu'nun verdigi kesin liste):
  tesisat / su ve pompa sistemleri / elektrik / kombi / klima /
  boya / mobilya montaji
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kart import sahne_kanca, sahne_icerik, sahne_cta, reel
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IG = os.path.join(KOK, "ig")
REELS = os.path.join(KOK, "reels")
TMP = ("/tmp/claude-0/-home-claude-medya/"
       "5d2379d8-c45f-5e6e-9b63-230e08d81a38/scratchpad/kare2")
os.makedirs(TMP, exist_ok=True)

P = [
 # --- 30 Ekim : musteri ---
 dict(ad="ev1-kombi", etiket="KOMBİ BAKIMI",
   kanca="Kombiniz bu kışı çıkarır mı?", vurgu="bu kışı",
   baslik="Kombi bakımında gerçekte ne yapılıyor",
   maddeler=[
     ("Eşanjör temizliği", "Kireç tutan eşanjör ısıyı suya veremez. Gaz boşa yanar."),
     ("Yanma ayarı", "Baca gazı ölçülür, hava-gaz oranı ayarlanır. Verim buradan çıkar."),
     ("Emniyet kontrolü", "Gaz kaçağı, baca tahliyesi, emniyet ventili."),
     ("Basınç ve genleşme", "Sürekli su eklettiren kombinin sebebi genelde genleşme tankı."),
   ],
   cta_ust="Kombi arızası soğukta çıkar. Servis de o zaman dolar.",
   cta_alt="Tuzla'da kombi ve petek bakımı yapıyoruz. Yapılan her iş fotoğrafıyla evinizin bakım karnesine yazılıyor."),

 # --- 31 Ekim : usta ilani 1 ---
 dict(ad="ev2-usta-ilan", etiket="USTA ARANIYOR",
   kanca="Tuzla'da usta arıyoruz", vurgu="Tuzla'da",
   baslik="Hangi branşlarda arıyoruz",
   maddeler=[
     ("Tesisat ve pompa", "Su kaçağı, tesisat, hidrofor, drenaj ve atıksu pompaları."),
     ("Elektrik", "Pano, sigorta, kaçak akım rölesi, priz, aydınlatma."),
     ("Kombi, petek, klima", "Bakım, arıza, montaj, gaz."),
     ("Boya ve mobilya montajı", "İç cephe boya, dolap ve raf montajı, küçük tadilat."),
   ],
   cta_ust="CV göndermeyin. Ne iş yaptığınızı yazın.",
   cta_alt="Çalışma şeklini konuşarak belirliyoruz: kadrolu da olur, iş başı da, kendi işini sürdüren ustayla ortaklık da. Bölge sadece Tuzla."),

 # --- 2 Kasim : musteri, guven ---
 dict(ad="ev3-nasil", etiket="NASIL ÇALIŞIYORUZ",
   kanca="Usta ne zaman gelecek, belli değil", vurgu="belli değil",
   baslik="Bildiğiniz usta deneyimini değiştiriyoruz",
   maddeler=[
     ("Saat veriyoruz", "\"Öğleden sonra gelirim\" değil. Gün ve saat aralığı belli."),
     ("Aynı ekip geliyor", "Evinize her seferinde yeni bir yabancı almıyorsunuz."),
     ("İş bitince yazılı", "Ne yapıldı, hangi parça değişti — fotoğrafıyla."),
     ("Arkasında duruyoruz", "Yaptığımız iş tekrar bozulursa tekrar geliyoruz."),
   ],
   cta_ust="Zor olan iş değil. Güvenilir birini bulmak.",
   cta_alt="Tuzla'da tesisat, elektrik, kombi, klima, boya, mobilya montajı ve pompa sistemleri. Randevu için DM."),

 # --- 3 Kasim : musteri, POMPA (yeni baslik) ---
 dict(ad="ev4-pompa", etiket="SU VE POMPA SİSTEMLERİ",
   kanca="Her yağmurda bodrum su alıyorsa", vurgu="bodrum su alıyorsa",
   baslik="Hangi pompa, nerede işe yarar",
   maddeler=[
     ("Drenaj pompası", "Bodrum, otopark, asansör kuyusu. Biriken temiz suyu dışarı basar."),
     ("Atıksu pompası", "Katı parça geçirir. Kanalizasyon kotunun altındaki tuvalet ve çamaşırhane."),
     ("Hidrofor", "Üst katta su akmıyorsa sorun boruda değil basınçtadır."),
     ("Santrifüj pompa", "Sürekli ve yüksek debi. Site, iş yeri, sanayi tesisi."),
   ],
   cta_ust="Satışını da yapıyoruz, montajını da, bakımını da.",
   cta_alt="Tuzla'da hidrofor, drenaj, atıksu ve santrifüj pompa. Site ve apartman yönetimleriyle de çalışıyoruz."),

 # --- 5 Kasim : usta ilani 2 ---
 dict(ad="ev5-usta-ortak", etiket="USTA ARANIYOR",
   kanca="Kendi işinizi bırakmanızı istemiyoruz", vurgu="bırakmanızı",
   baslik="Kendi işini yapan ustalara teklifimiz",
   maddeler=[
     ("İşinizi sürdürün", "Kendi müşterinize bakmaya devam edin."),
     ("Boş gününüz dolsun", "İşin seyreldiği günlerde size iş yönlendirelim."),
     ("Müşteri bulma bizde", "Reklam, telefon trafiği, fiyat pazarlığı bizim işimiz."),
     ("Bölge dar kalsın", "Sadece Tuzla. Gün boyu trafikte dolaşmayın."),
   ],
   cta_ust="Yanımızda değil, birlikte.",
   cta_alt="Tesisat, pompa, elektrik, kombi, klima, boya, mobilya montajı. Ne iş yaptığınızı yazın, konuşalım."),

 # --- 7 Kasim : musteri, etkilesim ---
 dict(ad="ev6-soru", etiket="SORU",
   kanca="Bu kış evde neyi erteliyorsunuz?", vurgu="erteliyorsunuz",
   baslik="Dürüst olalım — hangisi sizde duruyor?",
   maddeler=[
     ("Kombi bakımı", "Geçen yıldan beri yaptıracağım dediğiniz."),
     ("Şu damlayan musluk", "Aylar oldu, hâlâ damlıyor."),
     ("Panodaki eski sigorta", "Ara ara atıyor, idare ediyorsunuz."),
     ("Duvardaki o leke", "Büyüyor mu, emin değilsiniz."),
   ],
   cta_ust="Hangisi? Yoruma tek kelime yazın.",
   cta_alt="En çok hangisi yazılırsa önümüzdeki hafta tam olarak onu anlatacağız. Nasıl yapılır, kendiniz yapabilir misiniz."),

 # --- 9 Kasim : musteri, hizmet vitrini ---
 dict(ad="ev7-hizmetler", etiket="HİZMETLERİMİZ",
   kanca="Tuzla'da ne yapıyoruz?", vurgu="ne yapıyoruz",
   baslik="Evde ve binada baktığımız işler",
   maddeler=[
     ("Tesisat ve pompa", "Su kaçağı, tesisat, hidrofor, drenaj ve atıksu pompaları."),
     ("Elektrik ve kombi", "Pano, sigorta, aydınlatma. Kombi ve petek bakımı, arıza."),
     ("Klima", "Montaj, bakım, gaz, sökme-takma."),
     ("Boya ve mobilya montajı", "İç cephe boya, dolap ve raf montajı, küçük tadilat."),
   ],
   cta_ust="Tek ekip, yedi branş.",
   cta_alt="Çoğu ev işi tek branşta bitmiyor. Hepsi bizdeyse sorumluluk da bizde. Tuzla'da hizmet veriyoruz."),
]


def main():
    for p in P:
        k1 = sahne_kanca(os.path.join(TMP, p["ad"] + "-1.jpg"),
                         p["kanca"], p["etiket"], None, p["vurgu"])
        k2 = sahne_icerik(os.path.join(TMP, p["ad"] + "-2.jpg"),
                          p["baslik"], p["maddeler"], None)
        k3 = sahne_cta(os.path.join(TMP, p["ad"] + "-3.jpg"),
                       p["cta_ust"], p["cta_alt"], None)
        Image.open(k1).resize((1080, 1350), Image.LANCZOS).save(
            os.path.join(IG, p["ad"] + ".jpg"), quality=92)
        reel(os.path.join(REELS, p["ad"] + ".mp4"), [k1, k2, k3])
        print("bitti:", p["ad"])


if __name__ == "__main__":
    main()

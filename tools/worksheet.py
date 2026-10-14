#!/usr/bin/env python3
"""Tablet + kalem için çalışma kağıdı PDF'i üretir. Kullanım: python3 tools/worksheet.py day01"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("R", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("B", F + "DejaVuSans-Bold.ttf"))
W, H = A4
M = 45


class Sheet:
    def __init__(self, path, title):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle(title)
        self.y = H - M
        self.title(title)

    def need(self, h):
        if self.y - h < M:
            self.c.showPage()
            self.y = H - M

    def title(self, t):
        self.c.setFont("B", 18)
        self.c.drawString(M, self.y - 14, t)
        self.y -= 34

    def h(self, t):
        self.need(40)
        self.y -= 8
        self.c.setFont("B", 13)
        self.c.drawString(M, self.y - 12, t)
        self.y -= 26

    def p(self, t, size=11, font="R", gap=16):
        self.need(gap)
        self.c.setFont(font, size)
        self.c.drawString(M, self.y - size, t)
        self.y -= gap

    def table(self, rows):
        self.need(len(rows) * 24 + 10)
        for i, r in enumerate(rows):
            self.c.setFont("B" if i == 0 else "R", 11)
            x = M
            for cell, w in zip(r, (110, 90, 300)):
                self.c.drawString(x + 4, self.y - 16, cell)
                x += w
            self.c.line(M, self.y - 22, M + 500, self.y - 22)
            self.y -= 24
        self.y -= 6

    def write(self, prompt, lines=1):
        """Soru + kalemle yazılacak çizgili alan."""
        self.need(22 + lines * 34)
        self.p(prompt, gap=22)
        for _ in range(lines):
            self.c.setStrokeGray(0.7)
            self.c.line(M + 10, self.y - 24, W - M, self.y - 24)
            self.c.setStrokeGray(0)
            self.y -= 34

    def save(self):
        self.c.save()


def day01(path):
    s = Sheet(path, "Day 1 - to be (OffWeGo Modül 1)")
    s.p("Chapter 1 · Mini ders (20 dk) · Kaynak: OffWeGo English, Modül 1 (PDF s.11-15)", 10)
    s.h("1. Önce kitaptan oku (8 dk): 1.1, 1.2, 1.3 ve 1.9 'Mistake Hospital'")
    s.p("Aşağısı özet. Asıl anlatım kitapta; kutulardaki ⚠ uyarılara özellikle bak.", 10)
    s.h("2. Özet")
    s.p("İngilizce cümle fiilsiz kalmaz: 'Yorgunum' -> I am tired. (I tired ✗)")
    s.table([("Özne", "to be", "Kısa / olumsuz"),
             ("I", "am", "I'm / I'm not   (I amn't ✗)"),
             ("you / we / they", "are", "you're / aren't"),
             ("he / she / it", "is", "she's / isn't")])
    s.p("Hava, saat, mesafe için özne it: It is raining. It's five o'clock.  (Is raining ✗)")
    s.p("Yaş be ile: I'm twenty.  (I have twenty years ✗)")
    s.p("Soru: be başa gider. Are you a student?   Kısa cevap kısaltılmaz: Yes, I am.  (Yes, I'm ✗)")
    s.p("Yakın: this / these.   Uzak: that / those.   This is my phone. Those are your keys.")
    s.h("A. Çekimle: am / is / are / isn't / aren't")
    for q in ["I ____ a teacher.", "She ____ tired.", "They ____ students.", "It ____ cold today.",
              "We ____ from Bursa.", "He ____ not late.  (kısa)", "You ____ not ready.  (kısa)"]:
        s.p(q, 13, gap=28)
    s.h("B. Aynı cümleyi soru ve olumsuz yap")
    s.write("They are teachers.   ?  ", 1)
    s.write("They are teachers.   -  ", 1)
    s.write("She is happy.   ?  ", 1)
    s.write("She is happy.   -  ", 1)
    s.write("It is raining.   ?  ", 1)
    s.write("It is raining.   -  ", 1)
    s.h("C. Hatayı bul ve düzelt")
    s.write("1. I have twenty years.")
    s.write("2. She very tall.")
    s.write("3. Are you tired? - Yes, I'm.")
    s.write("4. I amn't ready.")
    s.write("5. These is my keys.")
    s.h("D. Çevir (Türkçe -> İngilizce)")
    s.write("1) Ben Niğdeliyim. Annem öğretmen, babam mühendis.", 2)
    s.write("2) Bunlar benim kitaplarım. Şunlar kardeşimin kitapları.", 2)
    s.write("3) Hava bugün çok soğuk ve yağmurlu.", 2)
    s.h("E. Kendin: tanışma diyaloğu (6 satır)")
    s.p("Kitaptaki 1.7 diyaloğu örnek al. İsim, nereden, yaş, öğrenci misin? Kapanışla bitir.", 10)
    for i in range(1, 7):
        s.write(f"{i})", 1)
    s.save()


def day01_reading(path):
    s = Sheet(path, "Day 1 - Okuma + kelime: A Normal Monday")
    s.p("Chapter 1 · Okuma + kelime (25 dk) · Kaynak: Oxford 3000 Okuma Serisi, Okuma 1 (PDF s.5)", 10)
    s.h("1. Oku (8 dk)")
    s.p("Oxford 3000 PDF'inde 'A Normal Monday' hikayesini oku. Önce Türkçe çeviriye bakma.")
    s.p("2 kez oku: ilkinde genel anlam, ikincisinde alttaki 8 kelimenin altını çiz.")
    s.h("2. Bugünün 8 kelimesi")
    rows = [("Kelime", "Türkçe", "Örnek"),
            ("always", "her zaman", "I am always late on Monday."),
            ("usually", "genellikle", "She usually drinks tea."),
            ("sometimes", "bazen", "Sometimes we walk home."),
            ("prepare", "hazırlamak", "He prepares breakfast."),
            ("check", "kontrol etmek", "Check your bag."),
            ("free", "boş, serbest", "I have a free hour."),
            ("cheap", "ucuz", "The cafe is cheap."),
            ("interesting", "ilginç", "It is an interesting book.")]
    s.need(len(rows) * 24 + 10)
    for i, r in enumerate(rows):
        s.c.setFont("B" if i == 0 else "R", 11)
        x = M
        for cell, w in zip(r, (110, 110, 280)):
            s.c.drawString(x + 4, s.y - 16, cell)
            x += w
        s.c.line(M, s.y - 22, M + 500, s.y - 22)
        s.y -= 24
    s.y -= 6
    s.p("Not: always / usually / sometimes sıklık zarfı. Fiilden önce gelir: He usually wakes up at six.", 10)
    s.h("3. Anlama soruları (kısa İngilizce cevap)")
    s.write("1) What time does Sam usually wake up?")
    s.write("2) Where does he go sometimes?")
    s.write("3) Is the cafe expensive?  (Yes/No + kısa cümle)")
    s.write("4) How long does he train?")
    s.h("4. Boşluğu doldur (yukarıdaki 8 kelimeden)")
    for q in ["I ______ wake up at seven. It is my routine, every day.",
              "This restaurant is not expensive. It is ______.",
              "I have two ______ hours today. Let's meet.",
              "Please ______ the door before you leave."]:
        s.p(q, 12, gap=30)
    s.h("5. Kendi cümlelerin (aktif kullanım)")
    s.p("Kendi Pazartesi'n hakkında 3 cümle. En az 3 farklı yeni kelime kullan.", 10)
    s.write("1)")
    s.write("2)")
    s.write("3)")
    s.save()


if __name__ == "__main__":
    name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f"worksheets/{name}.pdf"
    globals()[name](out)
    print(out)

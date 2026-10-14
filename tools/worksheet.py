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
    s = Sheet(path, "Day 1 - to be (am / is / are)")
    s.p("Chapter 1 · Solid Basics · Mini ders (20 dk)", 10)
    s.h("1. Kural")
    s.p("Türkçede 'ben öğrenciyim' derken ayrı fiil yok. İngilizcede cümlede mutlaka to be olmalı.")
    s.table([("Özne", "to be", "Örnek"),
             ("I", "am", "I am a teacher."),
             ("he / she / it", "is", "She is from Ankara."),
             ("you / we / they", "are", "We are friends.")])
    s.p("Olumsuz: not ekle.  I am not tired.  He is not (isn't) here.  They aren't at home.")
    s.p("Soru: fiil başa geçer.  Are you a student?  Is she at home?")
    s.p("Kısa cevap: Yes, I am. / No, she isn't.")
    s.h("2. Alıştırma: am / is / are yaz")
    for q in ["I ____ from Turkey.", "My brother ____ 25 years old.", "We ____ at work.",
              "____ you tired?  (soru)", "She ____ not my teacher.  (olumsuz)",
              "They ____ in Istanbul.", "It ____ a big city."]:
        s.p(q, 13, gap=30)
    s.h("3. Olumsuz ve soru yap")
    s.write("He is a doctor.  ->  Olumsuz:")
    s.write("You are late.  ->  Soru:")
    s.write("They are happy.  ->  Soru:")
    s.h("4. Kendini yaz (to be ile 3 cümle)")
    s.p("Adın, mesleğin, nerelisin. Örnek: I am Ali. I am an engineer. I am from Izmir.", 10)
    s.write("1)", 1)
    s.write("2)", 1)
    s.write("3)", 1)
    s.save()


if __name__ == "__main__":
    name = sys.argv[1]
    globals()[name](f"worksheets/{name}_to-be.pdf")
    print(f"worksheets/{name}_to-be.pdf")

#!/usr/bin/env python3
"""Tablet + kalem için çalışma kağıdı PDF'i üretir. Kullanım: python3 tools/worksheet.py day01"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("R", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("B", F + "DejaVuSans-Bold.ttf"))
W, H = A4
M = 45
# OffWeGo renk mantığı: A1 altın, A2 kırmızı (crimson), B1 mor, B2 lacivert. Şimdilik A2.
ACCENT = (0.69, 0.10, 0.20)      # crimson (A2)
SOFT = (0.99, 0.93, 0.94)        # açık kırmızımsı zemin
GLOSS = (0.31, 0.40, 0.52)       # gri-mavi açıklama
INK = (0.12, 0.12, 0.14)


class Sheet:
    def __init__(self, path, title):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle(title)
        self.y = H - M
        self.title(title)

    def newpage(self):
        self.c.showPage()
        self.y = H - M

    def need(self, h):
        if self.y - h < M:
            self.c.showPage()
            self.y = H - M

    def title(self, t):
        self.c.setFillColorRGB(*ACCENT)
        self.c.rect(0, H - 58, W, 58, stroke=0, fill=1)
        self.c.setFillColorRGB(1, 1, 1)
        self.c.setFont("B", 18)
        self.c.drawString(M, H - 38, t)
        self.c.setFillColorRGB(*INK)
        self.y = H - 58 - M + 14

    def h(self, t, keep=170):
        self.need(keep)
        self.y -= 8
        self.c.setFillColorRGB(*SOFT)
        self.c.roundRect(M - 6, self.y - 20, W - 2 * M + 12, 24, 5, stroke=0, fill=1)
        self.c.setFillColorRGB(*ACCENT)
        self.c.rect(M - 6, self.y - 20, 4, 24, stroke=0, fill=1)
        self.c.setFont("B", 12.5)
        self.c.drawString(M + 6, self.y - 13, t)
        self.c.setFillColorRGB(*INK)
        self.y -= 32

    def p(self, t, size=11, font="R", gap=16, color=INK):
        self.need(gap)
        self.c.setFillColorRGB(*color)
        self.c.setFont(font, size)
        self.c.drawString(M, self.y - size, t)
        self.c.setFillColorRGB(*INK)
        self.y -= gap

    def para(self, t, size=11, font="R", color=INK, leading=None, indent=0, gap=6):
        """Satır kaydırmalı paragraf."""
        leading = leading or size + 5
        for ln in simpleSplit(t, font, size, W - 2 * M - indent):
            self.need(leading)
            self.c.setFillColorRGB(*color)
            self.c.setFont(font, size)
            self.c.drawString(M + indent, self.y - size, ln)
            self.y -= leading
        self.c.setFillColorRGB(*INK)
        self.y -= gap

    def todo(self, text, minutes=None):
        """'NE YAPACAKSIN' kutusu: adımın net talimatı."""
        lines = []
        for item in text:
            lines += simpleSplit(item, "R", 11, W - 2 * M - 30)
        h = len(lines) * 16 + 34
        self.need(h + 8)
        self.c.setFillColorRGB(1, 0.97, 0.85)
        self.c.setStrokeColorRGB(0.9, 0.7, 0.2)
        self.c.roundRect(M - 6, self.y - h, W - 2 * M + 12, h, 6, stroke=1, fill=1)
        self.c.setFillColorRGB(0.55, 0.35, 0.0)
        self.c.setFont("B", 11)
        self.c.drawString(M + 4, self.y - 18, "NE YAPACAKSIN" + (f"  ({minutes} dk)" if minutes else ""))
        self.c.setFillColorRGB(*INK)
        self.c.setFont("R", 11)
        yy = self.y - 36
        for ln in lines:
            self.c.drawString(M + 8, yy, ln)
            yy -= 16
        self.c.setStrokeGray(0)
        self.y -= h + 12

    def table(self, rows):
        self.need(len(rows) * 24 + 10)
        for i, r in enumerate(rows):
            if i == 0:
                self.c.setFillColorRGB(*ACCENT)
                self.c.rect(M, self.y - 22, 500, 24, stroke=0, fill=1)
            x = M
            for j, (cell, w) in enumerate(zip(r, (110, 90, 300))):
                if i == 0:
                    self.c.setFillColorRGB(1, 1, 1)
                    self.c.setFont("B", 11)
                else:
                    self.c.setFillColorRGB(*(ACCENT if j == 1 else INK))
                    self.c.setFont("B" if j == 1 else "R", 11)
                self.c.drawString(x + 4, self.y - 16, cell)
                x += w
            self.c.setStrokeColorRGB(0.85, 0.85, 0.88)
            self.c.line(M, self.y - 22, M + 500, self.y - 22)
            self.c.setStrokeGray(0)
            self.c.setFillColorRGB(*INK)
            self.y -= 24
        self.y -= 6

    def write(self, prompt, lines=1):
        """Soru + kalemle yazılacak çizgili alan."""
        self.need(22 + lines * 34)
        self.p(prompt, gap=22)
        for _ in range(lines):
            self.c.setStrokeColorRGB(0.72, 0.78, 0.88)
            self.c.line(M + 10, self.y - 24, W - M, self.y - 24)
            self.c.setStrokeGray(0)
            self.y -= 34

    def save(self):
        self.c.save()


def day01(path):
    s = Sheet(path, "Gün 1 - Chapter 1: Solid Basics")
    s.p("Kısa gün · yaklaşık 65 dk · Her şey bu PDF'in içinde, başka kitaba bakman gerekmiyor.", 10, color=GLOSS)
    s.todo(["Sırayla 4 adım var. Her adımın başında sarı kutuda ne yapacağın yazıyor.",
            "Kalemle direkt PDF'e yaz. Bitince cevapları sohbete yaz, ben düzelteyim.",
            "Cevap formatı: 'A1 am, A2 is, B1 ..., Okuma-1 ...' gibi numarasıyla, kısa.",
            "Süre: her adımda yazan dakikaya telefonda sayaç kur. Takılırsan atla, devam et."])

    # ---------------- ADIM 1
    s.h("ADIM 1 · to be (am / is / are): hızlı kontrol · 15 dk")
    s.todo(["1) Aşağıdaki kuralı oku (2 dk). Bunu zaten biliyorsun, sadece hatırla.",
            "2) A, B ve C bölümlerini yap (13 dk).",
            "Hepsi doğruysa to be konusunu bitirdik, yarın yeni konuya geçeriz."])
    s.table([("Özne", "to be", "Kısa / olumsuz"),
             ("I", "am", "I'm / I'm not   (I amn't diye bir şey YOK)"),
             ("you / we / they", "are", "you're / aren't"),
             ("he / she / it", "is", "she's / isn't")])
    s.para("Dikkat edilecek 4 tuzak (Türkçeden gelen hatalar):", 11, "B", ACCENT, gap=2)
    s.para("1) Cümle fiilsiz kalmaz: 'Yorgunum' = I am tired.  (I tired ✗)", 11, indent=8, gap=2)
    s.para("2) Hava, saat, mesafe için özne 'it': It is raining.  (Is raining ✗)", 11, indent=8, gap=2)
    s.para("3) Yaş 'be' ile: I'm twenty.  (I have twenty years ✗)", 11, indent=8, gap=2)
    s.para("4) Kısa cevap kısaltılmaz: Are you tired? - Yes, I am.  (Yes, I'm ✗)", 11, indent=8)
    s.para("Soru: be başa gelir. Are you a student?   this/these = yakın, that/those = uzak.", 11, gap=10)
    s.p("A. am / is / are yaz", 12, "B", color=ACCENT, gap=22)
    for q in ["A1  I ____ a teacher.", "A2  She ____ tired today.", "A3  They ____ in Istanbul.",
              "A4  It ____ cold outside.", "A5  We ____ not ready.  (kısa)", "A6  ____ you a student?",
              "A7  My parents ____ from Bursa.", "A8  ____ this your phone?"]:
        s.p(q, 13, gap=28)
    s.p("B. Soru ve olumsuz yap", 12, "B", color=ACCENT, gap=22)
    s.write("B1  She is happy.   (soru)", 1)
    s.write("B2  She is happy.   (olumsuz)", 1)
    s.write("B3  They are late.  (soru)", 1)
    s.write("B4  They are late.  (olumsuz)", 1)
    s.p("C. Hatayı bul, doğrusunu yaz", 12, "B", color=ACCENT, gap=22)
    s.write("C1  I have twenty years.")
    s.write("C2  She very tall.")
    s.write("C3  Are you ready? - Yes, I'm.")
    s.write("C4  Is raining now.")
    s.write("C5  These is my keys.")

    # ---------------- ADIM 2
    s.newpage()
    s.h("ADIM 2 · Okuma + kelime · 25 dk")
    s.todo(["1) Hikâyeyi bir kez baştan sona oku (3 dk). Bilmediğin kelimenin altını çiz.",
            "2) 8 kelime tablosuna bak. Zaten bildiğin kelimelerin yanına ✓ koy (5 dk).",
            "3) Soruları cevapla (7 dk). 4) Kendi 3 cümleni yaz (8 dk). Çeviri en sonda,",
            "   önce bakma. Takılırsan çeviriye bak, utanılacak bir şey değil."], None)
    s.para("A Normal Monday", 14, "B", ACCENT, gap=4)
    story = ["Sam usually wakes up at six o'clock. That is early, but Mondays are always like this. He prepares breakfast, cuts bread and makes tea for his family. Their flat is on the fourth floor, and morning is his favourite part of its long day.",
             "The night was cold, so he puts on his winter boots. Before he leaves, he checks his bag and fills his bottle with water. He has a free hour before work, and he knows exactly what to do with it.",
             "Sometimes he walks to the gym through the park. It is small, but it has a stone lion at the gate and an old tree near the lake. The cold wind hurts his ears a little, and he does not talk much on this walk.",
             "The gym is half a mile from home. Here he is not a father or an office worker; he is just a person with a bottle of water. He trains for forty minutes and does not stop once. Today is his thirteenth visit - a small number, but it means something to him.",
             "After training he buys tea at a cheap café on the corner. He sits by the window and watches the street. \"I am ready for the week,\" he thinks. Maybe that is the interesting part: nothing special happens, and that is exactly what he needs."]
    for para in story:
        s.para(para, 12.5, "R", INK, leading=19, gap=8)
    s.need(240)
    s.p("Bugünün 8 kelimesi (bildiklerine ✓ koy)", 12, "B", color=ACCENT, gap=22)
    rows = [("", "Kelime", "Türkçe", "Hikâyedeki hali"),
            ("☐", "always", "her zaman", "Mondays are always like this."),
            ("☐", "usually", "genellikle", "Sam usually wakes up at six."),
            ("☐", "sometimes", "bazen", "Sometimes he walks to the gym."),
            ("☐", "prepare", "hazırlamak", "He prepares breakfast."),
            ("☐", "check", "kontrol etmek", "he checks his bag"),
            ("☐", "free", "boş, serbest", "He has a free hour."),
            ("☐", "cheap", "ucuz", "a cheap café"),
            ("☐", "interesting", "ilginç", "the interesting part")]
    s.need(len(rows) * 24 + 10)
    for i, r in enumerate(rows):
        if i == 0:
            s.c.setFillColorRGB(*ACCENT)
            s.c.rect(M, s.y - 22, 500, 24, stroke=0, fill=1)
        x = M
        for j, (cell, w) in enumerate(zip(r, (30, 90, 100, 280))):
            if i == 0:
                s.c.setFillColorRGB(1, 1, 1); s.c.setFont("B", 11)
            else:
                s.c.setFillColorRGB(*(ACCENT if j == 1 else (GLOSS if j == 2 else INK)))
                s.c.setFont("B" if j == 1 else "R", 11)
            s.c.drawString(x + 4, s.y - 16, cell)
            x += w
        s.c.setStrokeColorRGB(0.85, 0.85, 0.88)
        s.c.line(M, s.y - 22, M + 500, s.y - 22)
        s.c.setStrokeGray(0); s.c.setFillColorRGB(*INK)
        s.y -= 24
    s.y -= 8
    s.para("always / usually / sometimes sıklık zarfıdır, fiilden önce gelir: He usually wakes up early.", 10, color=GLOSS, gap=10)
    s.p("Okuma soruları (kısa İngilizce cevap)", 12, "B", color=ACCENT, gap=22)
    s.write("R1  What time does Sam usually wake up?")
    s.write("R2  Where does he sometimes walk?")
    s.write("R3  Is the café expensive? (Yes/No + kısa cümle)")
    s.write("R4  How long does he train?")
    s.need(150)
    s.p("Senin cümlelerin (Pazartesi'n hakkında, 3 yeni kelimeyle)", 12, "B", color=ACCENT, gap=22)
    s.write("K1", 1)
    s.write("K2", 1)
    s.write("K3", 1)
    s.need(190)
    s.para("Türkçe çeviri (en son bak)", 11, "B", GLOSS, gap=3)
    tr = ["Sam genellikle saat altıda uyanır. Erken bir saat, ama pazartesileri hep böyledir. Kahvaltıyı hazırlar, ekmek keser, ailesine çay yapar. Daireleri dördüncü katta; uzun gününün en sevdiği kısmı da sabah saatleridir.",
          "Gece soğuk geçmiştir, o yüzden kışlık botlarını giyer. Çıkmadan önce çantasını kontrol eder, şişesini suyla doldurur. İşe gitmeden önce bir saatlik boş zamanı var ve bunu nasıl geçireceğini çok iyi bilir.",
          "Bazen spor salonuna parkın içinden yürür. Park küçüktür ama girişinde taş bir aslan, gölün kıyısında da yaşlı bir ağaç vardır. Soğuk rüzgâr kulaklarını biraz acıtır; bu yolda fazla konuşmaz.",
          "Spor salonu eve yarım mil uzaklıktadır. Burada bir baba ya da ofis çalışanı değil, elinde su şişesi olan sıradan bir insandır. Kırk dakika çalışır ve bir kez bile durmaz. Bugün on üçüncü gelişi: küçük bir sayı ama onun için bir anlamı var.",
          "Çalıştıktan sonra köşedeki ucuz kafeden bir çay alır. Cam kenarına oturup sokağı izler. 'Ben bu haftaya hazırım,' diye düşünür. Belki de en ilginç yanı şu: özel hiçbir şey olmuyor ve bu ona çok iyi geliyor."]
    for t in tr:
        s.para(t, 9.5, "R", GLOSS, leading=13, gap=4)

    # ---------------- ADIM 3
    s.newpage()
    s.h("ADIM 3 · Yazma · 15 dk")
    s.todo(["Kendini tanıt: yaklaşık 60 kelime (6-8 cümle). Çizgilere yaz.",
            "İçinde olsun: adın, nerelisin, mesleğin, ailen, sabah rutinin.",
            "En az 2 kez am/is/are ve 2 kez usually/always/sometimes kullan.",
            "Başlangıç örneği: My name is ... I am from ... I am a ... In the morning I usually ..."])
    for i in range(1, 9):
        s.write(f"{i}.", 1)

    # ---------------- ADIM 4
    s.h("ADIM 4 · Konuşma · 10 dk (sohbette yapacağız)")
    s.todo(["Bu adımı PDF'e yazmıyorsun. Önce soruları oku, her birine aklında bir cümle kur (2 dk).",
            "Sonra sohbete 'konuşma hazır' yaz. Ben soruyorum, sen cevap yazıyorsun.",
            "Hataları sonda toplu düzeltirim."])
    for q in ["What is your name, and where are you from?", "What do you do? Is your job interesting?",
              "Tell me about your family.", "What do you usually do in the morning?",
              "Do you always have tea or coffee? When?"]:
        s.p("•  " + q, 12, gap=22)
    s.save()


if __name__ == "__main__":
    name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f"worksheets/{name}.pdf"
    globals()[name](out)
    print(out)

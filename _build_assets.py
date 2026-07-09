"""One-shot asset builder: optimize portrait, OG image, CV PDF."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from fpdf import FPDF

root = Path(__file__).resolve().parent

# ── Optimize portrait ──────────────────────────────────────
src = root / "portfolioPortrait.png"
img = Image.open(src).convert("RGB")
w, h = img.size
max_side = 1100
if max(w, h) > max_side:
    scale = max_side / max(w, h)
    img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
img_q = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=192)
img_q.save(root / "portfolioPortrait.png", format="PNG", optimize=True)
print("png:", (root / "portfolioPortrait.png").stat().st_size // 1024, "KB", img.size)

img.save(root / "portfolioPortrait.webp", format="WEBP", quality=82, method=6)
print("webp:", (root / "portfolioPortrait.webp").stat().st_size // 1024, "KB")

# ── OG image 1200x630 ──────────────────────────────────────
og_w, og_h = 1200, 630
og = Image.new("RGB", (og_w, og_h), (5, 7, 13))
draw = ImageDraw.Draw(og)

for y in range(og_h):
    t = y / og_h
    r = int(5 + (10 - 5) * t)
    g = int(7 + (15 - 7) * t)
    b = int(13 + (26 - 13) * t)
    draw.line([(0, y), (og_w, y)], fill=(r, g, b))

port = Image.open(root / "portfolioPortrait.webp").convert("RGB")
pw, ph = port.size
crop_w = int(ph * 0.72)
left = max(0, (pw - crop_w) // 2)
port = port.crop((left, 0, left + crop_w, int(ph * 0.85)))
port = port.resize((460, 630), Image.Resampling.LANCZOS)
port = ImageEnhance.Color(port).enhance(0.75)
port = ImageEnhance.Contrast(port).enhance(1.08)
port = ImageEnhance.Brightness(port).enhance(0.9)
og.paste(port, (0, 0))
draw.rectangle([450, 0, 460, og_h], fill=(47, 216, 201))

try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 54)
    font_em = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 32)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
    font_small = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
except Exception:
    font_title = font_em = font_mono = font_small = ImageFont.load_default()

tx = 510
draw.text((tx, 150), "Dr. med.", font=font_em, fill=(47, 216, 201))
draw.text((tx, 195), "Mohammad Hamdan", font=font_title, fill=(234, 243, 244))
draw.text((tx, 270), "MD  |  MHBA  |  FEBNS", font=font_mono, fill=(127, 244, 232))
draw.text((tx, 330), "Oberarzt | Spine Surgery & Neurosurgery", font=font_small, fill=(119, 144, 159))
draw.text((tx, 365), "Fachklinik 360 | Ratingen, Germany", font=font_small, fill=(119, 144, 159))
draw.text((tx, 520), "neuro-hamdan.tech", font=font_mono, fill=(47, 216, 201))

og.save(root / "og-image.jpg", format="JPEG", quality=88, optimize=True)
print("og:", (root / "og-image.jpg").stat().st_size // 1024, "KB")


# ── CV PDF (branded) ───────────────────────────────────────
NAVY = (5, 7, 13)
TEAL = (47, 180, 170)
TEAL_DEEP = (18, 100, 95)
CREAM = (30, 35, 40)
MUTED = (90, 100, 110)
LIGHT = (248, 250, 250)


class CV(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_xy(14, 3.5)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*TEAL)
        self.cell(100, 5, "Dr. med. Mohammad Hamdan")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(180, 200, 200)
        self.cell(0, 5, "neuro-hamdan.tech", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.3)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Confidential professional CV  |  page {self.page_no()}/{{nb}}  |  neuro-hamdan.tech", align="C")


pdf = CV(format="A4")
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_left_margin(14)
pdf.set_right_margin(14)
content_w = pdf.epw

def ascii_safe(s):
    return s.encode("latin-1", errors="replace").decode("latin-1")


# Hero band
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 42, "F")
pdf.set_fill_color(*TEAL)
pdf.rect(0, 42, 210, 1.6, "F")

pdf.set_xy(14, 10)
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(234, 243, 244)
pdf.cell(0, 8, "Dr. med. Mohammad Hamdan", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(*TEAL)
pdf.cell(0, 6, "MD  |  MHBA  |  FEBNS", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(170, 190, 195)
pdf.cell(0, 5, "Oberarzt  |  Spine Surgery & Neurosurgery  |  Fachklinik 360, Ratingen", new_x="LMARGIN", new_y="NEXT")

pdf.set_y(50)


def write_line(text, style="", size=9, color=CREAM, h=4.6):
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(*color)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_w, h, ascii_safe(text))


def section(title):
    pdf.ln(2)
    pdf.set_fill_color(236, 246, 245)
    y = pdf.get_y()
    pdf.rect(pdf.l_margin, y, content_w, 7.5, "F")
    pdf.set_xy(pdf.l_margin + 2, y + 1.4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEAL_DEEP)
    pdf.cell(content_w - 4, 5, ascii_safe(title.upper()))
    pdf.set_xy(pdf.l_margin, y + 9)
    pdf.set_text_color(*CREAM)


def job(dates, title, place, note=None):
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*CREAM)
    pdf.set_x(pdf.l_margin)
    # title + dates on one visual block
    pdf.cell(content_w * 0.68, 5, ascii_safe(title))
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*TEAL_DEEP)
    pdf.cell(content_w * 0.32, 5, ascii_safe(dates), align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_w, 4.2, ascii_safe(place))
    if note:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "I", 8)
        pdf.multi_cell(content_w, 4, ascii_safe(note))
    pdf.ln(1.4)


# Contact strip
pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(*MUTED)
write_line(
    "dr.mhmdan@gmail.com   |   neuro-hamdan.tech   |   LinkedIn: mohammad-hamdan-m-d-dr-med-mhba-febns-aa2122216",
    size=8,
    color=MUTED,
    h=4.2,
)
write_line(
    "Clinic: Fachklinik 360 Ratingen  |  med360grad.de/leistungsangebot/fachklinik/  |  +49 2102 206-200",
    size=8,
    color=MUTED,
    h=4.2,
)

section("Professional Experience")
job("02/2026 - Present", "Oberarzt for Spine Surgery and Neurosurgery", "Fachklinik 360, Ratingen, Germany")
job("04/2026", "Fellow of the European Board of Neurological Surgery (FEBNS)", "Barcelona, Spain")
job("02/2025 - 02/2026", "Oberarzt for Spine Surgery and Neurosurgery", "Johanniter-Krankenhaus Duisburg-Rheinhausen, Germany")
job("10/2024 - 12/2024", "Specialist in Neurosurgery (Facharzt)", "Klinikum Frankfurt Hoechst (Varisano), Germany")
job(
    "02/2018 - 09/2024",
    "Resident Physician in Neurosurgery",
    "Mediapark-Klinikum Cologne | Saarland University Hospital | Klinikum Frankfurt Hoechst",
)
job(
    "07/2017 - 09/2017",
    "Medecins Sans Frontieres (Doctors Without Borders)",
    "Amman, Jordan - treatment of war-wounded patients from Syria, Yemen, and Iraq",
)

section("Education & Qualifications")
job(
    "02/2025",
    "Doctorate in Medicine (Dr. med.)",
    "Justus Liebig University Giessen, Germany",
    "Dissertation: Novel endoscopic TLIF and percutaneous dorsal spondylodesis technique (Prof. Dr. med. Kartik Krishnan).",
)
job(
    "2022 - 2024",
    "Master of Health Business Administration (MHBA)",
    "FAU Erlangen-Nurnberg - Thesis: Augmented Reality in Health Care",
)
job("04/2026", "FEBNS - European Board of Neurological Surgery", "Barcelona, Spain")
job("01-04/2026", "Eurospine Diploma & DWG Basis Certificate", "Strasbourg / Germany")
job("08/2022", "EANS Board Examination, Part I", "Maastricht, Netherlands")
job("2010 - 2017", "Doctor of Medicine (MD)", "University of Jordan, Amman - GPA 3.84/4.00 (distinction)")

section("Selected Training")
for line in [
    "Special Pain Therapy Course - Sylt, Germany - 10/2025",
    "RIWOSpine Global Endoscopic Spine Days - 05/2025",
    "Neurosurgery International Master Class - Dubai, UAE - 2024",
    "Radiation protection (RoV / StrSchV) - updated 2024",
]:
    write_line(f"  |  {line}", size=8.5, color=MUTED, h=4.2)

section("Publications & Research")
pubs = [
    "Dissertation (2025): Endoscopic TLIF technique - JLU Giessen (institutional copy on request).",
    "Vertebral Body Osteolysis 6 Years After Cervical Disk Arthroplasty. J Neurol Surg A, 2020. DOI: 10.1055/s-0039-1698435",
    "L-Citrulline Supplementation... Type 2 Diabetes. Circulation, 2015. DOI: 10.1161/circ.132.suppl_3.15199",
    "Central Corneal Thickness in a Jordanian Population... BMC Ophthalmology, 2018. PMID: 30373555",
]
for p in pubs:
    write_line(f"  |  {p}", size=8.5, color=MUTED, h=4.2)

section("Memberships | Languages | Skills")
write_line("Memberships: DGNC | Eurospine | DWG | EANS | AANS", size=8.5, color=MUTED, h=4.2)
write_line("Languages: Arabic (native) | German (C1) | English (C1)", size=8.5, color=MUTED, h=4.2)
write_line(
    "Clinical innovation: Python, C++, SPSS; fMRI (FSL); clinical AI documentation; digital health / AR.",
    size=8.5,
    color=MUTED,
    h=4.2,
)

section("Awards")
for a in [
    "University Royal Scholarship (Jordan, 2010)",
    'Demoqrati Award (2014) - "A Doctor in Every House"',
    "NRW-DAAD Scholarship (2015)",
    "Global Experience Digital Participation Camp (2015, 2016)",
]:
    write_line(f"  |  {a}", size=8.5, color=MUTED, h=4.2)

out = root / "Mohammad-Hamdan-CV.pdf"
pdf.output(str(out))
print("cv:", out.stat().st_size // 1024, "KB")
print("done")

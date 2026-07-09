# Dr. med. Mohammad Hamdan · Portfolio

Personal site for **Dr. med. Mohammad Hamdan, MD, MHBA, FEBNS** — Oberarzt for spine surgery and neurosurgery at Fachklinik 360° (Ratingen).

**Live:** [neuro-hamdan.tech](https://neuro-hamdan.tech/)

## What this site is

A single-page cinematic portfolio: clinical credentials, professional path, research, and contact — designed as a quiet, high-craft medical brand piece (navy / teal, scroll storytelling, 3D “signal” film).

## Contents

| Path | Purpose |
|------|---------|
| `index.html` | Full site (markup + interaction + Three.js scenes) |
| `portfolio2026-v10.css` | Design system and responsive layout |
| `portfolioPortrait.webp` / `.png` | Hero portrait (WebP preferred, PNG fallback) |
| `og-image.jpg` | Open Graph / social share card (1200×630) |
| `Mohammad-Hamdan-CV.pdf` | Downloadable curriculum vitae |
| `favicon.svg` | MH monogram favicon |
| `robots.txt` / `sitemap.xml` | Search hygiene |
| `cv_text.txt` | Plain-text CV source (kept in sync with the page) |
| `CNAME` | Custom domain for GitHub Pages |
| `memory/` · `templates/` · `CLAUDE.md` | Internal playbook for the cinematic landing engine (not part of the public page) |

## Local preview

```bash
npx serve .
# or: python -m http.server 8080
```

Open the printed URL in a visible browser tab (hidden tabs pause `requestAnimationFrame` / WebGL).

## Contact

- Email: [dr.mhmdan@gmail.com](mailto:dr.mhmdan@gmail.com)
- LinkedIn: [Mohammad Hamdan](https://www.linkedin.com/in/mohammad-hamdan-m-d-dr-med-mhba-febns-aa2122216/)
- Clinic: [Fachklinik 360°](https://www.med360grad.de/leistungsangebot/fachklinik/) · appointments secretariat `02102 206-200`

## Notes for maintainers

- Prefer editing copy and structure in `index.html`; keep `cv_text.txt` and `Mohammad-Hamdan-CV.pdf` aligned when dates or roles change.
- Rebuild assets (optimized portrait, OG card, PDF) with: `python _build_assets.py` (requires `pillow` and `fpdf2`).
- Motion respects `prefers-reduced-motion`; Three.js density and bloom are reduced on mobile.

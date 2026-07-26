# Business Growth Visualization Engine (BGVE)

**A desktop application that turns business scripts into animated, data-driven video overlays — built by a finance & business transformation consultant, for the content he creates.**

![Status](https://img.shields.io/badge/status-working%20end--to--end-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## The Problem

As a finance and tax compliance consultant (MJ Business Solutions), I make short-form content explaining VAT, CIT, and business compliance to Nigerian SME owners. Every creator in this space faces the same bottleneck: turning dry, numbers-heavy scripts into content that actually holds attention on TikTok, Reels, and WhatsApp Status — without spending hours in CapCut hand-animating every chart, deadline, and warning.

Generic templates don't fit finance/tax content. Nobody sells a "BOJ assessment formula reveal" or a "VATable vs non-VATable" animated comparison. So I built the tool myself.

## What BGVE Does

Give it a talking-head video and the script you spoke, and BGVE:
1. **Reads the script** and identifies moments worth visualizing — currency amounts, deadlines, risk language, comparisons, growth trends
2. **Generates a scene plan** automatically (which visual, what data, exactly when)
3. **Renders each visual** as a real animated motion-graphics overlay — numbers that count up, timelines that progress month by month, charts that draw themselves
4. **Composites everything** onto the original footage, positioned to never cover the speaker's face, branded and logo-tagged throughout
5. **Exports a finished, phone-first vertical video**, ready to post

All of this runs through a standalone desktop app — no code editing required for day-to-day use.

## Demo

*(demo GIF/video goes here)*

## Architecture
Script + Data
│
▼
Scene Generator ──▶ Scene JSON (template, timing, content)
│
▼
Renderer (Playwright) ──▶ Transparent animated PNG frame sequences
│
▼
Compositor (FFmpeg) ──▶ Frames + talking-head footage + logo
│
▼
Finished vertical video (1080×1920, phone-first)

**Stack:**
- **Python** — orchestration, scene logic, desktop app (PySide6)
- **HTML/CSS/JS + Playwright** — the actual animation engine. Every visual is a web page; Playwright drives a real headless Chromium browser to capture it frame by frame with a true alpha (transparency) channel — this means the animation quality of a modern browser, without needing a game engine or After Effects.
- **FFmpeg** — video compositing, timing, and export
- **PySide6** — the desktop application shell

This design choice (browser-based rendering instead of a custom-built engine) was a deliberate pivot partway through the project — after starting with plans for a from-scratch rendering/animation engine, I chose to build on proven, battle-tested rendering (the browser) instead of reinventing it. Same end result, dramatically faster to build and more reliable.

## Template Library

22 reusable, animated visual components, covering five content pillars (Tax & Compliance, Economic Survival, Business Reality, Business Systems, Tech & Future):

| Category | Templates |
|---|---|
| Alerts & Risk | BOJ-style alert, warning shake, deadline badges |
| Data | KPI counter, growth bar chart, line/trend chart, gauge/ratio meter |
| Time | 6-month countdown timeline, calendar flip |
| Comparison | Comparison table, before/after card, myth vs. fact reveal |
| Documents | Bank statement (auto-scroll), invoice, bank account flow, transaction sorting, approval/decline stamps |
| Structure | Process flow, government/tax authority flow, expansion map |
| Branding | Orbiting-icon outro, confetti burst |

Every template is built once and reused indefinitely — a new script never requires new code unless it introduces a genuinely new visual concept.

## Project Structure
scene_generator/ # script → scene JSON logic, rule-based content detection
renderer/ # HTML/CSS/JS templates + Playwright rendering scripts
templates/
compositor/ # FFmpeg overlay/compositing logic, background replacement (experimental)
app/ # PySide6 desktop application
scripts/ # test/utility scripts
samples/ # sample scripts, test footage
docs/ # architecture notes

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
```

FFmpeg must also be installed as a system binary — see `docs/setup.md`.

## Running the app

```bash
python app/main_window.py
```

Or use the packaged standalone executable (build with PyInstaller — see `docs/setup.md`).

## Roadmap

Full phase-by-phase build history: [ROADMAP.md](./ROADMAP.md)

## About

Built by **Mobola Jimoh** — Finance & Business Transformation Consultant, founder of MJ Business Solutions. This project sits at the intersection of accounting/tax expertise and hands-on software engineering — built to solve a real content problem, and to demonstrate the kind of systems-thinking I bring to client work.

Open to conversations about custom business tooling, automation, or data visualization work — reach out via [MJ Business Solutions](info.mjbusinesssolutions@gmail.com).

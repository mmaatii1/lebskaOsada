# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static single-page website for **Łebska Osada** — a luxury apartment complex in Żarnowska near Łeba, Poland. The entire site lives in one file: `index.html`. There is no build system, no package manager, no framework.

## File Structure

```
index.html          — entire website (HTML + CSS + JS, ~1300 lines)
sw.js               — Service Worker: caches images (WebP/JPG/PNG) for 7 days
robots.txt          — SEO robots config
fotki/              — exterior/property photos (.webp + .png pairs)
wpAranzacjeOkolice/ — interior/surroundings photos + logo + favicon (.webp/.jpg pairs)
karty-lokalow/      — apartment spec PDFs (10M6.pdf, 8M6.pdf, etc.)
```

## Development

No build step. Open `index.html` directly in a browser or serve with any static file server:

```bash
python3 -m http.server 8080
# or
npx serve .
```

No linting, no tests, no CI.

## Architecture of index.html

The file is structured in order: `<head>` meta/SEO → `<style>` (all CSS) → `<script>` analytics (Google Tag + Meta Pixel) → `<body>` sections → `<script>` (all JS at bottom).

**Page sections (in order):**
- `.top-banner` — animated promo strip
- `nav#mainNav` — fixed nav, becomes opaque on scroll (`.scrolled` class added by JS)
- `section.hero` — 3-image crossfade hero (`hero-bg-1/2/3`), CSS keyframe animations
- `section.atuty` — feature cards grid
- `section.lokalizacja` — location map + feature list (CSS grid layout on ≥640px)
- `section.atrakcje` — photo carousel (desktop) + simple grid
- `section.galeria` — filterable photo carousel
- `section.basen` — pool section
- `section.wyk` — interior photos carousel
- `section#listaapartamentow.apartamenty` — apartment cards with filter; `.apart-card.reserved` shows a ribbon overlay
- `section.operator` — rental operator section
- `section#promocja.promocja` — promo offer
- `section#formularz.formularz` — contact form (submits to Formspree `xbdpzngb`)
- `section.kontakt` — contact cards + social links
- `footer`
- `div#fabCall.fab-call` — fixed floating call button (phone menu dropdown)

**CSS custom properties** (`:root`):
- `--green-deep: #1a5276`, `--green-mid: #2e86c1`, `--green-light: #5dade2`
- `--sand: #eaf6fd`, `--sand-dark: #d6eaf8`
- `--gold: #c09a52`, `--gold-light: #dcc080`
- `--white: #f0f9ff`, `--text: #154360`, `--text-muted: #5d8aa8`

**Fonts:** Cormorant Garamond (serif, headings) + DM Sans (sans-serif, body). Loaded from Google Fonts with `media="print"` swap trick for non-blocking load.

**Scroll reveal:** Elements with `.reveal` start invisible; JS adds `.visible` once they enter viewport. Parent `<html>` gets `.js-loaded` class on DOMContentLoaded — this activates the reveal CSS transitions (so it degrades gracefully without JS).

**Carousels:** Two independent carousels with the same pattern: track element + dots + prev/next buttons. Gallery carousel supports category filtering (data-cat attribute on slides). Attractions carousel autoplay (4s interval) on desktop only (≥640px).

**Apartment filter:** `.filter-btn` buttons with `data-rooms` attribute; JS shows/hides `.apart-card` elements based on `data-rooms` match. `.apart-card.reserved` uses CSS `::after` to show a diagonal ribbon.

**FAB phone button** (`#fabCall`): Fixed circle button; click toggles `.open` class to show `.fab-call-menu` dropdown with two phone numbers:
- +48 792 503 213 (Patrycja Leonowicz — sales)
- +48 500 299 775 (Jarosław Szreder — company)

**Contact form:** Submits via `fetch` to Formspree. On success fires `fbq('track', 'Lead')` and a Google Ads conversion event.

**Service Worker** (`sw.js`): Cache-first for images, 7-day TTL tracked via custom `sw-cached-at` response header.

## Icons

All icons are inline SVGs with `fill="currentColor"` (no icon library). Icon sizing CSS:
- `.atut-icon svg, .feature-icon svg, .atrakcja-icon svg, .contact-icon svg` → `1.3em × 1.3em`
- `.icon-inline` → `1.1em × 1.1em`, `vertical-align: text-bottom` (used inline in text)

## Key External Services

- **Formspree** endpoint: `https://formspree.io/f/xbdpzngb`
- **Google Analytics/Ads**: `AW-18063980473`
- **Meta Pixel**: `2030720391135450`
- **Service Worker cache name**: `lebska-images-v1` (bump version to invalidate)

## Contact Info (for content edits)

- Email: `sprzedaz@lebskaosada.pl`
- Phone sales: `+48 792 503 213` (Patrycja Leonowicz)
- Phone company: `+48 500 299 775` (Jarosław Szreder)
- Address: ul. Wydmowa, Żarnowska 84-360, Pomorskie
- Canonical URL: `https://lebskaosada.pl/`

---
name: kimi-web-form-filler
description: Automatically fills forms and text fields on any website using humanized mouse movement, randomized click positions, right-click paste simulation, and stealth browsing techniques. Includes auto-learning to analyze and adapt to new websites. Trigger on fill form, auto fill website, humanize form filling, kimi web bridge form, paste into fields, or any request to automatically complete web forms without detection.
---

# Kimi Web Form Filler

## Overview
Automates filling of web forms and text fields with strong humanization to avoid bot detection. Uses randomized mouse paths, variable timing, right-click context-menu paste, and always varies click coordinates inside target elements. Includes an **auto-learning capability** to analyze new websites and adapt filling strategies dynamically.

## Core Principles
- Everything runs under `/home/workdir/artifacts` for persistence.
- Never use direct keyboard paste when right-click paste is possible.
- Always randomize click position inside the target field (never exact center).
- Insert realistic delays, micro-movements, and occasional overshoots.
- Prefer the existing humanization-stealth-browsing patterns when available.
- **Auto-Learning**: When a website is opened, the system analyzes its structure, learns fillable fields, and adapts future interactions based on patterns detected.

## Workflow

1. **Auto-Learning Analysis**
   - When a new website is opened, the system performs a full analysis of the page structure.
   - Identifies and logs all fillable fields, their types, labels, placeholders, and validation rules.
   - Stores learned patterns for future interactions with the same or similar websites.

2. **Analyze the Page**
   - Identify all fillable fields (input, textarea, contenteditable, select).
   - Map labels, placeholders, names, IDs, and nearby text.
   - Detect required vs optional fields and validation patterns.

3. **Plan the Fill Order**
   - Follow natural tab order or visual top-to-bottom / left-to-right order.
   - Group related fields (name blocks, address blocks, etc.).

4. **Humanized Interaction Loop** (for every field)
   - Move mouse with curved, variable-speed path toward the field.
   - Add small random jitter and occasional pause.
   - Click at a randomized offset inside the field bounds (never dead center).
   - Prefer right-click → "Paste" from context menu when pasting longer text.
   - For short values, type with realistic keystroke timing and occasional corrections.
   - After filling, briefly move the mouse away or hover nearby to mimic reading.

5. **Verification**
   - Re-read the value of each field after filling.
   - Retry once with a different click position if the value did not stick.
   - Report success/failure per field.

## Scripts
- `scripts/analyze_form.py` — Extract fillable fields and their metadata from page HTML or accessibility tree. Includes auto-learning logic to store and recall website patterns.
- `scripts/human_mouse.py` — Generate realistic mouse trajectories and randomized click points.
- `scripts/fill_field.py` — Single-field fill using the preferred humanized method.
- `scripts/learn_website.py` — Analyzes and stores website structures for future reference.

## Safety & Stealth Notes
- Never submit the form unless the user explicitly asks.
- Respect rate limits and add longer pauses on sensitive sites (login, payment, government).
- Log every action with timestamps and coordinates for debugging.
- Fall back to direct typing only when right-click paste is blocked by the site.

## Error Handling
- If a field cannot be located → skip and report.
- If paste is blocked → fall back to character-by-character typing with human delays.
- Always leave a clear summary of what was filled and what failed.
- If a website structure changes, re-analyze and update learned patterns.

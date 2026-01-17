---
name: crawler
description: |
  Intelligent web scraping with tiered approach: requests for static pages, Playwright for dynamic pages, Bright Data API for anti-bot bypass. Use when user needs to: (1) Scrape/crawl web pages, (2) Extract content from URLs, (3) Download articles or web content, (4) Convert web pages to PDF, (5) Handle blocked or protected websites. Triggers: "爬取", "抓取", "crawl", "scrape", "fetch URL", "get content from".
---

# Web Crawler

Tiered web scraping: static → dynamic → anti-bot bypass.

## Workflow

```
URL Input
    ↓
[1] requests (static)
    ↓ success? → done
    ↓ blocked?
[2] Playwright (dynamic)
    ↓ success? → done
    ↓ blocked?
[3] Bright Data (anti-bot)
    ↓
done
```

## Step 1: Static Scraping (requests)

Try first for all URLs. Fast and free.

```bash
python scripts/scrape_static.py "<url>"
```

**Success indicators:**
- `"success": true` in output
- Content length > 1000 characters
- No captcha/verification text detected

**Failure indicators (proceed to Step 2):**
- `"needs_upgrade": true`
- Contains "环境异常", "验证", "captcha", "blocked"

## Step 2: Dynamic Scraping (Playwright)

Use when Step 1 fails. Handles JavaScript-rendered content.

```bash
python scripts/scrape_dynamic.py "<url>" --pdf output.pdf
```

Options:
- `--pdf output.pdf` - Generate PDF
- `--screenshot output.png` - Take screenshot
- `-o output.json` - Save JSON result

**Success indicators:**
- `"success": true`
- Page title extracted
- Content visible in text field

**Failure indicators (proceed to Step 3):**
- `"needs_upgrade": true`
- Anti-bot still triggered

## Step 3: Bright Data API (Last Resort)

Use ONLY when both above methods fail. This costs money.

Use MCP tool `scrape_as_markdown`:
```
Tool: scrape_as_markdown
Parameters: { "url": "<target_url>" }
```

See [references/brightdata_usage.md](references/brightdata_usage.md) for details.

## Output Formats

### Save as PDF
```bash
# Direct from URL
python scripts/scrape_dynamic.py "<url>" --pdf article.pdf

# From saved HTML
python scripts/html_to_pdf.py input.html output.pdf
```

### Extract Text Only
```bash
python scripts/scrape_static.py "<url>" | jq -r '.text'
```

## Common Patterns

| Site Type | Recommended Method |
|-----------|-------------------|
| Static HTML, blogs | requests (Step 1) |
| WeChat articles | requests, fallback Playwright |
| JavaScript SPA | Playwright (Step 2) |
| Captcha/IP blocking | Bright Data (Step 3) |
| PDF generation | Playwright with --pdf |

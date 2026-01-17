#!/usr/bin/env python3
"""
Dynamic web scraper using Playwright.
Usage: python scrape_dynamic.py <url> [--pdf output.pdf] [--screenshot output.png]
"""

import sys
import asyncio
import json
import argparse


async def ensure_playwright():
    """Ensure playwright is installed."""
    try:
        from playwright.async_api import async_playwright
        return True
    except ImportError:
        print("Installing playwright...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        return True


async def scrape(url: str, pdf_path: str = None, screenshot_path: str = None) -> dict:
    """Scrape a webpage using Playwright."""
    await ensure_playwright()
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        try:
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(2)  # Wait for dynamic content

            content = await page.content()
            title = await page.title()

            # Check for anti-bot protection
            blocked_indicators = ["环境异常", "完成验证", "captcha", "blocked", "access denied"]
            for indicator in blocked_indicators:
                if indicator.lower() in content.lower():
                    if screenshot_path:
                        await page.screenshot(path=screenshot_path)
                    await browser.close()
                    return {
                        "success": False,
                        "error": f"Blocked by anti-bot protection (detected: {indicator})",
                        "needs_upgrade": True,
                        "screenshot": screenshot_path
                    }

            # Generate PDF if requested
            if pdf_path:
                await page.pdf(
                    path=pdf_path,
                    format='A4',
                    margin={'top': '15mm', 'right': '15mm', 'bottom': '15mm', 'left': '15mm'},
                    print_background=True
                )

            # Take screenshot if requested
            if screenshot_path:
                await page.screenshot(path=screenshot_path, full_page=True)

            # Extract text content
            text = await page.evaluate('() => document.body.innerText')

            await browser.close()

            return {
                "success": True,
                "title": title,
                "html": content,
                "text": text[:5000] + "..." if len(text) > 5000 else text,
                "content_length": len(text),
                "pdf": pdf_path,
                "screenshot": screenshot_path
            }

        except Exception as e:
            await browser.close()
            return {
                "success": False,
                "error": str(e),
                "needs_upgrade": True
            }


def main():
    parser = argparse.ArgumentParser(description='Dynamic web scraper using Playwright')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--pdf', help='Output PDF path')
    parser.add_argument('--screenshot', help='Output screenshot path')
    parser.add_argument('--output', '-o', help='JSON output file')
    args = parser.parse_args()

    result = asyncio.run(scrape(args.url, args.pdf, args.screenshot))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Output saved to: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

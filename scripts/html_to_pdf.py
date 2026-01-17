#!/usr/bin/env python3
"""
Convert HTML content to PDF using Playwright.
Usage: python html_to_pdf.py <input.html> <output.pdf> [--title "Title"]
"""

import sys
import asyncio
import argparse


async def html_to_pdf(html_path: str, pdf_path: str, title: str = None):
    """Convert HTML file to PDF."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f'file://{html_path}')
        await page.wait_for_load_state('networkidle')

        await page.pdf(
            path=pdf_path,
            format='A4',
            margin={'top': '20mm', 'right': '15mm', 'bottom': '20mm', 'left': '15mm'},
            print_background=True
        )

        await browser.close()
        print(f"PDF saved: {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description='Convert HTML to PDF')
    parser.add_argument('input', help='Input HTML file path')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--title', help='Document title')
    args = parser.parse_args()

    asyncio.run(html_to_pdf(args.input, args.output, args.title))


if __name__ == "__main__":
    main()

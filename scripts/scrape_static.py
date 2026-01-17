#!/usr/bin/env python3
"""
Static web scraper using requests.
Usage: python scrape_static.py <url> [output_file]
"""

import sys
import re
import json
from html import unescape

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


def scrape(url: str) -> dict:
    """Scrape a webpage using requests."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    html = response.text

    # Check for anti-bot protection (only trigger on specific patterns)
    # These patterns indicate the page is a captcha/verification page, not actual content
    blocked_patterns = [
        (r'环境异常.*完成验证', '环境异常验证页'),
        (r'<title>.*验证.*</title>', '验证页面'),
        (r'class="captcha"', 'captcha'),
        (r'Access Denied.*You don\'t have permission', 'access denied'),
        (r'rate.?limit.*exceeded', 'rate limit'),
    ]
    for pattern, name in blocked_patterns:
        if re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            return {
                "success": False,
                "error": f"Blocked by anti-bot protection (detected: {name})",
                "needs_upgrade": True
            }

    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = unescape(title_match.group(1)) if title_match else ""

    # Try to extract main content
    # WeChat article pattern
    wechat_title = re.search(r'var msg_title = ["\']([^"\']*)["\']', html)
    if wechat_title:
        title = wechat_title.group(1)

    content_match = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*(?:<div|<script)', html, re.DOTALL)
    if content_match:
        content_html = content_match.group(1)
        # Fix image src
        content_html = re.sub(r'data-src="([^"]+)"', r'src="\1"', content_html)
    else:
        # Generic content extraction
        content_html = html

    # Extract text
    text = re.sub(r'<[^>]+>', '', content_html)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()

    return {
        "success": True,
        "title": title,
        "html": content_html,
        "text": text[:5000] + "..." if len(text) > 5000 else text,
        "full_html": html,
        "content_length": len(text)
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_static.py <url> [output_file]")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = scrape(url)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Output saved to: {output_file}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

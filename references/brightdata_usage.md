# Bright Data MCP Usage

Bright Data is the last resort for bypassing anti-bot protection. Only use when requests and Playwright both fail.

## Available MCP Tools

The `brightdata` MCP server provides these tools:

### Basic Tools (Always Available)
- `search_engine` - Search query with scraped results
- `scrape_as_markdown` - Scrape URL and return markdown
- `scrape_batch` - Batch scrape multiple URLs

### Usage Examples

**Single page scrape:**
```
Tool: scrape_as_markdown
Parameters: { "url": "https://example.com/article" }
```

**Search and scrape:**
```
Tool: search_engine
Parameters: { "query": "topic keywords", "num_results": 5 }
```

**Batch scrape:**
```
Tool: scrape_batch
Parameters: { "urls": ["url1", "url2", "url3"] }
```

## When to Use Bright Data

Use ONLY when:
1. requests returned blocked/captcha response
2. Playwright also failed with anti-bot detection
3. The content is genuinely needed

Do NOT use for:
- Simple static pages
- Pages that load fine with requests
- First attempt at any URL

## Cost Awareness

Bright Data charges per request. Always try free methods first:
1. requests (free)
2. Playwright (free)
3. Bright Data (paid) - last resort only

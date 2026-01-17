# Crawler Skill

智能网页爬虫 Skill，采用阶梯式策略自动选择最优爬取方式。

## 特性

- **阶梯式爬取策略**：自动从简单到复杂尝试，避免不必要的资源消耗
- **多种爬取方式**：支持静态页面、动态渲染页面、反爬保护页面
- **PDF 导出**：支持将网页直接保存为 PDF
- **智能检测**：自动识别反爬机制并升级爬取策略

## 工作流程

```
URL 输入
    ↓
[1] requests (静态) ──→ 成功 ──→ 完成
    ↓ 失败
[2] Playwright (动态) ──→ 成功 ──→ 完成
    ↓ 失败
[3] Bright Data (反爬) ──→ 完成
```

## 安装

### 作为 Claude Code Skill 使用

将此仓库克隆到 Claude Code skills 目录：

```bash
git clone https://github.com/rubyluuu54-ai/crawler-skill.git ~/.claude/skills/crawler
```

### 依赖安装

```bash
# 静态爬取
pip install requests

# 动态爬取
pip install playwright
playwright install chromium
```

### Bright Data MCP 配置（可选）

如需使用 Bright Data 绕过反爬，在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "brightdata": {
      "command": "npx",
      "args": ["-y", "@brightdata/mcp"],
      "env": {
        "API_TOKEN": "your-api-token"
      }
    }
  }
}
```

## 使用方法

### 方式一：通过 Claude Code Skill 调用

在 Claude Code 中使用 `/crawler` 命令，或直接描述爬取需求：

- "爬取这个网页的内容"
- "抓取这篇文章并保存为 PDF"
- "scrape this URL"

### 方式二：直接运行脚本

**静态爬取：**
```bash
python scripts/scrape_static.py "https://example.com"
```

**动态爬取（支持 PDF 导出）：**
```bash
python scripts/scrape_dynamic.py "https://example.com" --pdf output.pdf
```

**HTML 转 PDF：**
```bash
python scripts/html_to_pdf.py input.html output.pdf
```

## 脚本参数

### scrape_static.py

```bash
python scrape_static.py <url> [output_file]
```

| 参数 | 说明 |
|------|------|
| `url` | 目标网页 URL |
| `output_file` | 可选，JSON 输出文件路径 |

### scrape_dynamic.py

```bash
python scrape_dynamic.py <url> [options]
```

| 参数 | 说明 |
|------|------|
| `url` | 目标网页 URL |
| `--pdf` | 生成 PDF 文件 |
| `--screenshot` | 生成截图 |
| `-o, --output` | JSON 输出文件路径 |

## 适用场景

| 网站类型 | 推荐方法 |
|----------|---------|
| 静态 HTML、博客 | requests (Step 1) |
| 微信公众号文章 | requests，备用 Playwright |
| JavaScript SPA | Playwright (Step 2) |
| 验证码/IP 封锁 | Bright Data (Step 3) |
| 需要生成 PDF | Playwright with --pdf |

## 输出格式

脚本返回 JSON 格式：

```json
{
  "success": true,
  "title": "页面标题",
  "text": "提取的文本内容...",
  "html": "<原始HTML>",
  "content_length": 12345
}
```

失败时返回：

```json
{
  "success": false,
  "error": "错误信息",
  "needs_upgrade": true
}
```

## 许可证

MIT License

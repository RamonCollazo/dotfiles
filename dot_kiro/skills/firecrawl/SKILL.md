---
name: firecrawl-cli
description: Web scraping, search, crawling, site mapping, and browser automation via the Firecrawl CLI. Use when the user needs to fetch web content, search the web, discover URLs on a site, crawl documentation, or interact with web pages programmatically.
---

# Firecrawl CLI

Web interaction tool installed at `/usr/local/bin/firecrawl` (v1.12.2). Authenticated and ready to use.

## Quick Reference

### Scrape a URL
```bash
firecrawl <url> --only-main-content
firecrawl <url> --html
firecrawl <url> --format markdown,links
firecrawl <url> --format images
firecrawl <url> --format summary
firecrawl <url> --screenshot
firecrawl <url> --include-tags article,main
firecrawl <url> -o output.md
```

### Search the web
```bash
firecrawl search "<query>" --limit 10
firecrawl search "<query>" --scrape --scrape-formats markdown
firecrawl search "<query>" --tbs qdr:d  # last day (h=hour, w=week, m=month, y=year)
firecrawl search "<query>" --categories github,research,pdf
```

### Map (discover URLs on a site)
```bash
firecrawl map <url>
firecrawl map <url> --search "blog" --limit 500
firecrawl map <url> --include-subdomains
```

### Crawl (full site)
```bash
firecrawl crawl <url> --limit 100 --max-depth 3 --wait --progress
firecrawl crawl <url> --include-paths /docs,/blog --wait
firecrawl crawl <job-id>  # check status
```

### Browser automation
```bash
firecrawl browser launch-session
firecrawl browser execute "open <url>"
firecrawl browser execute "snapshot"
firecrawl browser execute "click @e5"
firecrawl browser execute "scrape"
firecrawl browser close
```

### Agent (natural language web research)
```bash
firecrawl agent "<prompt>" --wait
firecrawl agent "<prompt>" --urls <url1>,<url2> --wait
```

### Status and credits
```bash
firecrawl --status
firecrawl credit-usage
```

## Notes
- Use `--only-main-content` for clean output (strips nav, footer, ads)
- Single format outputs raw content; multiple formats output JSON
- Crawl returns a job ID immediately; use `--wait` to block until complete
- Browser sessions run server-side Chromium — no local browser needed
- Credits: each scrape/crawl consumes credits. Check with `firecrawl --status`

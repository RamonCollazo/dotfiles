---
name: playwright-cli
description: Browser automation via Playwright CLI. Use when the user needs to open a browser, navigate pages, click elements, fill forms, take screenshots, test web UIs, or interact with web pages programmatically.
---

# Playwright CLI

Browser automation tool installed globally (`playwright-cli` v0.1.8).

## Workflow

```bash
playwright-cli open                          # open browser
playwright-cli open https://example.com      # open with URL
playwright-cli goto https://example.com      # navigate
playwright-cli snapshot                      # get page state with element refs
playwright-cli click e15                     # click element by ref
playwright-cli fill e5 "text" --submit       # fill input + press Enter
playwright-cli type "search query"           # type text
playwright-cli screenshot                    # take screenshot
playwright-cli close                         # close browser
```

## Core Commands

```bash
# Navigation
playwright-cli goto <url>
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload

# Interaction (use refs from snapshot)
playwright-cli click e3
playwright-cli dblclick e7
playwright-cli fill e5 "value" --submit
playwright-cli select e9 "option-value"
playwright-cli hover e4
playwright-cli drag e2 e8
playwright-cli check e12 / playwright-cli uncheck e12
playwright-cli upload ./file.pdf

# Keyboard
playwright-cli press Enter
playwright-cli press ArrowDown

# Snapshot & Screenshot
playwright-cli snapshot
playwright-cli snapshot --depth=4
playwright-cli snapshot e34
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf

# Evaluate JS
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5

# Tabs
playwright-cli tab-list
playwright-cli tab-new https://example.com
playwright-cli tab-select 0
playwright-cli tab-close

# Storage
playwright-cli cookie-list
playwright-cli cookie-get <name>
playwright-cli cookie-set <name> <value>
playwright-cli localstorage-get <key>
playwright-cli localstorage-set <key> <value>
playwright-cli state-save auth.json
playwright-cli state-load auth.json

# Network
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'

# DevTools
playwright-cli console
playwright-cli network

# Sessions
playwright-cli -s=mysession open https://example.com --persistent
playwright-cli list
playwright-cli close-all
```

## Raw Output

Use `--raw` to get clean output for piping:
```bash
playwright-cli --raw eval "document.title"
playwright-cli --raw snapshot > page.yml
```

## Browser Options

```bash
playwright-cli open --browser=chrome    # or firefox, webkit, msedge
playwright-cli open --persistent        # persistent profile
playwright-cli attach --cdp=chrome      # attach to running browser
```

## Notes
- Always `snapshot` after navigation or interaction to get current element refs
- Use element refs (e1, e2, etc.) from snapshots to target elements
- CSS selectors and Playwright locators also work: `playwright-cli click "#submit"`
- `--submit` on `fill` presses Enter after filling

import os
import argparse
import re
import time
import urllib.request
import urllib.error
from collections import OrderedDict, deque
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup, Tag

BASE = "https://kivy.org/doc/stable/"
API_ROOT = urljoin(BASE, "api-kivy.html")

REQUEST_DELAY = 0.05
TIMEOUT = 5

PAGE_CACHE: dict[str, str | None] = {}

def clean_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def inline_markdown(node: Tag | str) -> str:
    if isinstance(node, str):
        return node
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        value = inline_markdown(child)
        if name == "code":
            value = f"`{value.strip()}`"
        elif name in {"strong", "b"}:
            value = f"**{value.strip()}**"
        elif name in {"em", "i"}:
            value = f"*{value.strip()}*"
        elif name == "br":
            value = "\n"
        elif name == "a":
            href = child.get("href")
            if href:
                value = f"[{value.strip()}]({urljoin(BASE, href)})"
        parts.append(value)
    return clean_ws("".join(parts))

def description_to_markdown(dd: Tag, include_details: bool) -> str:
    soup = BeautifulSoup(str(dd), "html.parser")
    if not include_details:
        for nested in soup.select("dl, pre, .admonition"):
            nested.decompose()
    blocks: list[str] = []
    for child in soup.find_all(recursive=False):
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if name in {"p", "div", "section", "blockquote"}:
            value = inline_markdown(child)
            if value:
                blocks.append(value)
        elif name in {"ul", "ol"}:
            items: list[str] = []
            for li in child.find_all("li", recursive=False):
                value = inline_markdown(li)
                if value:
                    items.append(("- " if name == "ul" else "1. ") + value)
            if items:
                blocks.append("\n".join(items))
    if not blocks:
        value = inline_markdown(soup)
        if value:
            blocks.append(value)
    return "\n\n".join(x.strip() for x in blocks if x.strip())

def fetch(url: str, retries=2) -> str | None:
    if url in PAGE_CACHE:
        return PAGE_CACHE[url]
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Kivy-API-Crawler/1.0'})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                html = response.read().decode('utf-8', errors='replace')
                PAGE_CACHE[url] = html
                time.sleep(REQUEST_DELAY)
                return html
        except Exception as exc:
            print(f"[WARN] Failed: {url} on attempt {attempt+1}: {exc}")
            time.sleep(1)
    PAGE_CACHE[url] = None
    return None

def discover_urls(start_url: str) -> list[str]:
    html = fetch(start_url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select('a[href^="api-"]')
    
    pages = []
    for a in links:
        href = a.get("href", "")
        if href.startswith("api-"):
            full = urljoin(start_url, href)
            full, _ = urldefrag(full)
            if full not in pages:
                pages.append(full)
                print(f"[DISCOVER] {len(pages):>3}  {full}")
    return pages

def extract_api_entries(
    url: str, html: str, include_details: bool
) -> tuple[list[tuple[str, str, str, str]], list[tuple[str, str]]]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one("div[role='main']") or soup
    
    entries: list[tuple[str, str, str, str]] = []
    discovered_modules: list[tuple[str, str]] = []
    
    parsed = urlparse(url)
    filename = parsed.path.split("/")[-1]
    
    current_module = None
    if filename.startswith("api-") and filename.endswith(".html"):
        current_module = filename[4:-5]
        if current_module == "index":
            return [], []
    else:
        return [], []
        
    discovered_modules.append((current_module, url))

    for element in main.find_all("dl"):
        classes = set(element.get("class", []))
        if "py" not in classes:
            continue

        dt = element.find("dt", recursive=False)
        dd = element.find("dd", recursive=False)
        if not dt:
            continue

        object_id = dt.get("id")
        if not object_id or not object_id.startswith("kivy"):
            continue

        object_name = object_id
        description = description_to_markdown(dd, include_details) if dd else ""
        object_url = f"{url}#{dt['id']}" if dt.get("id") else url

        entries.append((current_module, object_name, description, object_url))

    return entries, discovered_modules

def generate(output: str, include_details: bool) -> None:
    print("Kivy API Reference Generator")
    print("=" * 31)
    print(f"Source: {BASE}")
    print()

    pages = discover_urls(API_ROOT)
    print(f"\nParsing {len(pages)} documentation pages...\n")

    modules: OrderedDict[str, OrderedDict[str, tuple[str, str]]] = OrderedDict()
    module_urls: dict[str, str] = {}

    for index, url in enumerate(pages, 1):
        html = fetch(url)
        if html is None:
            continue

        entries, discovered_modules = extract_api_entries(url, html, include_details)

        for module, module_url in discovered_modules:
            module_urls.setdefault(module, module_url)

        for module, object_name, description, object_url in entries:
            modules.setdefault(module, OrderedDict())
            if object_name not in modules[module]:
                modules[module][object_name] = (description, object_url)

        print(f"[PARSE   ] {index:>3}/{len(pages)}  {url}", flush=True)

    sorted_modules = sorted(modules.items(), key=lambda item: item[0].lower())

    with open(output, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Kivy API Reference\n\n")
        f.write("> Automatically generated from the Kivy documentation.\n")
        f.write(f"> Source: {BASE}\n\n")
        f.write("---\n\n")

        for module, objects in sorted_modules:
            module_url = module_urls.get(module, urljoin(BASE, f"api-{module}.html"))
            f.write(f"## API - [`{module}`]({module_url})\n\n")

            for object_name, (description, _object_url) in objects.items():
                f.write(f"**{object_name}**\n\n")
                if description:
                    f.write(f"{description}\n\n")

            f.write("---\n\n")

    total_objects = sum(len(objects) for objects in modules.values())

    print("\nDone!")
    print(f"Pages scanned : {len(pages)}")
    print(f"API modules   : {len(modules)}")
    print(f"API objects   : {total_objects}")
    print(f"Output file   : {output}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown Kivy API reference from ReadTheDocs."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "api", "kivy_api.md"),
        help="Output Markdown filename (default: kivy_api.md)",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Keep detailed parameter/return/event sections. Default is compact descriptions.",
    )
    args = parser.parse_args()

    generate(args.output, args.details)

if __name__ == "__main__":
    main()

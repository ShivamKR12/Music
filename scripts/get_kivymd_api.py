from __future__ import annotations
import os

import argparse
import re
import time
from collections import OrderedDict, deque
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

BASE = "https://kivymd.readthedocs.io/en/latest/"
API_ROOT = urljoin(BASE, "api/kivymd/")

REQUEST_DELAY = 0.08
TIMEOUT = 30

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "KivyMD-API-Reference-Generator/1.0",
        "Accept": "text/html,application/xhtml+xml",
    }
)

# Cache downloaded pages so a page is never downloaded twice.
PAGE_CACHE: dict[str, str | None] = {}


def clean_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def inline_markdown(node: Tag | str) -> str:
    """Convert a small HTML fragment to readable Markdown."""
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
    """Extract a readable description from a Sphinx autodoc <dd>."""
    soup = BeautifulSoup(str(dd), "html.parser")

    if not include_details:
        # Remove detailed parameter/return/event lists and examples.
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


def get_api_heading(heading: Tag) -> tuple[str | None, str | None]:
    """Return (module_name, heading_anchor) for an 'API - ...' heading."""
    text = clean_ws(heading.get_text(" ", strip=True))
    if not text.startswith("API -"):
        return None, None

    code = heading.find("code")
    if code:
        module = clean_ws(code.get_text(" ", strip=True)).strip("`")
    else:
        module = text.split("API -", 1)[1].strip().strip("`")

    if not module.startswith("kivymd"):
        return None, None

    anchor = heading.get("id")
    return module, anchor


def fetch(url: str) -> str | None:
    if url in PAGE_CACHE:
        return PAGE_CACHE[url]

    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        html = response.text
        PAGE_CACHE[url] = html
        time.sleep(REQUEST_DELAY)
        return html
    except requests.RequestException as exc:
        print(f"[WARN] Failed: {url}\n       {exc}")
        PAGE_CACHE[url] = None
        return None


def discover_urls(start_url: str) -> list[str]:
    """Crawl API pages plus component pages that contain the real class APIs."""
    queue = deque([start_url])
    seen: set[str] = set()
    pages: list[str] = []

    allowed_prefixes = (
        urljoin(BASE, "api/kivymd/"),
        urljoin(BASE, "components/"),
    )
    host = urlparse(BASE).netloc

    while queue:
        url, _ = urldefrag(queue.popleft())

        if url in seen:
            continue
        seen.add(url)

        parsed = urlparse(url)
        if parsed.netloc != host:
            continue
        if not url.endswith("/"):
            continue
        if not url.startswith(allowed_prefixes):
            continue

        html = fetch(url)
        if html is None:
            continue

        pages.append(url)
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a[href]"):
            nxt, _ = urldefrag(urljoin(url, a.get("href", "")))
            if nxt.startswith(allowed_prefixes) and nxt.endswith("/"):
                if nxt not in seen:
                    queue.append(nxt)

        print(f"[DISCOVER] {len(pages):>3}  {url}")

    return pages


def extract_api_entries(
    url: str, html: str, include_details: bool
) -> tuple[list[tuple[str, str, str, str]], list[tuple[str, str]]]:
    """
    Return:
        entries = (module, object_name, description, object_url)
        modules = (module, module_url)
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one("main") or soup.select_one("div[role='main']") or soup

    entries: list[tuple[str, str, str, str]] = []
    discovered_modules: list[tuple[str, str]] = []
    current_module: str | None = None
    current_module_url: str | None = None

    for element in main.find_all(["h1", "h2", "h3", "dl"]):
        if element.name in {"h1", "h2", "h3"}:
            module, heading_anchor = get_api_heading(element)
            if module:
                current_module = module
                current_module_url = url
                if heading_anchor:
                    current_module_url = f"{url}#{heading_anchor}"
                discovered_modules.append((module, current_module_url))
            elif element.name in {"h1", "h2"}:
                current_module = None
                current_module_url = None
            continue

        if current_module is None:
            continue

        classes = set(element.get("class", []))
        if "py" not in classes:
            continue

        dt = element.find("dt", recursive=False)
        dd = element.find("dd", recursive=False)
        if not dt:
            continue

        object_name = (dt.get("id") or clean_ws(dt.get_text(" ", strip=True))).strip()

        if not object_name.startswith("kivymd"):
            continue

        description = description_to_markdown(dd, include_details) if dd else ""
        object_url = url
        if dt.get("id"):
            object_url = f"{url}#{dt['id']}"

        entries.append((current_module, object_name, description, object_url))

    return entries, discovered_modules


def generate(output: str, include_details: bool) -> None:
    print("KivyMD API Reference Generator")
    print("=" * 31)
    print(f"Source: {BASE}")
    print()

    pages = discover_urls(API_ROOT)
    print(f"\nParsing {len(pages)} documentation pages...\n")

    # module -> object -> (description, object_url)
    modules: OrderedDict[str, OrderedDict[str, tuple[str, str]]] = OrderedDict()
    module_urls: dict[str, str] = {}

    for index, url in enumerate(pages, 1):
        html = PAGE_CACHE.get(url)
        if html is None:
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

        print(f"[PARSE   ] {index:>3}/{len(pages)}  {url}")

    # Put modules in alphabetical order.
    sorted_modules = sorted(modules.items(), key=lambda item: item[0].lower())

    with open(output, "w", encoding="utf-8", newline="\n") as f:
        f.write("# KivyMD API Reference\n\n")
        f.write("> Automatically generated from the KivyMD documentation.\n")
        f.write(f"> Source: {BASE}\n\n")
        f.write("---\n\n")

        for module, objects in sorted_modules:
            module_url = module_urls.get(module, f"{API_ROOT}#module-{module}")
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
        description="Generate a Markdown KivyMD API reference from ReadTheDocs."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "api", "kivymd_api.md"),
        help="Output Markdown filename (default: kivymd_api.md)",
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

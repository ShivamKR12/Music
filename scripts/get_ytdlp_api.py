import argparse
import inspect
import os
import sys
import yt_dlp

DEFAULT_OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs",
    "api",
    "yt-dlp_api.md"
)

def generate(output: str) -> None:
    print("yt-dlp API Reference Generator")
    print("=" * 31)
    print("Generating from local yt_dlp module...")

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        f.write("# yt-dlp API Reference\n\n")
        f.write("> Automatically generated from yt_dlp Python docstrings.\n")
        f.write(f"> yt-dlp version: {yt_dlp.version.__version__}\n\n")
        f.write("---\n\n")
        
        # YoutubeDL class doc
        ydl_doc = inspect.getdoc(yt_dlp.YoutubeDL)
        if ydl_doc:
            f.write("## API - `yt_dlp.YoutubeDL`\n\n")
            f.write("### Class Documentation & Options\n\n")
            f.write("```text\n")
            f.write(ydl_doc)
            f.write("\n```\n\n")

        # YoutubeDL Methods
        f.write("### Methods\n\n")
        methods = inspect.getmembers(yt_dlp.YoutubeDL, predicate=inspect.isfunction)
        for name, func in methods:
            if name.startswith("_"):
                continue  # skip private
            f.write(f"**{name}**\n\n")
            sig = ""
            try:
                sig = str(inspect.signature(func))
            except ValueError:
                pass
            
            f.write(f"`YoutubeDL.{name}{sig}`\n\n")
            doc = inspect.getdoc(func)
            if doc:
                f.write(f"{doc}\n\n")
            f.write("---\n\n")

    print("\nDone!")
    print(f"Output file: {output}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown yt-dlp API reference.")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output filename")
    args = parser.parse_args()
    generate(args.output)

if __name__ == "__main__":
    main()

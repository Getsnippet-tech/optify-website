"""Export App Store screenshots at exact pixel dimensions using Playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent

SCREENS = {
    "iphone": {
        "width": 1242,
        "height": 2688,
        "screens": [
            ("screen-1", "iPhone-1-Home.jpg"),
            ("screen-2", "iPhone-2-Personas.jpg"),
            ("screen-3", "iPhone-3-Tools.jpg"),
            ("screen-4", "iPhone-4-Styles.jpg"),
            ("screen-5", "iPhone-5-Brand.jpg"),
        ],
    },
    "ipad": {
        "width": 2064,
        "height": 2752,
        "screens": [
            ("ipad-1", "iPad-1-Home.jpg"),
            ("ipad-2", "iPad-2-Personas.jpg"),
            ("ipad-3", "iPad-3-Tools.jpg"),
            ("ipad-4", "iPad-4-Styles.jpg"),
            ("ipad-5", "iPad-5-Brand.jpg"),
        ],
    },
}

def export():
    iphone_dir = BASE / "export" / "iPhone"
    ipad_dir = BASE / "export" / "iPad"
    iphone_dir.mkdir(parents=True, exist_ok=True)
    ipad_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for device_type, config in SCREENS.items():
            w = config["width"]
            h = config["height"]
            out_dir = iphone_dir if device_type == "iphone" else ipad_dir

            context = browser.new_context(
                viewport={"width": w, "height": h},
                device_scale_factor=1,
            )
            page = context.new_page()

            for folder, filename in config["screens"]:
                html_path = BASE / folder / "index.html"
                url = f"file://{html_path.resolve()}"
                page.goto(url)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(500)

                out_path = out_dir / filename
                page.screenshot(path=str(out_path), full_page=False, type="jpeg", quality=95)
                print(f"✓ {filename} ({w}x{h})")

            context.close()

        browser.close()

    print(f"\nDone! Files in:")
    print(f"  {iphone_dir}")
    print(f"  {ipad_dir}")

if __name__ == "__main__":
    export()

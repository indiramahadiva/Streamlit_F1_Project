from pathlib import Path
# parents[0] = utils/, parents[1] = f1_monza/
ASSETS_PATH = Path(__file__).parents[1] / "assets"

DATA_PATH = ASSETS_PATH / "data"
IMAGE_PATH = ASSETS_PATH / "image"
STYLE_PATH = ASSETS_PATH / "style"
MARKDOWN_PATH = ASSETS_PATH / "markdown"

# Tyre compound colour palette — matches the official F1 colours in the Power BI dashboard
COMPOUND_COLOURS = {
    "SOFT": "#FF1E1E",
    "MEDIUM": "#FFD700",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#43B02A",
    "WET": "#0067AD",
    "UNKNOWN": "#888888",
}

# Years available for the Italian GP at Monza
MONZA_YEARS = [2023, 2024, 2025]

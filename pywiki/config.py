from pathlib import Path
from jinja2 import Environment, PackageLoader


class Config:
    env = Environment(
        loader=PackageLoader("pywiki"),
    )

    project_root = Path(__file__).parents[0].absolute()
    print(project_root)

    name = "wiki"
    theme = "default_theme"

    source_path = Path("")
    out_path = Path("./out")
    out_pages_path = out_path / name / "pages"
    out_styles_path = out_path / name / "styles"

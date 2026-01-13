import os
import io
import importlib.util
from typing import Optional


def _load_generator_module(base_dir: str):
    """Load generator helpers.

    Prefer a normal package import if `generator.py` is inside the package.
    Fall back to dynamic loading from base_dir/generator.py for backwards
    compatibility.
    """
    try:
        # generator.py now lives inside this package
        from . import generator as gen  # type: ignore
        return gen
    except Exception:
        # fallback: load generator.py from base_dir (repo root)
        gen_path = os.path.join(base_dir, "generator.py")
        spec = importlib.util.spec_from_file_location("pp_generator", gen_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def generate_worksheet_pdf(
    worksheet_id: int,
    student_name: str,
    student_iyatta: str,
    worksheet_date: str,
    worksheet_json_path: str,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate a worksheet PDF and return its bytes.

    Args:
      worksheet_id: numeric id used by the tag functions.
      student_name: name to render on the worksheet header.
      student_iyatta: class/grade to render on the header.
      worksheet_date: date string to render on the header.
      worksheet_json_path: path to the worksheet json file (used by open_worksheet).
      output_path: if provided, the PDF will also be written to this file path.

    Returns:
      The generated PDF as bytes.
    """
    # base_dir - repository root where tags/ and worksheets remain
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # package_dir where package-local assets (template, media, style) live
    package_dir = os.path.dirname(__file__)

    # load generator helpers from generator.py
    gen = _load_generator_module(base_dir)

    # read template from package directory
    template_path = os.path.join(package_dir, "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # open worksheet json (use provided path)
    questions = gen.open_worksheet(worksheet_json_path)

    # generate questions HTML and tags HTML
    questions_html = gen.generate_questions_html(questions)
    tags_html = gen.generate_tags_html(gen.getTagNumbers(worksheet_id))

    # fill template placeholders
    final_html = (
        template_html
        .replace("{{tags_html}}", tags_html)
        .replace("{{questions}}", questions_html)
        .replace("{{worksheet_id}}", str(worksheet_id))
        .replace("{{student_name}}", student_name)
        .replace("{{student_iyatta}}", student_iyatta)
        .replace("{{worksheet_date}}", worksheet_date)
    )

    # create PDF
    # Import weasyprint lazily so errors are raised only when generating
    from weasyprint import HTML

    # weasyprint needs a base_url so relative asset URLs (tags and worksheets)
    # resolve. We keep base_url as the repository root so the external
    # "tags/" folder and worksheet json files are found, while package-local
    # assets are referenced in the template with the package prefix.
    pdf_bytes = HTML(string=final_html, base_url=base_dir).write_pdf()

    # optionally write to disk
    if output_path:
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes


__all__ = ["generate_worksheet_pdf"]

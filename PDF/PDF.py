import os
import jinja2
from fpdf import FPDF
from datetime import datetime


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.template = None
        self.file_name = "cover_letter.pdf"

    def _get_date():
        return datetime.now().strftime("%B %d, %Y")

    def header(self):
        self.set_font("helvetica", "B", 12)
        self.cell(0, 10, " Cover Letter", 0, 1, "C")

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("helvetica", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_letter(self, title, body):
        self.add_page()
        self.chapter_body(body)

    def special_vars(self, context: dict):
        if "Today's_Date" in context.keys():
            context["Today's_Date"] = self._get_date()
        if "Your_Name" and "Company_Name" in context.keys():
            self.file_name = (
                f"{context['Your_Name']}_{context['Company_Name']}_Cover_Letter.pdf"
            )

    def create_cover_letter_pdf(
        self, template_path: str, output_path: str, context: dict
    ):
        template_content = ""
        self.special_vars(context)
        try:
            # Read the template file
            with open(template_path, "r") as file:
                template_content = file.read()
        except Exception as e:
            print("Error reading the template file", e)
            raise Exception("Error reading the template file", e)

        # Create a Jinja2 template object
        template = jinja2.Template(template_content)

        # Render the template with teh provided context
        cover_letter_content = template.render(context)
        self.add_letter(self.file_name, cover_letter_content)

        # Create a PDF object
        self.output(os.path.join(output_path, self.file_name), "F")

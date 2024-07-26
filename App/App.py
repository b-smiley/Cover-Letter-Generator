from os import name as os_name
from re import findall as re_findall
from pathlib import Path
from tkinter import Tk, filedialog
import eel
from PDF import PDF


class Application:
    """
    Application class for top-level logic
    """

    def __init__(self) -> None:
        self.TEMPLATE_PATH = "cover_letter_template.txt"
        self.output_path = self._usersDownloadFolder()
        self.context_placeholders: list = self._get_placeholders()
        self.context: list = {}
        eel.init("web")
        self._expose_list(eel)
        eel.start("index.html", size=(600, 850))

    def _expose_list(self, eel):
        """
        Exposing like this is a workaround for enabling the self parameter to be passed
        from the Application class to the frontend.
        """
        eel.expose(self.get_context)
        eel.expose(self.file_dialog)
        eel.expose(self.submit_context)

    def _get_placeholders(self):
        """
        Opens the template file and uses regex to find all placeholders.
        """
        try:
            with open(self.TEMPLATE_PATH, "r") as file:
                content = file.read()
            self.context_placeholders = re_findall(r"\{\{(.*?)\}\}", content)
            return self.context_placeholders
        except Exception as e:
            self.error_dialog("Error reading the template file", e)
            return

    def _usersDownloadFolder(self):
        """
        Gets the current user's download folder.
        """
        if os_name == "nt":
            return str(Path.home() / "Downloads")  # Windows
        else:
            return str(Path.home() / "Downloads")

    # Routes
    def get_context(self):
        return self.context_placeholders

    def file_dialog(self) -> str:
        """
        eel cannot return file system paths so the workaround is tkinter.
        """
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        folder = filedialog.askdirectory()
        return folder

    def submit_context(self, context: dict, output_path):
        try:
            # frontend uses placeholder sfor keys, backend needs to use placeholders
            for i in range(len(self.context_placeholders)):
                if self.context_placeholders[i] == "Todays_Date":
                    self.context[self.context_placeholders[i]] = PDF._get_date()
                    continue
                self.context[self.context_placeholders[i]] = context[
                    f"{self.context_placeholders[i]}"
                ]

            if output_path != "":
                self.output_path = output_path
            pdf = PDF()
            pdf.create_cover_letter_pdf(
                self.TEMPLATE_PATH, self.output_path, self.context
            )
            return "success"
        except Exception as e:
            print(e)
            return "fail"

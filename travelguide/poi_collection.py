"""
POI Collection Module.

Create a collection of POIs - points of interest.
"""
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
import os
from pathlib import Path
import traceback
from typing import Any
from poi import Poi


class PoiCollection:
    """PoiCollection."""

    def __init__(self, input_prompts: dict, all_pois: dict):
        """Initialize."""
        self.input_prompts = input_prompts
        self.all_pois = all_pois
        self.all_riddle_answers = {}

    # def create_poi_table_of_content(self, poi_list: List[dict]) -> str:
    #     """Create HTML table of contents for POIs."""
    #     try:
    #         toc_items = ''.join(
    #             [f"<li>{poi['name']}</li>" for poi in poi_list])
    #         return f"<ul>{toc_items}</ul>"
    #     except (KeyError, TypeError) as e:
    #         raise ValueError("Invalid POI list for table of contents") from e

    def create_poi_pages(self,
                         template_dir: str = 'templates',
                         output_dir: str = 'outputs') -> Any:
        """Create POI content with images."""
        poi_contents = []

        try:
            for poi_ident, poi_ident_detail in self.all_pois.items():
                p = Poi(self.input_prompts, poi_ident, poi_ident_detail)
                poi_prompt = p.generate_poi_prompt()
                response = p.call_api_poi_prompt(poi_prompt)
                if response is not None:
                    # images = p.retrieve_images(poi_ident)
                    # p.retrieve_image_details()
                    p.retrieve_images()
                    content = p.create_poi(template_dir, output_dir)
                    # content = p.create_poi('templates', 'outputs')
                    # content = p.create_poi(os.path.join(os.path.dirname(__file__),
                    #                                     '.', 'templates'),
                    #                        os.path.join(os.path.dirname(__file__),
                    #                                     '.', 'outputs'))
                    poi_contents.append(content)
                    # Extract riddle answers
                    # self.all_riddle_answers.append(p.retrieve_riddle_answers())
                    # Store riddle answers as a dict entry
                    # self.all_riddle_answers[poi_ident] = {
                    #     'detail': poi_ident_detail,
                    #     'riddle_answers': p.retrieve_riddle_answers()
                    # }
                    # Extract riddle answers and store minimal dict
                    self.all_riddle_answers[poi_ident] = {
                        'name': poi_ident_detail['name'],
                        'riddle_answers': p.retrieve_riddle_answers()
                    }
                else:
                    print("##### POI is None")
            return poi_contents
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to create POI Collection") from e

    def create_poi_riddle_answers(self,
                                  template_dir: str = 'templates',
                                  output_dir: str = 'outputs') -> str:
        """Generate riddle rally answers page."""
        try:
            print("*** Riddle Rally Answers")
            print(self.all_riddle_answers)

            # Render HTML template
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('riddlerallyanswers.html')
            htmlsource = template.render(
                all_riddle_answers=self.all_riddle_answers)

            # Write HTML to file
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / 'riddlerallyanswers.html'

            try:
                output_file.write_text(htmlsource, encoding='utf-8')
            except Exception as e:
                raise IOError(
                    f"Failed to write riddlerallyanswers to '{output_file}'"
                ) from e

            # options = {
            #     'page-size': 'A4',
            #     'margin-top': '20mm',
            #     'margin-right': '20mm',
            #     'margin-bottom': '20mm',
            #     'margin-left': '20mm',
            #     'encoding': "UTF-8",
            #     'no-outline': None,
            #     'enable-local-file-access': None
            # }

            # pdfkit.from_string(
            #     htmlsource, output_dir / 'itinerary.pdf', options=options)
            return htmlsource
        except TemplateNotFound as e:
            raise FileNotFoundError(f"Template 'riddlerallyanswers.html' not "
                                    f"found in '{template_dir}'") from e
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to create riddlerallyanswers content"
                             ) from e

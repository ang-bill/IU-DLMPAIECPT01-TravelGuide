"""
Itinerary Module.

Create an itinerary.
"""
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from pathlib import Path
import pprint
import traceback
from prompter import GenAIPrompter


class Itinerary:
    """Itinerary."""

    def __init__(self, input_prompts: dict):
        """Initialize."""
        self.input_prompts = input_prompts

    def generate_itinerary_prompt(self) -> str:
        """Generate itinerary prompt text."""
        try:
            # Load general itinerary instructions as template
            template = Template(
                self.input_prompts["general_itinerary_instructions"])

            # Render template with individual prompt and output example
            prompt_text = template.render(**self.input_prompts)

            return prompt_text
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to generate itinerary prompt") from e

    def call_api_itinerary_prompt(self, prompt_text: str) -> dict:
        """Call API with itinerary prompt ."""
        try:
            # Log to ease debugging
            pp = pprint.PrettyPrinter(indent=2, width=120)
            with open('debug/itinerary_prompt_request.txt', 'w',
                      encoding='utf-8') as f:
                f.write(pp.pformat(prompt_text))

            # API call
            genai_prompter = GenAIPrompter(self.input_prompts)
            response = genai_prompter.prompt(prompt_text, self.input_prompts[
                "itinerary_prompt_output_schema"])

            # Log to ease debugging
            pp = pprint.PrettyPrinter(indent=2, width=120)
            with open('debug/itinerary_prompt_response.txt', 'w',
                      encoding='utf-8') as f:
                f.write(pp.pformat(response))

            return response
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError("API call for itinerary prompt failed") from e

    def create_itinerary(self, itinerary_data: dict,
                         template_dir: str = 'templates',
                         output_dir: str = 'outputs') -> str:
        """Create formatted itinerary content (HTML and PDF)."""
        try:
            # Render HTML template
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('itinerary.html')
            htmlsource = template.render(**itinerary_data)

            # Write HTML to file
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / 'itinerary.html'

            try:
                output_file.write_text(htmlsource, encoding='utf-8')
            except Exception as e:
                traceback.print_exc()
                raise IOError(
                    f"Failed to write itinerary to '{output_file}'") from e

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
            traceback.print_exc()
            raise FileNotFoundError(f"Template 'itinerary.html' not found in"
                                    f" '{template_dir}'") from e
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to create itinerary content") from e

    def retrieve_all_pois(self, itinerary_data: dict) -> dict:
        """Retrieve POI list."""
        try:
            poi_dict = {
                poi['id']: poi
                for day in itinerary_data['itinerary']
                for poi in day['points_of_interest']
            }
            return poi_dict
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError("Retrieve POI list failed") from e

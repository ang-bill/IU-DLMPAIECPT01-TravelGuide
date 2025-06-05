"""
POI Module.

Create a POI - point of interest.
"""
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
import os
from pathlib import Path
import pprint
import re
import requests
import traceback
from typing import Any
import urllib.parse

from poi_images import PoiImages
from prompter import GenAIPrompter


class Poi:
    """Poi."""

    def __init__(self, input_prompts: dict, poi_ident: str,
                 poi_ident_detail: dict):
        """Initialize."""
        self.input_prompts = input_prompts
        self.poi_ident_detail = poi_ident_detail
        self.poi_ident = poi_ident
        self.poi_data = {}
        print("***Poi poi_ident:")
        print(self.poi_ident)
        print("***Poi poi_ident_detail:")
        print(self.poi_ident_detail)

    def generate_poi_prompt(self) -> str:
        """Generate prompt text for a single POI."""
        try:
            # Load general itinerary instructions as template
            template = Template(
                self.input_prompts["general_poi_instructions"])

            # Compose data for prompts
            prompts = self.input_prompts
            prompts['poi_ident'] = self.poi_ident_detail

            # Render template with individual prompt and output example
            self.prompt_text = template.render(**prompts)

            # print("***Poi promt text:")
            # print(self.prompt_text)
            return self.prompt_text
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to generate POI prompt") from e

    def call_api_poi_prompt(self, prompt_text: str) -> dict:
        """Call API with POI prompt ."""
        try:
            # Log to ease debugging
            pp = pprint.PrettyPrinter(indent=2, width=120)
            with open('debug/poi_prompt_request_' + self.poi_ident +
                      '.txt', 'w', encoding='utf-8') as f:
                f.write(pp.pformat(prompt_text))
            # API call
            genai_prompter = GenAIPrompter(self.input_prompts)
            self.poi_data = genai_prompter.prompt(
                prompt_text, self.input_prompts[
                    "poi_prompt_output_schema"])

            # print("***Poi data:")
            # print(self.poi_data)
            # Log to ease debugging
            pp = pprint.PrettyPrinter(indent=2, width=120)
            with open('debug/poi_prompt_response_' + self.poi_ident +
                      '.txt', 'w', encoding='utf-8') as f:
                f.write(pp.pformat(self.poi_data))

            return self.poi_data
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError("API call for POI prompt failed") from e

    def retrieve_images(self) -> Any:
        """Retrieve images and image details."""
        try:
            # Retrieve images
            pi = PoiImages(self.input_prompts, self.poi_ident,
                           self.poi_ident_detail)

            # Retrieve image details
            images_prompt = pi.generate_poi_images_prompt()
            images = pi.call_api_poi_images_prompt(images_prompt)
            image_details = pi.retrieve_image_details()

            # Append image details to poi_data
            self.poi_data['images'] = image_details

            return (image_details)

        except ValueError as e:
            traceback.print_exc()
            raise ValueError(
                "Failed to retrieve image details.") from e

    # def retrieve_image_details(self) -> Any:
    #     """Retrieve image details."""
    #     try:
    #         # Ensure the key exists (creates an empty list if
    #         # not), and appends safely.
    #         self.poi_data.setdefault('images', [])
    #         wikimedia_urls = self.poi_data['wikimedia_urls']
    #         for wikimedia_url in wikimedia_urls:
    #             try:
    #                 image_data = self.retrieve_wikimedia_image_detail(
    #                     wikimedia_url)
    #                 # Ensure the key exists (creates an empty list if
    #                 # not), and appends safely.
    #                 self.poi_data.setdefault('images', []
    #                                          ).append(image_data)
    #             except ValueError:
    #                 print(f"Image info not found for the wikimedia_url:"
    #                       f" {wikimedia_url}")
    #         return self.poi_data['images']

    #     except KeyError as e:
    #         traceback.print_exc()
    #         raise ValueError(
    #             "Failed to retrieve image details.") from e

    # @staticmethod
    # def retrieve_wikimedia_image_detail(page_url: str) -> str:
    #     """
    #     Retrieve direct wikimedia image details.

    #     Return dict with page_url, image_url, citation (APA 7 figure note).
    #     """
    #     try:
    #         # Extract filename from URL
    #         parsed = urllib.parse.urlparse(page_url)
    #         path_parts = parsed.path.split('/')
    #         if len(path_parts) < 3 or not path_parts[2].startswith('File:'):
    #             raise ValueError("Invalid Wikimedia Commons file page URL")

    #         # Extract and URL-decode the filename
    #         filename_encoded = path_parts[2].replace('File:', '')
    #         filename = urllib.parse.unquote(filename_encoded)
    #         # filename = path_parts[2].replace('File:', '')

    #         # Query Wikimedia API
    #         api_url = "https://commons.wikimedia.org/w/api.php"
    #         params = {
    #             'action': 'query',
    #             'titles': f'File:{filename}',
    #             'prop': 'imageinfo',
    #             'iiprop': 'url|extmetadata',
    #             'format': 'json'
    #         }

    #         response = requests.get(api_url, params=params)
    #         data = response.json()

    #         pages = data['query']['pages']
    #         page = next(iter(pages.values()))

    #         if 'imageinfo' not in page:
    #             raise ValueError("Image info not found for the file")

    #         imageinfo = page['imageinfo'][0]
    #         img_url = imageinfo['url']
    #         metadata = imageinfo['extmetadata']

    #         # Helper to safely get metadata values
    #         def get_meta(field, default=''):
    #             return metadata.get(field, {}).get('value', default).strip()

    #         # Extract fields
    #         title = get_meta('ObjectName') or filename.replace('_', ' ')
    #         author_html = get_meta('Artist', 'Wikimedia Commons user')
    #         author = BeautifulSoup(author_html, 'html.parser').get_text()
    #         date = get_meta('DateTimeOriginal') or get_meta(
    #             'DateTime') or get_meta('Date')
    #         license_name = get_meta('LicenseShortName')
    #         license_url = get_meta('LicenseUrl')

    #         # Extract year
    #         year_match = re.search(r'(\d{4})', date)
    #         year = year_match.group(1) if year_match else 'n.d.'

    #         # Build license text
    #         license_text = f"{license_name}" if not license_url else f"{license_name} ({license_url})"

    #         # Build citation (APA 7 figure note)
    #         citation = f"{title}. From {author}, {year}, Wikimedia Commons. {page_url} ({license_text})"

    #         return {
    #             'page_url': page_url,
    #             'image_url': img_url,
    #             'citation': citation
    #         }
    #     except Exception as e:
    #         traceback.print_exc()
    #         raise ValueError("Failed to retrieve image details.") from e

    # def retrieve_image_urls(self) -> Any:
    #     """Retrieve image URLs."""
    #     try:
    #         wikimedia_urls = self.poi_data['wikimedia_urls']
    #         for wikimedia_url in wikimedia_urls:
    #             image_url = self.retrieve_wikimedia_image_url(wikimedia_url)
    #             # Ensure the key exists (creates an empty list if
    #             # not), and appends safely.
    #             self.poi_data.setdefault('images', []
    #                                      ).append(image_url)
    #         return self.poi_data['images']

    #     except KeyError as e:
    #         traceback.print_exc()
    #         raise ValueError(
    #             "Failed to retrieve image URLs.") from e

    # @staticmethod
    # def retrieve_wikimedia_image_url(wikimedia_url: str) -> str:
    #     """Retrieve direct wikimedia image URL."""
    #     try:
    #         if wikimedia_url.startswith("https://upload.wikimedia.org"):
    #             return wikimedia_url
    #         else:
    #             # Get the file description page
    #             # Helps avoid potential blocking
    #             headers = {'User-Agent': 'Mozilla/5.0'}
    #             response = requests.get(wikimedia_url, headers=headers)
    #             soup = BeautifulSoup(response.content, 'html.parser')

    #             # Find the direct image URL (it is in the 'fullMedia' class or
    #             # 'a' with class 'internal')
    #             image_link = soup.find('a', class_='internal')
    #             if image_link:
    #                 image_url = image_link['href']
    #                 return image_url

    #     except KeyError as e:
    #         traceback.print_exc()
    #         raise ValueError(
    #             "Failed to retrieve direct wikimedia image URL.") from e

    def create_poi(self, template_dir: str = 'templates',
                   output_dir: str = 'outputs') -> str:
        """Create formatted poi content (HTML and PDF)."""
        try:
            # Add Geoapify API key
            load_dotenv()
            self.poi_data['geoapify_key'] = os.getenv('GEOAPIFY_KEY')

            # Render HTML template
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('poi.html')
            htmlsource = template.render(**self.poi_data)

            # Write HTML to file
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            print(self.poi_ident_detail)
            # print(self.poi_ident_detail('id'))
            # print(self.poi_ident_detail['id'])
            output_file = output_dir / (self.poi_ident + '.html')

            try:
                output_file.write_text(htmlsource, encoding='utf-8')
            except Exception as e:
                traceback.print_exc()
                raise IOError(
                    f"Failed to write poi to '{output_file}'") from e

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
            #     htmlsource, output_dir / (self.poi_ident['id']+'.pdf'),
            #     options=options)
            return htmlsource
        except TemplateNotFound as e:
            traceback.print_exc()
            raise FileNotFoundError(f"Template 'poi.html' not found in"
                                    f" '{template_dir}'") from e
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to create poi content") from e

    def retrieve_riddle_answers(self) -> list:
        """Retrieve Riddle answer list."""
        try:
            # riddle_answers_dict = {
            #     # riddle_answers['poi_ident']: self.poi_ident
            #     # riddle_answers['poi_ident_detail']: self.poi_ident_detail
            #     for riddle_answers in self.poi_data['riddle_answers']
            # }
            # riddle_answers_dict = self.poi_data['riddle_answers']
            # riddle_answers_dict = {
            #     'poi_ident': self.poi_ident,                # string
            #     'poi_ident_detail': self.poi_ident_detail,  # dict
            #     'riddle_answers': self.poi_data['riddle_answers']  # list
            # }
            # return riddle_answers_dict
            try:
                return self.poi_data['riddle_answers']  # returns list directly
            except KeyError:
                print("No riddle answers.")
                return None
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError("Retrieve Riddle answer list failed") from e

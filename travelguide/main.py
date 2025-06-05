"""
Travel Guide structure.

travelguide/
├── __init__.py
├── prompts/
│   ├── __init__.py
│   ├── individual_prompt.txt
│   ├── general_itinerary_instructions.txt
│   ├── itinerary_prompt_output_example.txt
│   ├── general_poi_instructions.txt
│   ├── poi_prompt_output_example.txt
├── templates/
│   ├── __init__.py
│   ├── itinerary_template.html
│   ├── poi_template.html
├── input_loader.py
├── itinerary.py
├── poi.py
├── poi_collection.py
├── merger.py
└── main.py
"""
from input_loader import load_input_prompt_files
from itinerary import Itinerary
from poi_collection import PoiCollection
from merger import merge_all_pages


def main():
    """Generate the travel guide based on input prompt and templates."""
    try:
        input_prompts = load_input_prompt_files("prompts")
        i = Itinerary(input_prompts)
        itinerary_prompt = i.generate_itinerary_prompt()
        itinerary_data = i.call_api_itinerary_prompt(itinerary_prompt)
        itinerary_htmlsource = i.create_itinerary(itinerary_data)

        all_pois = i.retrieve_all_pois(itinerary_data)
        poi_collection = PoiCollection(input_prompts, all_pois)
        poi_contents = poi_collection.create_poi_pages()
        poi_collection.create_poi_riddle_answers()

        merge_all_pages()

        print("Travel guide generated")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

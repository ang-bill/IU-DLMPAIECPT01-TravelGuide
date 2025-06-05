"""
Input Loader Module.

Load all input files.
"""
import os


def load_input_prompt_files(prompt_dir: str) -> dict:
    """
    Load all text files from the given directory as prompts.

    Args:
        prompt_dir (str): Directory path containing prompt text files.

    Returns:
        dict: Mapping of filename (without extension and version number)
              to file content.
    """
    prompts = {}
    try:
        for filename in os.listdir(prompt_dir):
            # if filename.endswith('.txt') or filename.endswith('.py'):
            if filename.endswith('.txt') or filename.endswith('.json'):
                filepath = os.path.join(prompt_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    stem = os.path.splitext(filename)[0]
                    key = stem.split('-', 1)[0]  # Split at first hyphen
                    prompts[key] = file.read()
    except (IOError, OSError) as e:
        raise RuntimeError(f"Failed to load prompts from {prompt_dir}") from e
    return prompts

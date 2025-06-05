"""
Output Merger Module.

Merge all output files.
"""
from natsort import natsorted
import os
import pdfkit
from typing import Any


def merge_all_pages(output_dir: str = 'outputs') -> Any:
    """
    Merge all created html files from the given directory into an pdf.

    Args:
        output_dir (str): Directory path containing prompt html files.

    Returns:
        htmlsource (str)

    """
    try:
        # Get list of all HTML files in the folder, sorted alphabetically
        html_files = sorted([
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.lower().endswith('.html')
        ])
        # folder_path = os.path.join(os.path.dirname(__file__), '..', output_dir)
        # folder_path = os.path.abspath(folder_path)

        # # Get sorted list of HTML files (with absolute paths!)
        # html_files = sorted([
        #     os.path.abspath(os.path.join(folder_path, f))
        #     for f in os.listdir(folder_path)
        #     if f.lower().endswith('.html')
        # ])
        # Natural sort, case-insensitive
        html_files = natsorted(html_files,
                               key=lambda x: os.path.basename(x).lower())

        # Optional: Check files to be merged
        print("HTML files to merge (in order):")
        for file in html_files:
            print(file)

        # Generate the PDF
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'footer-center': 'Page [page] of [topage]',  # Page X of Y
            'enable-local-file-access': None
        }
        toc = {
            'toc-header-text': 'Table of Contents'
        }

        # Generate PDF
        pdfkit.from_file(html_files,
                         os.path.join(output_dir, 'travelguide.pdf'),
                         options, toc)

        print("PDF generated successfully")

    except Exception as e:
        raise RuntimeError("Failed to merge all pages") from e

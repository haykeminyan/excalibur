import datetime
import logging

from docx.shared import Pt

logger = logging.getLogger(__name__)


def replace_placeholders_in_doc(doc, regex, replace_dict):
    """
    Replaces placeholders in the DOCX document with corresponding values from the replace_dict.
    """
    # Process paragraphs
    for p in doc.paragraphs:
        if p.text.strip():  # Only process non-empty paragraphs
            full_text = p.text  # Get the full text of the paragraph

            # Replace placeholders in the entire paragraph's text first
            new_text = replace_in_text(full_text, regex, replace_dict)
            p.clear()  # Clear existing runs to prevent overlapping styles
            p.add_run(new_text)  # Add the updated text

    # Process tables (cells within rows)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_placeholders_in_doc(cell, regex, replace_dict)


def replace_in_text(text, regex, replace_dict):
    """
    Helper function to replace placeholders in a text using regex from replace_dict.
    """
    text = text.strip()  # Trim the text
    logger.error(f'Original text: {text}')
    logger.error('!' * 100)

    # Use regex to find placeholders and replace them with values from the replace_dict
    for match in regex.finditer(text):
        placeholder = match.group(0)
        logger.error(f'Found placeholder: {placeholder}')

        # Check if the placeholder is in the replace_dict
        if placeholder in replace_dict:
            replacement_value = replace_dict[placeholder]

            # If the value is a datetime, convert it to string
            if isinstance(replacement_value, datetime.date):
                replacement_value = replacement_value.strftime('%Y-%m-%d')
            # If the value is None, replace with an empty string or default value
            elif replacement_value is None:
                replacement_value = ''

            logger.error(f'Replacing {placeholder} with {replacement_value}')
            text = text.replace(placeholder, str(replacement_value))

    return text


def set_font_size(doc):
    """Set the font size for the entire document to fit in one page."""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                # Loop through each paragraph in the cell
                for p in cell.paragraphs:
                    for run in p.runs:  # Loop through each run in the paragraph
                        run.font.size = Pt(10)  # Set

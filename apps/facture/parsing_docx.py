from django.http import HttpResponse
from docx import Document
from io import BytesIO
import aiofiles
import logging
import re
logger = logging.getLogger(__name__)
from django.contrib.staticfiles import finders


def generate_filled_document(template_path, output_path, json_calc):
    # Load the Word document
    doc = Document(template_path)
    # Extract text from paragraphs

    # Extract text from tables
    for paragraph in doc.paragraphs:
        for key, value in json_calc.items():
            if value is None:
                value = ""  # Replace None with an empty string
            placeholder = key
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, str(value))

    # Replace placeholders in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in json_calc.items():
                    if value is None:
                        value = ""  # Replace None with an empty string
                    placeholder = key
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, str(value))


    # Save the modified document to a buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Save the modified document to the specified path
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())

    return buffer

def process_and_save_docx(json_calc):
    template_path = '/usr/src/app/apps/facture/static/facture/file_templates/file_input/Facture_template_Maroc.docx'  # Path to your template file
    output_path = '/usr/src/app/apps/facture/static/facture/file_templates/file_output/xer.docx'  # Output file path

    # Generate the filled document
    buffer = generate_filled_document(template_path, output_path, json_calc)

    # Return the file as a downloadable response
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=modified_template.docx'
    return response


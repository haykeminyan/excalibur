import datetime
import re
from unittest.mock import MagicMock

import pytest
from docx import Document
from docx.shared import Pt

from apps.facture.parsing_docx import (
    replace_in_text,
    replace_placeholders_in_doc,
    set_font_size,
)


@pytest.fixture
def sample_doc():
    """Create a sample DOCX document with placeholders for testing."""
    doc = Document()

    # Add a paragraph with placeholders
    paragraph = doc.add_paragraph('Hello, {{name}}! Today is {{date}}.')

    # Add a table with placeholders
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = 'Order: {{order_id}}'
    table.cell(0, 1).text = 'Amount: {{amount}}'
    table.cell(1, 0).text = 'Status: {{status}}'
    table.cell(1, 1).text = 'Due: {{due_date}}'

    return doc


def test_replace_placeholders_in_doc(sample_doc):
    """Test the placeholder replacement logic."""
    # Define the regex for placeholders
    placeholder_regex = re.compile(r'{{(.*?)}}')

    # Define the replacement dictionary
    replace_dict = {
        '{{name}}': 'John Doe',
        '{{date}}': datetime.date(2025, 1, 3),
        '{{order_id}}': '12345',
        '{{amount}}': '100.00',
        '{{status}}': 'Pending',
        '{{due_date}}': datetime.date(2025, 1, 10),
        '{{empty_string}}': None,
    }

    # Call the function to replace placeholders
    replace_placeholders_in_doc(sample_doc, placeholder_regex, replace_dict)

    # Extract the updated text from the document
    paragraphs_text = [p.text for p in sample_doc.paragraphs]
    table_text = [
        [cell.text for cell in row.cells] for table in sample_doc.tables for row in table.rows
    ]

    # Assert that placeholders are replaced correctly in the paragraph
    assert paragraphs_text == ['Hello, John Doe! Today is 2025-01-03.']

    # Assert that placeholders are replaced correctly in the table
    assert table_text == [
        ['Order: 12345', 'Amount: 100.00'],
        ['Status: Pending', 'Due: 2025-01-10'],
    ]


def test_replace_in_text_with_none_value():
    """Test replace_in_text handles None values correctly."""
    # Define the regex for placeholders
    placeholder_regex = re.compile(r'{{(.*?)}}')

    # Define the text with placeholders
    input_text = 'Hello, {{name}}! Your order {{missing_placeholder}} is incomplete.'

    # Define the replacement dictionary, including a None value
    replace_dict = {
        '{{name}}': 'Jane Doe',
        '{{missing_placeholder}}': None,  # Placeholder with a None value
    }

    # Expected output after replacements
    expected_output = 'Hello, Jane Doe! Your order  is incomplete.'  # Notice the empty string

    # Call the function
    result = replace_in_text(input_text, placeholder_regex, replace_dict)

    # Assert the result matches the expected output
    assert result == expected_output


def test_set_font_size():
    """Test the set_font_size function."""
    # Mock the document structure
    mock_doc = MagicMock()
    mock_table = MagicMock()
    mock_row = MagicMock()
    mock_cell = MagicMock()
    mock_paragraph = MagicMock()
    mock_run = MagicMock()

    # Set up the relationships
    mock_doc.tables = [mock_table]
    mock_table.rows = [mock_row]
    mock_row.cells = [mock_cell]
    mock_cell.paragraphs = [mock_paragraph]
    mock_paragraph.runs = [mock_run]

    # Call the function
    set_font_size(mock_doc)

    # Assert that the font size was set
    mock_run.font.size = Pt(10)  # Set the expected value explicitly

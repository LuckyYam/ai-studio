import io
from typing import Literal

import pandas as pd
from docx import Document
from htmldocx import HtmlToDocx
from xhtml2pdf import pisa


def create_document(extension: Literal['pdf', 'docx', 'csv'], html: str, filename: str | None = None) -> tuple[bytes, str, str]:
    ext = extension.lower()
    name = (filename or 'document').strip() or 'document'
    if name.lower().endswith(f'.{ext}'):
        name = name[: -(len(ext) + 1)]
    if ext == 'pdf':
        buf = io.BytesIO()
        pisa.CreatePDF(io.StringIO(html), dest=buf)
        return buf.getvalue(), 'application/pdf', f'{name}.pdf'
    if ext == 'docx':
        doc = Document()
        HtmlToDocx().add_html_to_document(html, doc)
        buf = io.BytesIO()
        doc.save(buf)
        return (buf.getvalue(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', f'{name}.docx')
    if ext == 'csv':
        tables = pd.read_html(io.StringIO(html))
        if not tables:
            raise RuntimeError('No <table> found in the generated HTML to convert to CSV.')
        data = tables[0].to_csv(index=False).encode('utf-8')
        return data, 'text/csv', f'{name}.csv'
    raise RuntimeError(f'Unsupported document extension: {extension!r}')

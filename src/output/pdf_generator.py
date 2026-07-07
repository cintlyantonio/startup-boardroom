import os
import re
import datetime
import logging
import markdown
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)

def generate_pdf(markdown_content: str, idea: str, output_dir: str = "generated_plans") -> str:
    """
    Converts markdown business plan to a PDF file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a filesystem safe filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        
        # Create a slug from the idea (alphanumeric and dashes only, max 30 chars)
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', idea)
        slug = slug.strip('-').lower()[:30]
        
        filename = f"business_plan_{timestamp}_{slug}.pdf"
        output_path = os.path.join(output_dir, filename)
        
        # Convert markdown to HTML
        html_body = markdown.markdown(markdown_content, extensions=['tables'])
        
        # Get path to CSS and read it inline for xhtml2pdf
        css_path = os.path.join(os.path.dirname(__file__), "pdf_style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
        # Construct full HTML document for xhtml2pdf
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Business Plan</title>
            <style>
            {css_content}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        # Generate PDF using xhtml2pdf
        with open(output_path, "wb") as output_file:
            pisa_status = pisa.CreatePDF(
                full_html,
                dest=output_file
            )
            
        if pisa_status.err:
            raise RuntimeError(f"xhtml2pdf encountered errors: {pisa_status.err}")
        
        logger.info(f"Successfully generated PDF at {output_path}")
        return output_path
        
    except Exception as e:
        logger.exception("Failed to generate PDF")
        raise RuntimeError(f"PDF generation failed: {str(e)}") from e

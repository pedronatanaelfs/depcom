import pdfkit

def markdown_to_pdf(md_file, pdf_file):
    """
    Convert a Markdown file to PDF.

    Parameters:
    md_file (str): Path to the Markdown file.
    pdf_file (str): Path to save the generated PDF.
    """
    try:
        # Read the Markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert Markdown to HTML using markdown library
        from markdown import markdown
        html_content = markdown(markdown_content)

        # Save the HTML content to PDF
        pdfkit.from_string(html_content, pdf_file)
        print(f"PDF successfully saved as {pdf_file}")

    except Exception as e:
        print(f"Error during conversion: {e}")


markdown_to_pdf('depcom/src/atividade_2.md', 'depcom/src/atividade_2.pdf')

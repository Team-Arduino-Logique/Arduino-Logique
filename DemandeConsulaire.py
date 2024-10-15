from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, "Document: Demande de RDV", ln=True, align='C')

# Line break
pdf.ln(10)

# Set content
pdf.set_font('Arial', '', 12)
content = """L'extrait d'acte de naissance est actuellement au Consulat du Royaume du Maroc à Montréal. 
Veuillez contacter l'adjointe au consul, Mme Fatéma, pour plus d'informations."""
pdf.multi_cell(0, 10, content)

# Output PDF
pdf_output_path = "/mnt/data/reformulation_document.pdf"
pdf.output(pdf_output_path)

pdf_output_path

import io
import os
import datetime
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_ai_summary(risk_score: int, breakdown: dict) -> str:
    """Uses Gemini to generate a short 2-3 sentence summary of the security posture."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "AI Summary unavailable: API key not configured."
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a cybersecurity assistant. Based on this user's risk score, write a concise 2-3 sentence summary of their security posture.
        Keep it professional and focused on the key issues.
        
        Overall Score: {risk_score}/100 (100 is best)
        Penalties Breakdown (negative numbers are bad):
        {breakdown}
        """
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_report_pdf(email: str, risk_score: int, risk_breakdown: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    elements = []
    
    elements.append(Paragraph("Cyber Twin AI Security Report", title_style))
    elements.append(Spacer(1, 12))
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"<b>User:</b> {email}", normal_style))
    elements.append(Paragraph(f"<b>Generated:</b> {timestamp}", normal_style))
    elements.append(Spacer(1, 24))
    
    score_style = ParagraphStyle(
        'ScoreStyle', 
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.green if risk_score > 70 else (colors.orange if risk_score > 40 else colors.red)
    )
    elements.append(Paragraph(f"Overall Risk Score: {risk_score}/100", score_style))
    elements.append(Spacer(1, 24))
    
    elements.append(Paragraph("Score Breakdown", heading_style))
    elements.append(Spacer(1, 12))
    
    data = [["Category", "Penalty"]]
    for category, penalty in risk_breakdown.items():
        data.append([category.capitalize(), str(penalty)])
        
    table = Table(data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))
    
    elements.append(Paragraph("AI Security Summary", heading_style))
    elements.append(Spacer(1, 12))
    ai_summary = generate_ai_summary(risk_score, risk_breakdown)
    elements.append(Paragraph(ai_summary, normal_style))
    
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

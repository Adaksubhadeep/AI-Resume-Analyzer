from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from src.models import AnalysisReport

class PDFReportGenerator:
    @staticmethod
    def generate_pdf(report: AnalysisReport) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor("#1E3A8A"),
            spaceAfter=12
        )
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = styles['Normal']

        # Title
        story.append(Paragraph("ATS Resume Analysis Report", title_style))
        story.append(Paragraph(f"<b>Overall Score:</b> {report.ats_score}%", heading_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))

        # Summary
        story.append(Paragraph("Candidate Summary", heading_style))
        story.append(Paragraph(report.candidate_summary, body_style))
        story.append(Spacer(1, 10))

        # Matched / Missing
        story.append(Paragraph("Matched Skills", heading_style))
        story.append(Paragraph(", ".join(report.matched_skills) if report.matched_skills else "None", body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("Missing Skills", heading_style))
        story.append(Paragraph(", ".join(report.missing_skills) if report.missing_skills else "None", body_style))
        story.append(Spacer(1, 10))

        # Improvements
        story.append(Paragraph("Recommended Improvements", heading_style))
        for imp in report.resume_improvements:
            story.append(Paragraph(f"• {imp}", body_style))
        story.append(Spacer(1, 10))

        # Interview Questions
        story.append(Paragraph("Tailored Interview Questions", heading_style))
        for q in report.interview_questions:
            story.append(Paragraph(f"• {q}", body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer
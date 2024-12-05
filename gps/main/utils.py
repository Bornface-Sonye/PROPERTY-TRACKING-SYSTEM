from .models import (
    Owner, Laptop, Vehicle, Item, EntryLog, ExitLog, Authorised_User, System_User, PasswordResetToken
)

import string
import random

def generate_code():
    """Generate a random 10-character alphanumeric unique Code."""
    letters = string.ascii_uppercase
    digits = string.digits
    unique_code = ''.join(random.choice(letters + digits) for _ in range(6))
    return unique_code

def unique_code():
    """Generate a unique code not already in use."""
    while True:
        unique_code = generate_code()
        if not Laptop.objects.filter(unique_code=unique_code).exists():
            return unique_code
        
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_item_pdf(details, filename):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}"

    # Create PDF
    pdf_canvas = canvas.Canvas(response, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 12)

    y_position = 750
    for key, value in details.items():
        pdf_canvas.drawString(100, y_position, f"{key.replace('_', ' ').capitalize()}: {value}")
        y_position -= 20

    pdf_canvas.save()
    return response



from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_pdf(unique_code, entry_logs, exit_logs):
    # Create a BytesIO buffer
    buffer = BytesIO()

    # Create a PDF canvas
    pdf = canvas.Canvas(buffer)

    # Add content to the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, f"Log Details for Unique Code: {unique_code}")

    y_position = 770

    if entry_logs:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y_position, "Entry Logs:")
        y_position -= 20

        pdf.setFont("Helvetica", 10)
        for log in entry_logs:
            pdf.drawString(100, y_position, f"{log.timestamp} - {log.item_type}")
            y_position -= 15
    else:
        pdf.drawString(100, y_position, "No entry logs found.")
        y_position -= 20

    if exit_logs:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y_position, "Exit Logs:")
        y_position -= 20

        pdf.setFont("Helvetica", 10)
        for log in exit_logs:
            pdf.drawString(100, y_position, f"{log.timestamp} - {log.item_type}")
            y_position -= 15
    else:
        pdf.drawString(100, y_position, "No exit logs found.")
        y_position -= 20

    # Finalize the PDF
    pdf.showPage()
    pdf.save()

    # Prepare the HTTP response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


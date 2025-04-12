from django.http import HttpResponse
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
from .models import Teacher
import qrcode
from io import BytesIO

def generate_teacher_card_pdf(request, teacher_id):
    try:
        # Fetch the teacher from the database
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        return HttpResponse("Teacher not found", status=404)

    # Define card size (3.375 x 2.125 inches, standard ID card size)
    card_width, card_height = 3.375 * inch, 2.125 * inch

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{teacher.first_name}_{teacher.last_name}_Teacher_Card.pdf"'

    try:
        # Create a canvas with card dimensions
        p = canvas.Canvas(response, pagesize=(card_width, card_height))

        # White background
        p.setFillColor(colors.white)
        p.rect(0, 0, card_width, card_height, stroke=0, fill=1)

        # Add a dark blue bottom line
        p.setFillColor(colors.darkblue)
        p.rect(0, 0, card_width, 10, stroke=0, fill=1)

        # Add the school logo
        school_logo_path = os.path.join(settings.STATIC_ROOT, '1.png')
        if os.path.exists(school_logo_path):
            logo = ImageReader(school_logo_path)
            p.drawImage(logo, 10, card_height - 60, width=40, height=40)
        else:
            print(f"Logo not found at {school_logo_path}")

        # Title: "Teacher Card"
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(colors.black)
        p.drawString(70, card_height - 40, "Jubilee International")

        # Teacher details
        p.setFont("Helvetica", 9)
        p.setFillColor(colors.black)
        p.drawString(10, card_height - 80, f"Amission no: {teacher.admission_number}")
        p.drawString(10, card_height - 95, f"Name: {teacher.first_name} {teacher.last_name}")
        p.drawString(10, card_height - 110, f"Contact: {teacher.contact}")
        p.drawString(10, card_height - 125, f"Address: {teacher.address}")
        p.drawString(10, card_height - 140, f"Class Master: {'Yes' if teacher.is_class_master else 'No'}")

        # Add the teacher's photo
        if teacher.profile_photo and teacher.profile_photo.name:
            photo_path = os.path.join(settings.MEDIA_ROOT, teacher.profile_photo.name)
            if os.path.exists(photo_path):
                photo = ImageReader(photo_path)
                p.drawImage(photo, card_width - 70, card_height - 100, width=50, height=50)
            else:
                print(f"Profile photo not found at {photo_path}")
        else:
            p.setFont("Helvetica", 8)
            p.setFillColor(colors.red)
            p.drawString(card_width - 70, card_height - 90, "No Photo")

        # Generate QR Code
        qr_data = f"Admission no: {teacher.admission_number}\nName: {teacher.first_name} {teacher.last_name}\nContact: {teacher.contact}\nAddress: {teacher.address}\nClass Master: {'Yes' if teacher.is_class_master else 'No'}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image for the QR code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # Add QR code to the card
        qr_code_img = ImageReader(qr_buffer)
        p.drawImage(qr_code_img, card_width - 70, 10, width=40, height=40)  # Position the QR code

        # Finalize PDF
        p.showPage()
        p.save()
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return HttpResponse(f"Error generating card: {str(e)}", status=500)

    return response

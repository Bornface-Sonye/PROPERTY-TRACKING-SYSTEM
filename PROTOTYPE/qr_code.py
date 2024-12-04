import qrcode
from PyQt5.QtGui import QPixmap
from io import BytesIO

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    byte_io = BytesIO()
    img.save(byte_io)
    byte_io.seek(0)

    pixmap = QPixmap()
    pixmap.loadFromData(byte_io.read())
    return pixmap

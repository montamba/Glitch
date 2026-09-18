from qrcode import QRCode
import os

def generate(name, f):
    path = os.path.join("static/Qr/", f)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)

    qr = QRCode(version=5, box_size=20, border=4)
    qr.add_data(name)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=(0, 225, 225), back_color="black")
    img.save(path)
    
    return path



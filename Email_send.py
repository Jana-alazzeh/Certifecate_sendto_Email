import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 

from PIL import Image, ImageDraw, ImageFont 
import os 

# =========================================================
# 🔴 1. NAMES AND EMAILS (REMEMBER TO USE ACTUAL EMAILS) 🔴
# =========================================================
names_list = [
    {"name": "jjjjjjjjji", "email": "fm.mobile.494@gmail.com"},
    {"name": "Farah Yahya Aboushi", "email": "aboush ifarah@gmail.com"},
    {"name": "Farhhhhhhhhhhi", "email": "fm.mobile.494@gmail.com"},
   
    

]


# =========================================================
# 🔴 2. EMAIL CONFIGURATION (MUST USE APP PASSWORD) 🔴
# =========================================================
SMTP_SERVER = 'smtp.gmail.com'     
SMTP_PORT = 587
SENDER_EMAIL = 'jana.alazzeh4931@gmail.com'
SENDER_PASSWORD = 'mnyz jegb hitl bijj'

# =========================================================
# 3. SMTP CONNECTION SETUP
# =========================================================
try:
    print("Connecting to SMTP server...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls() 
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("Connection successful.")
except Exception as e:
    print(f"\nFATAL ERROR: Failed to connect to SMTP server. Please check credentials.")
    print(f"Error: {e}")
    exit() 

# 4. CERTIFICATE SETTINGS (No changes to sizes/coordinates)
output_folder = "Certificates"
os.makedirs(output_folder, exist_ok=True) 

# Font settings
font_path = "Alice/Alice-Regular.ttf" 
font_size = 350

try:
    font = ImageFont.truetype(font_path, font_size)
    id_font = ImageFont.truetype(font_path, 100) 
except IOError:
    print(f"ERROR: Font file not found at path: {font_path}") # EN
    exit() 

# Colors and Coordinates
X_center = 3100
Y_start = 1930
text_color = (145, 195, 239)      
stroke_color = (25, 75, 120)      
stroke_thickness = 15             
id_color_with_alpha = (121, 121, 121, 0) 

base_id = "CACE - BC - MMAA - GGAA - AA - AAAA"
id_position = (2130, 4000) 

# =========================================================
# 5. LOOP, GENERATION, AND SENDING
# =========================================================
for index, person in enumerate(names_list):
    
    name = person["name"]
    recipient_email = person["email"]
    
    if not recipient_email:
        print(f"Skipping {name}, no email provided.")
        continue

    # A. Generate ID
    suffix_index = index % 26 
    suffix_letter = chr(ord('A') + suffix_index)
    certificate_id = f"ID: {base_id}{suffix_letter}"
    
    # B. Open Template
    try:
        img = Image.open("image/Certificate.png").convert("RGBA")
    except FileNotFoundError:
        print(f"ERROR: Certificate template not found at path: image/Certificate.png") # EN
        continue 

    draw = ImageDraw.Draw(img)

    # Calculate centering
    text_bbox = draw.textbbox((0, 0), name, font=font, stroke_width=stroke_thickness)
    text_width = text_bbox[2] - text_bbox[0]
    X_position = X_center - (text_width / 2)
    text_position = (X_position, Y_start)

    # Draw Name and ID
    draw.text(text_position, name, fill=text_color, font=font, stroke_width=stroke_thickness, stroke_fill=stroke_color)
    draw.text(id_position, certificate_id, fill=id_color_with_alpha, font=id_font)

    # C. Save
    file_name = f"{name.replace(' ', '_')}_{suffix_letter}_Certificate.png" 
    output_path = os.path.join(output_folder, file_name)
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
        
    img.save(output_path)
    
    print(f"Certificate created for: {name} | Sending email...") # EN
    
    # D. Send Email
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = 'Congratulations! Your Certificate of Attendance'
        
        # Email Body (in Arabic for the recipient)
        body = f"مرحباً {name},\n\nيسرنا أن نرفق شهادة التقدير الخاصة بك برقم تسلسلي {certificate_id}.\n\nنتمنى لك التوفيق،\n[اسم الجهة/فريقك]"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Attach File
        with open(output_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="png")
            attach.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(attach)

        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"SUCCESS: Email sent to: {recipient_email}") # EN

    except Exception as e:
        print(f"❌ ERROR: Failed to send email to {recipient_email}. Error: {e}") # EN


# 6. Close Connection
server.quit()
print("\nAll certificates created and emails process completed.") # EN
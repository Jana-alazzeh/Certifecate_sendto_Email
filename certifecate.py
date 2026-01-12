from PIL import Image, ImageDraw, ImageFont 
import os 

# 1. الاسماء وهمية ! قائمة الأسماء:
names_list = [
"Hala Samer Al-Qadi",

"Karem Walid Jaber",

"Noor Eddin Al-Fares",

"Sara Yousif Al-Salem" 
]

# 2. إعداد المسارات:
output_folder = "Certificates"
os.makedirs(output_folder, exist_ok=True) 

# إعدادات الخط الرئيسي (الاسم)
font_path = "Alice/Alice-Regular.ttf" 
font_size = 350

try:
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    print(f"خطأ: لم يتم العثور على ملف الخط في المسار: {font_path}")
    exit() 

# إعدادات خط الترميز (ID)
id_font_size = 100 # حجم مقترح للـ ID ليتناسب مع حجم الخط 350
id_font = ImageFont.truetype(font_path, id_font_size) 
id_position = (2130, 4000) # مثال: الزاوية العلوية اليسرى. عدّلي هذا لتحديد الموقع.

# إعدادات الألوان والتنسيق (الاسم)
X_center = 3100
Y_start = 1930
text_color = (145, 195, 239)      # لون النص الداخلي
stroke_color = (25, 75, 120)      # لون الستروك (الكحلي #194b78)
stroke_thickness = 15             # سُمك الستروك

# إعدادات لون الترميز (ID) - أسود مع شفافية 35%
# (R, G, B, A) | A=255 يعني شفافية 0%، A=0 يعني شفافية 100%.
# 255 * 0.35 ≈ 89 (درجة الشفافية المطلوبة)
id_color_with_alpha = (121, 121, 121, 0) 


# =========================================================
# حلقة التكرار
# =========================================================
base_id = "CACE - BC - MMAA - GGAA - AA - AAAA"

for index, name in enumerate(names_list):
    
    # 1. توليد كود الترميز الأبجدي (A, B, C, ...)
    suffix_index = index % 26 
    suffix_letter = chr(ord('A') + suffix_index)
    certificate_id = f"ID: {base_id}{suffix_letter}"
    
    # 2. فتح قالب الشهادة
    try:
        img = Image.open("image/Certificate.png").convert("RGBA")
        # التحويل إلى RGBA ضروري لضمان عمل الشفافية بشكل صحيح
    except FileNotFoundError:
        print(f"خطأ: لم يتم العثور على قالب الشهادة في المسار: image/Certificate.png")
        continue 

    draw = ImageDraw.Draw(img)

    # 3. حساب عرض النص (الاسم) والتوسيط
    text_bbox = draw.textbbox((0, 0), name, font=font, stroke_width=stroke_thickness)
    text_width = text_bbox[2] - text_bbox[0]
    X_position = X_center - (text_width / 2)
    text_position = (X_position, Y_start)

    # 4. رسم الاسم مع الستروك (تجنب الرسم مرتين)
    # ملاحظة: تم حذف سطر draw.text المكرر، ورسم الاسم مرة واحدة فقط مع كل التنسيقات
    draw.text(
        text_position, 
        name, 
        fill=text_color, 
        font=font,
        stroke_width=stroke_thickness,   
        stroke_fill=stroke_color 
    )

    # 5. رسم كود الشهادة (ID)
    draw.text(id_position, certificate_id, fill=id_color_with_alpha, font=id_font)

    # 6. الحفظ 
    file_name = f"{name.replace(' ', '_')}_{suffix_letter}_Certificate.png" 
    output_path = os.path.join(output_folder, file_name)
    
    # لإزالة الشفافية وتحسين التوافق قبل الحفظ
    if img.mode == 'RGBA':
        img = img.convert('RGB')
        
    img.save(output_path)
    
    print(f"done foe: {name} with ID: {certificate_id}")

# =========================================================
# نهاية البرنامج
# =========================================================
print("\n creating images done sussecfully")

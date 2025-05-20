import cv2
import numpy as np
from skimage import color
from PIL import Image
import io

class ImageProcessor:
    @staticmethod
    def extract_skin_tone(image_bytes):
        # Convert image bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to LAB color space
        lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        
        # Extract the average L*a*b* values
        l, a, b = cv2.mean(lab_image)[:3]
        
        return l, a, b

    @staticmethod
    def suggest_colors(lab_values):
        # Simple color suggestion based on skin tone
        l, a, b = lab_values
        
        if l < 50:  # Dark skin
            return ["Navy", "Coral", "Emerald", "Burgundy", "Gold"]
        elif 50 <= l < 65:  # Medium skin
            return ["Teal", "Olive", "Plum", "Rust", "Mustard"]
        else:  # Light skin
            return ["Pastel Blue", "Lavender", "Peach", "Mint", "Rose"]

    @staticmethod
    def change_skin_tone(image_bytes, target_lab):
        # Convert image bytes to PIL Image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to LAB color space
        lab_image = color.rgb2lab(np.array(img))
        
        # Extract skin mask (simple threshold-based approach)
        skin_mask = (lab_image[:,:,0] > 20) & (lab_image[:,:,0] < 200) & \
                    (lab_image[:,:,1] > 0) & (lab_image[:,:,1] < 30) & \
                    (lab_image[:,:,2] > 0) & (lab_image[:,:,2] < 30)
        
        # Adjust skin tone
        lab_image[skin_mask, 0] = target_lab[0]
        lab_image[skin_mask, 1] = target_lab[1]
        lab_image[skin_mask, 2] = target_lab[2]
        
        # Convert back to RGB
        rgb_image = color.lab2rgb(lab_image)
        
        # Convert to PIL Image
        result_img = Image.fromarray((rgb_image * 255).astype(np.uint8))
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        result_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return img_byte_arr
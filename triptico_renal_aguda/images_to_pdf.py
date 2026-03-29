from PIL import Image
import os

def convert_images_to_pdf():
    img1_path = r"C:\Users\aicil\.gemini\antigravity\brain\91d2459c-5c26-4147-b48e-ba2ec0d9fa6e\acute_interior_v4_1772048198561.png"
    img2_path = r"C:\Users\aicil\.gemini\antigravity\brain\91d2459c-5c26-4147-b48e-ba2ec0d9fa6e\acute_exterior_v4_1772048205122.png"
    output_path = r"C:\Users\aicil\.gemini\antigravity\scratch\triptico_renal_aguda\Triptico_LRA.pdf"

    image1 = Image.open(img1_path).convert('RGB')
    image2 = Image.open(img2_path).convert('RGB')

    image1.save(output_path, save_all=True, append_images=[image2])
    print(f"PDF saved to {output_path}")

if __name__ == "__main__":
    convert_images_to_pdf()

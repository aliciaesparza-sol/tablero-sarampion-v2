from PIL import Image, ImageDraw, ImageFilter
import math

# Create a 256x256 image with dark purple-magenta gradient (similar to the screenshot)
size = 256
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw radial gradient background (circle shape)
center = size // 2
for r in range(center, 0, -1):
    # Interpolate from dark purple (center) to magenta-pink (outer)
    ratio = (center - r) / center
    red = int(80 + ratio * 100)
    green = int(0 + ratio * 20)
    blue = int(80 + ratio * 80)
    alpha = 255
    draw.ellipse(
        [center - r, center - r, center + r, center + r],
        fill=(red, green, blue, alpha)
    )

# Draw glowing teal/cyan outer ring
ring_width = 12
outer_r = center - 10
for offset in range(-ring_width, ring_width + 1):
    r_val = outer_r + offset
    glow_intensity = max(0, 255 - abs(offset) * 30)
    draw.ellipse(
        [center - r_val, center - r_val, center + r_val, center + r_val],
        outline=(0, glow_intensity, glow_intensity, glow_intensity),
        width=2
    )

# Draw syringe icon in center (simplified: rectangle + triangle)
syringe_color = (255, 180, 0, 255)  # Gold color
# Body
draw.rectangle([center - 8, center - 35, center + 8, center + 20], fill=syringe_color)
# Plunger
draw.rectangle([center - 12, center - 40, center + 12, center - 30], fill=syringe_color)
# Needle tip
draw.polygon([
    (center, center + 45),
    (center - 6, center + 20),
    (center + 6, center + 20)
], fill=syringe_color)
# Window on body
draw.rectangle([center - 5, center - 25, center + 5, center + 10], fill=(200, 220, 255, 200))

# Glow effect around syringe
img = img.filter(ImageFilter.GaussianBlur(0.5))

# Save as ICO
ico_path = r"C:\Users\aicil\.gemini\antigravity\scratch\vacunacion-durango-2026\coeva_icon.ico"
img.save(ico_path, format="ICO", sizes=[(256, 256)])
print(f"Icon saved to {ico_path}")

import base64
import os

static_dir = 'C:/Users/Hp/Desktop/Kenya-Africa-Projects/01-Agricultural-Prices/static'

# Read the transparent PNG
with open(os.path.join(static_dir, 'favicon_transparent.png'), 'rb') as f:
    png_data = base64.b64encode(f.read()).decode()

# Create SVG with embedded PNG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
  <image width="192" height="192" href="data:image/png;base64,{png_data}"/>
</svg>'''

# Save SVG favicon
with open(os.path.join(static_dir, 'favicon.svg'), 'w') as f:
    f.write(svg_content)

print('favicon.svg created')
print('Size:', len(svg_content), 'bytes')

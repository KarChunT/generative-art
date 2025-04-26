import os

# Directory containing the images
images_dir = "output/images"

# Output file (README.md)
readme_file = "README.md"

# Collect all image files
image_files = [
    f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))
]

# Generate HTML for grid layout
html_snippet = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;" align="center">\n'
for image in image_files:
    html_snippet += f'  <img src="{images_dir}/{image}" alt="{image}" width="150">\n'
html_snippet += "</div>\n"

# Append to README.md
with open(readme_file, "w") as readme:
    readme.write("\n<h1 align='center'>Generative Art</h1>\n")
    readme.write(html_snippet)

print(f"Added {len(image_files)} images to the grid layout in {readme_file}.")

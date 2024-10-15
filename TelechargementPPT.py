from PIL import Image

## Convert the first uploaded image to PNG format

# Path to the first uploaded image
uploaded_image_path_1 = "FdPourMedaillon.webp"
image_1 = Image.open(uploaded_image_path_1)
converted_path_1 = "FdPourMedaillon.png"
image_1.save(converted_path_1, "PNG")

converted_path_1

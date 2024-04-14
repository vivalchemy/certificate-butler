from PIL import Image, ImageDraw, ImageFont
import io


# Open the image file
def generateCertificate(image_path, participantName, fontSize, textPosition):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        "/usr/share/fonts/TTF/Poppins/Poppins-Regular.ttf", fontSize
    )
    text_color = "white"
    text_width = draw.textlength(participantName, font=font)
    image_width, image_height = image.size
    print(image_width, image_height)
    text_x = (image_width - text_width) // 2
    text_y = textPosition
    img_ext = image_path.split(".")[-1]
    # # Draw the text onto the image
    draw.text((text_x, text_y), participantName, fill=text_color, font=font)
    modified_image = io.BytesIO()
    image.save(modified_image, format=img_ext)
    modified_image.seek(0)
    # image.show()
    return modified_image

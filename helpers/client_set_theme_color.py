import requests
from PIL import Image
from io import BytesIO
from dominant_color import dominant_color, domimant_to_rgb, domimant_to_hex

def set_theme_color(client):
    response = requests.get(client.user.display_avatar.with_size(512).url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((572,572))
    dom_color = domimant_to_rgb(dominant_color(image, "default")[0]["color"])
    client.theme_color = dom_color
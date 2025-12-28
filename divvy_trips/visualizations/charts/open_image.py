import base64
from PIL import Image
from io import BytesIO

def open_image(url: str, **configs):
    pil_image = Image.open(url)
    if (rotate := configs.get("rotate")):
        pil_image = pil_image.rotate(rotate)
    output = BytesIO()
    pil_image.save(output, format="PNG")

        
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()
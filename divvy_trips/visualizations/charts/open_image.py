import base64
from PIL import Image
from io import BytesIO

def open_image(url: str, format: str = "PNG", **configs):
    pil_image = Image.open(url)

    if (opaqueLevel := configs.get("opaque")):
        pil_image.putalpha(opaqueLevel)
    if (rotate := configs.get("rotate")):
        pil_image = pil_image.rotate(rotate)
    if (flip := configs.get("flip")):
        if (flip == "left"):
            pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    if (width := configs.get("width")) and (height := configs.get("height")):
        pil_image = pil_image.resize((width, height), resample=Image.Resampling.BICUBIC)
    output = BytesIO()
    pil_image.save(output, format=format)
    
        
    if (format == 'PNG'):
        return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()
    if (format == 'JPEG'):
        return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode()
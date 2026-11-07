from pathlib import Path
import json,base64,io
from PIL import Image
root=Path(__file__).resolve().parents[2]
for item in json.loads((root/'reference/index2-raster-batch.json').read_text()):
    image=Image.open(io.BytesIO(base64.b64decode(item['data'].split(',')[1])))
    image.save(root/'assets/index2'/item['name'].replace('.svg','.webp'),lossless=True,method=6)
print('Saved lossless artwork batch')

from PIL import Image
from PIL.ExifTags import TAGS

ret = {}
i = Image.open("/home/bhanureddy/Pictures/test.jpeg")
info = i._getexif()
for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    ret[decoded] = value

print(ret)

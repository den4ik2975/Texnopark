'''from track_analyze import Track

track = Track('music/Endless Love - DVRST.mp3')

track.get_wav()
track.get_numbers()'''

from PIL import Image

image_template = Image.new('RGB', (370, 40), color=(78, 63, 96))
image_template.save('temp\\t.png')
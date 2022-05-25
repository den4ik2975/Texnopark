import io
import time

import numpy as np
import librosa.display
import PIL.Image as Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pydub import AudioSegment

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent


class Track:
    def __init__(self, tpath):
        self.track_path = tpath
        self.playing = False
        self.pl_name = '   ' + self.track_path[self.track_path.rfind("/") + 1:]
        self.content = QMediaContent(QUrl.fromLocalFile(self.track_path))
        self.sound = AudioSegment.from_mp3(self.track_path)

        self.lenth = 0
        self.wav_path = ''
        self.name = ''
        self.artist = ''
        self.album = ''
        self.image: Image = ''
        self.image_path = ''
        self.wav_path = ''
        self.numbers = []
        self.sec_lenth = 0
        self.delta = 0
        self.get_data()
        self.get_wav()
        self.get_numbers()

    def get_data(self):
        track = MP3(self.track_path)
        self.sec_lenth = int(track.info.length)
        self.lenth = time.strftime("%M.%S", time.gmtime(int(track.info.length)))
        self.name = track['TIT2'][0]
        self.artist = track['TPE1'][0]
        tr_im = ID3(self.track_path)
        self.image = Image.open(io.BytesIO(tr_im.getall('APIC')[0].data))

    def get_image(self):
        self.image.save('temp/i.png')
        return 'temp/i.png'

    def get_wav(self):
        self.wav_path = 'temp/c.wav'
        self.sound.export(self.wav_path, format='wav')

    def get_numbers(self):
        x, sr = librosa.load(self.wav_path)
        beats = librosa.beat.plp(y=x, sr=sr)
        hlp = len(beats) // self.sec_lenth
        for i in range(self.sec_lenth):
            self.numbers += [np.mean(beats[hlp * i: hlp * (i + 1)])]
        self.delta = 370 / max(self.numbers)





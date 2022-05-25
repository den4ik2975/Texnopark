from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QPen
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
import sys
import os
import time
from track_analyze import Track

MainUI = loadUiType('main.ui')[0]
WINDOW_SIZE = 0
counter = 0

full_path = os.path.join(os.getcwd(), 'test.mp3')


class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.num = -1
        self.player = QMediaPlayer()
        self.track_repeat = False
        self.player_volume = 10
        self.brush = QBrush()
        self.pen = QPen()
        self.ui()
        self.btns()
        self.playlist = []
        self.hlp_pix = QPixmap('temp\\t.png')
        self.pl_names = []
        self.duration = 0


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.frame_top_1.mouseMoveEvent = self.mouseMoveEvent
        self.playlist_text.setReadOnly(True)
        self.btn_play.setIcon(QIcon('icons\pause.png'))
        self.btn_play.setIconSize(QSize(24, 24))
        self.brush.setColor(QColor('#FFFFFF'))
        self.brush.setStyle(Qt.Dense1Pattern)
        self.pen.setColor(QColor("#FFFFFF"))

    def btns(self):
        self.btn_browse_track.clicked.connect(self.browse_track)
        self.btn_browse_folder.clicked.connect(self.browse_folder)
        self.btn_togle.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pg_home))
        self.btn_music.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pg_music))
        self.btn_music2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pg_setting))
        self.btn_go_to_setting.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pg_setting))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_close.clicked.connect(self.close)
        self.btn_play.clicked.connect(self.play_stop)
        self.btn_next.clicked.connect(self.play_next_track)
        self.btn_back.clicked.connect(self.play_previous_track)
        self.volume_button.setIcon(QIcon('icons\\volume.png'))
        self.volume_button.setIconSize(QSize(24, 24))
        self.volume_button.clicked.connect(self.mute_unmute)
        self.track_slider.setRange(0, 0)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.player_volume)
        self.volume_slider.sliderMoved.connect(self.volume_position_changed)
        self.track_slider.sliderMoved.connect(self.set_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    def mute_unmute(self):
        if self.player.volume() == 0:
            self.volume_button.setIcon(QIcon('icons\\volume.png'))
            self.volume_button.setIconSize(QSize(24, 24))
            self.player.setVolume(self.player_volume)
        else:
            self.volume_button.setIcon(QIcon('icons\\mute.png'))
            self.volume_button.setIconSize(QSize(24, 24))
            self.player.setVolume(0)

    def write_playlist(self):
        txt = ''
        for track in self.playlist:
            if track.playing is True:
                txt += f' ➜ {track.pl_name[3:]}\n'
            else:
                txt += f'{track.pl_name}\n'
        self.playlist_text.clear()
        self.playlist_text.insertPlainText(txt)

    def write_track(self, position):
        for track in self.playlist:
            if track.playing is True:
                txt = f'Title: {track.name}\n\n' \
                      f'Artist: {track.artist}\n\n' \
                      f'Time: {time.strftime("%M.%S", time.gmtime(position // 1000))}/{track.lenth}'
                self.current_song_text.clear()
                self.current_song_text.insertPlainText(txt)

                self.visual.setPixmap(self.hlp_pix)
                painter = QPainter(self.visual.pixmap())
                painter.setBrush(self.brush)
                painter.setPen(self.pen)
                hlp = int((track.numbers[position // 1000]) * track.delta)
                painter.drawRect(0, 0, hlp, 40)
                break

    def write_image(self):
        for track in self.playlist:
            if track.playing is True:
                pix = QPixmap(track.get_image())
                pix = pix.scaled(370, 370, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                self.track_icon.setPixmap(pix)
                break


    def play_previous_track(self):
        contentt = ''
        for i, track in enumerate(self.playlist):
            if track.playing is True:
                try:
                    contentt = self.playlist[i - 1].content
                    track.playing = False
                    self.playlist[i - 1].playing = True
                    break
                except IndexError:
                    contentt = self.playlist[0].content
                    track.playing = False
                    self.playlist[0].playing = True
                    break

        if contentt:
            self.player.setMedia(contentt)
            self.btn_play.setIcon(QIcon('icons\pause.png'))
            self.btn_play.setIconSize(QSize(24, 24))
            self.player.play()
            self.write_playlist()
            self.write_image()

    def play_next_track(self, num=-1):
        if num == -1 or num is False:
            contentt = ''
            for i, track in enumerate(self.playlist):
                if track.playing is True:
                    try:
                        contentt = self.playlist[i + 1].content
                        track.playing = False
                        self.playlist[i + 1].playing = True
                        break
                    except IndexError:
                        contentt = self.playlist[0].content
                        track.playing = False
                        self.playlist[0].playing = True
                        break
        else:
            contentt = self.playlist[num].content
            self.playlist[num].playing = True

        if contentt:
            self.player.setMedia(contentt)
            self.btn_play.setIcon(QIcon('icons\pause.png'))
            self.btn_play.setIconSize(QSize(24, 24))
            self.player.play()
            self.write_playlist()
            self.write_image()

    def browse_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder_name:
            files = os.listdir(folder_name)
            self.playlist = list(filter(lambda x: x.endswith('.mp3'), files))
            print('a')
            self.playlist = [Track(f'{folder_name}/{i}') for i in self.playlist]
            self.play_next_track(num=0)
            self.write_playlist()

    def browse_track(self):
        track_path = QFileDialog.getOpenFileName(self, 'Open music file', '', 'Music(*.mp3)')[0]
        if track_path:
            self.playlist = [Track(track_path)]
            self.play_next_track(num=0)
            self.write_playlist()

    def play_stop(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play.setIcon(QIcon('icons\play.png'))
            self.btn_play.setIconSize(QSize(24, 24))
        else:
            self.player.play()
            self.btn_play.setIcon(QIcon('icons\pause.png'))
            self.btn_play.setIconSize(QSize(24, 24))

    def volume_position_changed(self, position):
        if position == 0:
            self.volume_button.setIcon(QIcon('icons\mute.png'))
            self.volume_button.setIconSize(QSize(24, 24))
        else:
            self.volume_button.setIcon(QIcon('icons\\volume.png'))
            self.volume_button.setIconSize(QSize(24, 24))
        self.player_volume = position
        self.volume_slider.setValue(position)
        self.player.setVolume(position)

    def position_changed(self, position):
        self.track_slider.setValue(position)
        self.write_track(position)
        if self.duration == position and self.duration != 0:
            self.play_next_track()

    def duration_changed(self, duration):
        self.duration = duration
        self.track_slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)


def main():
    app = QApplication(sys.argv)
    main_win = Main()
    main_win.show()
    app.exec_()


if __name__ == '__main__':
    main()


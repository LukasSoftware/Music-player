""" Program is music player that can play only mp3 files right now,
    future plans are to play more kinds of music files,
    definitive version will be with options to equalize
    music stream but it is far future """

# -*- coding: utf-8 -*-

import wx
import pygame
import time
import threading
from mutagen.mp3 import MP3


class Frame(wx.Frame):

    def __init__(self, *args, **kw):
        super(Frame, self).__init__(*args, **kw)

# Initialize all variables, layout, widgets and buttons

        self.tracks = {}
        self.volume = 100
        self.paused = False
        self.played = False
        self.minutes = 0
        self.sec = 0
        panel1 = wx.Panel(self)

        play = wx.Bitmap(name="play.png", type=wx.BITMAP_TYPE_ANY)
        self.playButton = wx.BitmapButton(panel1, bitmap=play, pos=(102, 50), size=(25, 25))

        stop = wx.Bitmap(name="pause.png", type=wx.BITMAP_TYPE_ANY)
        self.stopButton = wx.BitmapButton(panel1, bitmap=stop, pos=(76, 50), size=(25, 25))

        forward = wx.Bitmap(name="forward.png", type=wx.BITMAP_TYPE_ANY)
        self.forwardButton = wx.BitmapButton(panel1, bitmap=forward, pos=(127, 50), size=(25, 25))

        rewind = wx.Bitmap(name="rewind.png", type=wx.BITMAP_TYPE_ANY)
        self.rewindButton = wx.BitmapButton(panel1, bitmap=rewind, pos=(50, 50), size=(25, 25))

        self.addButton = wx.Button(panel1, label="Add", pos=(470, 100), size=(50, 25))

        self.deleteButton = wx.Button(panel1, label="Delete", pos=(470, 125), size=(50, 25))

        self.clearButton = wx.Button(panel1, label="Clear", pos=(470, 150), size=(50, 25))

        self.timer = wx.Gauge(panel1, range=100, pos=(25, 30), size=(330, 5))

        self.volume = wx.Slider(panel1, value=100, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL,
                                pos=(160, 50), size=(100, -1))

        self.volumeValue = wx.StaticText(panel1, label="100%", pos=(260, 53))

        self.playList = wx.ListBox(panel1, pos=(10, 100), size=(460, 500))

        self.title_label = wx.StaticText(panel1, label="Currently not playing any song", pos=(10, 10))

        self.duration = wx.StaticText(panel1, label="0:00", pos=(360, 25))

        # Function to show main window

        self.show_gui()

    def show_gui(self):

        # Binding functions to buttons

        self.playButton.Bind(wx.EVT_BUTTON, self.play_audio)
        self.stopButton.Bind(wx.EVT_BUTTON, self.pause)
        self.forwardButton.Bind(wx.EVT_BUTTON, self.forward)
        self.rewindButton.Bind(wx.EVT_BUTTON, self.rewind)
        self.addButton.Bind(wx.EVT_BUTTON, self.add_to_playlist)
        self.deleteButton.Bind(wx.EVT_BUTTON, self.delete_track)
        self.clearButton.Bind(wx.EVT_BUTTON, self.clear_playlist)
        self.volume.Bind(wx.EVT_SCROLL, self.set_volume)
        self.playList.Bind(wx.EVT_LISTBOX_DCLICK, self.play_audio)

        # Initialize PyGame to play music

        pygame.init()
        pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)

        # Setting properties of window

        self.Center()
        self.SetSize(600, 700)
        self.SetTitle("MP3 Player")

# Definition of function that can set volume of playing music

    def set_volume(self, event):
        handler = event.GetEventObject()
        value = handler.GetValue()
        self.volumeValue.SetLabel(str(value) + "%")
        value = value / 100
        pygame.mixer.music.set_volume(value)

# Definition of function to add files to playlist

    def add_to_playlist(self, event):
        with wx.FileDialog(self, "Add file to playlist", wildcard="Music files (*.mp3)|*.mp3",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPaths()
            titles = file_dialog.GetFilenames()

            for i, e in zip(titles, path_name):
                position = self.playList.GetCount()
                self.playList.Insert(i, pos=position)
                self.tracks[i] = e

# Definition of function to delete track from playlist

    def delete_track(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track = self.playList.GetSelection()
            delete_track = self.playList.GetString(track)
            self.playList.Delete(track)
            self.tracks.pop(delete_track)
            if self.playList.GetCount() == 0:
                self.title_label.SetLabel("Currently not playing any song")

# Definition of function to clear playlist

    def clear_playlist(self, event):
        self.playList.Clear()
        self.tracks.clear()
        self.title_label.SetLabel("Currently not playing any song")
        pygame.mixer.music.stop()

# Definition of function that can change title of playing track when new is starting to play

    def change_title(self):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            current_track = self.playList.GetSelection()
            current_track = self.playList.GetString(current_track)
            self.title_label.SetLabel(current_track)

# Definition of main function that playing music

    def play_audio(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track_index = self.playList.GetSelection()
            track = self.playList.GetString(track_index)
            path = self.tracks[track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            audio_time = MP3(path).info
            audio_time = int(audio_time.length)
            self.process = threading.Thread(target=self.song_time)
            self.change_title()
            self.played = True
            self.process.start()

# Definition of function to change track to next on playlist

    def forward(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            self.played = False
            track_index = self.playList.GetSelection()
            self.playList.SetSelection(track_index + 1)
            track = self.playList.GetSelection()
            next_track = self.playList.GetString(track)
            path = self.tracks[next_track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        else:
            self.played = False
            return

# Definition of function to change track to previous

    def rewind(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track_index = self.playList.GetSelection()
            self.playList.SetSelection(track_index - 1)
            track = self.playList.GetSelection()
            next_track = self.playList.GetString(track)
            path = self.tracks[next_track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.played = False
        else:
            self.played = False
            return

# Definition of function to pause music stream

    def pause(self, event):

        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.played = True

        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.played = False

# Definition of function to show duration of playing song. Need to be fixed.

    def song_time(self):
        while self.played:
            if self.sec == 60:
                self.minutes += 1
                self.sec = 0
            if self.sec < 10:
                self.duration.SetLabel(f'{self.minutes}:0{self.sec}')
            else:
                self.duration.SetLabel(f'{self.minutes}:{self.sec}')

# Definition of function to show progress bar of playing song. Need to be fixed.

    def progress_bar(self, dur):
        secs = 0
        progress = dur / 100
        progress = int(round(progress, 0))

        if self.sec % progress == 0:
            secs += 1
            self.timer.SetValue(secs)
        time.sleep(1)
        self.sec += 1


# Definition of main app function

def execute():
    app = wx.App()
    exe = Frame(None)
    exe.Show()
    app.MainLoop()


# Start app as thread

t = threading.Thread(target=execute)
t.start()

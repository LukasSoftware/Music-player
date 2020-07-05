# -*- coding: utf-8 -*-

import wx
import pygame
# import time


class Frame(wx.Frame):

    def __init__(self, *args, **kw):
        super(Frame, self).__init__(*args, **kw)

        self.tracks = {}
        self.volume = 100
        self.paused = False

        self.show_gui()

    def show_gui(self):
        panel1 = wx.Panel(self)

        play = wx.Bitmap(name="play.png", type=wx.BITMAP_TYPE_ANY)
        self.playButton = wx.BitmapButton(panel1, bitmap=play, pos=(102, 50), size=(25, 25))
        self.playButton.Bind(wx.EVT_BUTTON, self.play_audio)

        stop = wx.Bitmap(name="pause.png", type=wx.BITMAP_TYPE_ANY)
        self.stopButton = wx.BitmapButton(panel1, bitmap=stop, pos=(76, 50), size=(25, 25))
        self.stopButton.Bind(wx.EVT_BUTTON, self.pause)

        forward = wx.Bitmap(name="forward.png", type=wx.BITMAP_TYPE_ANY)
        self.forwardButton = wx.BitmapButton(panel1, bitmap=forward, pos=(127, 50), size=(25, 25))
        self.forwardButton.Bind(wx.EVT_BUTTON, self.forward)

        rewind = wx.Bitmap(name="rewind.png", type=wx.BITMAP_TYPE_ANY)
        self.rewindButton = wx.BitmapButton(panel1, bitmap=rewind, pos=(50, 50), size=(25, 25))
        self.rewindButton.Bind(wx.EVT_BUTTON, self.rewind)

        self.addButton = wx.Button(panel1, label="Add", pos=(470, 100), size=(50, 25))
        self.addButton.Bind(wx.EVT_BUTTON, self.add_to_playlist)

        self.deleteButton = wx.Button(panel1, label="Delete", pos=(470, 125), size=(50, 25))
        self.deleteButton.Bind(wx.EVT_BUTTON, self.delete_track)

        self.clearButton = wx.Button(panel1, label="Clear", pos=(470, 150), size=(50, 25))
        self.clearButton.Bind(wx.EVT_BUTTON, self.clear_playlist)

        self.timer = wx.Gauge(panel1, range = 100, pos=(25, 30), size=(330, 5))

        self.volume = wx.Slider(panel1, value=100, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL,
                                pos=(160, 50), size=(100, -1))
        self.volume.Bind(wx.EVT_SCROLL, self.set_volume)

        self.volumeValue = wx.StaticText(panel1, label="100%", pos=(260, 53))

        self.playList = wx.ListBox(panel1, pos=(10, 100), size=(460, 500))
        self.playList.Bind(wx.EVT_LISTBOX_DCLICK, self.change_title)
        self.title_label = wx.StaticText(panel1, label="Currently not playing any song", pos=(10, 10))

        self.duration = wx.StaticText(panel1, label="00:00", pos=(360, 25))

        pygame.init()
        pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)

        self.Center()
        self.SetSize(600, 700)
        self.SetTitle("Player")

    def set_volume(self, event):
        handler = event.GetEventObject()
        value = handler.GetValue()
        self.volumeValue.SetLabel(str(value) + "%")
        value = value / 100
        pygame.mixer.music.set_volume(value)

    def add_to_playlist(self, event):
        with wx.FileDialog(self, "Add file to playlist", wildcard="Music files (*.mp3)|*.mp3|Wave files (*.wav)|.wav",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPaths()
            titles = file_dialog.GetFilenames()

            for i, e in zip(titles, path_name):
                position = self.playList.GetCount()
                self.playList.Insert(i, pos=position)
                self.tracks[i] = e

    def delete_track(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track = self.playList.GetSelection()
            delete_track = self.playList.GetString(track)
            self.playList.Delete(track)
            self.tracks.pop(delete_track)
            if self.playList.GetCount() == 0:
                self.title_label.SetLabel("Currently not playing any song")

    def clear_playlist(self, event):
        self.playList.Clear()
        self.tracks.clear()
        self.title_label.SetLabel("Currently not playing any song")
        pygame.mixer.music.stop()

    def change_title(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            current_track = self.playList.GetSelection()
            current_track = self.playList.GetString(current_track)
            self.title_label.SetLabel(current_track)
            self.play_audio(wx.EVT_LISTBOX_DCLICK)

    def play_audio(self, event):

        if self.playList.GetSelection() != wx.NOT_FOUND:
            track_index = self.playList.GetSelection()
            track = self.playList.GetString(track_index)
            path = self.tracks[track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

        elif self.playList.GetSelection() == wx.NOT_FOUND:
            track_index = 0
            track = self.playList.GetString(track_index)
            path = self.tracks[track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def forward(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track_index = self.playList.GetSelection()
            self.playList.SetSelection(track_index + 1)
            track = self.playList.GetSelection()
            next_track = self.playList.GetString(track)
            path = self.tracks[next_track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        else:
            return

    def rewind(self, event):
        if self.playList.GetSelection() != wx.NOT_FOUND:
            track_index = self.playList.GetSelection()
            self.playList.SetSelection(track_index - 1)
            track = self.playList.GetSelection()
            next_track = self.playList.GetString(track)
            path = self.tracks[next_track]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        else:
            return

    def pause(self, event):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True


app = wx.App()
execute = Frame(None)
execute.Show()
app.MainLoop()

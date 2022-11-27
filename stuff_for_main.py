import datetime as dt
import time
import threading
import librosa
from pygame import mixer

mixer.init(buffer=1024)
from tkinter import *
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
a = []

import random

class Song:
    def __init__(self, path, ):
        self.path = path
        self.name = path.split('/')[-1]

    def __str__(self):
        return ''+self.name


class Interface:
    def __init__(self, master, canvas):

        self.can = canvas
        self.root = master
        self.choose_button = Button(master, text='Выбрать музыку', highlightthickness=0, activebackground='#ffae00',
                                    background='#ffae00', width=17, height=2, command=self.choose_music_first_time)
        self.userplaylist_button = Button(master, text='Мой плейлист', highlightthickness=0, activebackground='#ffae00',
                                          background='#ffae00', width=17, height=2, command=self.user_playlist)
        self.addplaylist_button = Button(master, text='Добавить в плейлист', highlightthickness=0,
                                         activebackground='#ffae00', background='#ffae00', width=17, height=2,
                                         command=self.add_to_playlist)

        self.choose_button.place(relx=0.15, rely=0.02)
        self.userplaylist_button.place(relx=0.35, rely=0.02)
        self.addplaylist_button.place(relx=.55, rely=0.02)

        self.choose_button.bind('<Leave>', self.button_hover_leave)
        self.choose_button.bind('<Enter>', self.button_hover_enter)

        self.userplaylist_button.bind('<Leave>', self.button_hover_leave)
        self.userplaylist_button.bind('<Enter>', self.button_hover_enter)

        self.addplaylist_button.bind('<Leave>', self.button_hover_leave)
        self.addplaylist_button.bind('<Enter>', self.button_hover_enter)
        self.gragient = ['#FFCA69', '#FFC04B', '#FFB630', '#FFA500', '#E89600']
        self.music_now = ''
        self.music_now_playing = False
        self.playlist_work = False
        self.root.update()
        self.playlist = []
        self.start = True
        self.thread = threading.Thread(target=self.loop_music)
        self.thread.daemon = True
        self.thread_stop_now = False


    def button_hover_enter(self, event):
        for i in self.gragient:
            event.widget.configure(background=i)
            self.root.update()
            time.sleep(0.02)

    def button_hover_leave(self, event):
        event.widget.configure(background='#ffae00')

    def animation(self, ):
        x_choose, y_choose = 15, 1
        for i in range(0, 10):
            self.choose_button['width'] += 1
            self.choose_button['height'] += 1
            x_choose -= 5
            y_choose -= 5
            self.choose_button.place(y=y_choose, x=x_choose)
            self.userplaylist_button['width'] += 1
            self.userplaylist_button['height'] += 1

            self.addplaylist_button['width'] += 1
            self.addplaylist_button['height'] += 1
            self.root.update()
            time.sleep(0.01)
        for i in range(0, 10):
            self.choose_button['width'] -= 1
            self.choose_button['height'] -= 1
            x_choose += 5
            y_choose += 5

            self.choose_button.place(y=y_choose, x=x_choose)
            self.userplaylist_button['width'] -= 1
            self.userplaylist_button['height'] -= 1

            self.addplaylist_button['width'] -= 1
            self.addplaylist_button['height'] -= 1
            self.root.update()
            time.sleep(0.01)

    def choose_music_first_time(self):
        self.music_now = tkinter.filedialog.askopenfilename()
        while self.music_now.split('.')[-1] != 'mp3' and self.music_now:
            messagebox.showerror('Вы выбрали не mp3 файл', "Попробуйте еще")
            self.music_now = tkinter.filedialog.askopenfilename()
        if self.music_now:
            self.label = Label(self.root, text=self.music_now.split('/')[-1], )
            self.label.place(relx=0.42, rely=0.38)
            mixer.music.unload()
            mixer.music.load(self.music_now)

            self.icon_stop_music = Image.open('np.png')
            self.icon_stop_music = ImageTk.PhotoImage(self.icon_stop_music.resize((30, 30)))
            self.stop_music = Button(self.root, image=self.icon_stop_music, highlightthickness=0, background='#ffffff',
                                     activebackground='#ffffff', border=-1, command=self.stop_music)
            self.stop_music.place(rely=0.73, relx=0.46, width=40, height=40)
            hah = self.can.create_line(600, 500, 600, 300, fill='#808080', capstyle='round', width=2)
            self.hah_1 = self.can.create_oval(578, 365, 622, 410, fill='#f0f8ff')
            self.can.bind('<B1-Motion>', self.volume)
            self.choose_button.configure(command=self.choose_music)
            self.matrix_labels = [[Label(self.root, background='whitesmoke', width=1, pady=0.2) for x in range(10)] for y in
                             range(8)]
            self.can.create_rectangle(30, 90, 240, 280, fill='whitesmoke')
            y = 250
            for i in self.matrix_labels:
                x = 60
                for label in i:
                    label.place(x=x, y=y)
                    x += 16
                y -= 25

            y, sr = librosa.load(self.music_now, sr=44100)
            tempo, beat_frames = librosa.beat.beat_track(y, sr=sr)
            self.beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            print(self.beat_times)


    def loop_music(self):
        for x in self.beat_times:
            while 1:
                if self.thread_stop_now:
                    return None
                if (x -0.1) <= mixer.music.get_pos()/1000 <= (x+0.1):
                    if self.one_frame_of_bit():
                        break


    def choose_music(self, listbox=None):
        self.can.unbind('<B1-Motion>')
        self.label.destroy()
        if listbox is None:
            self.music_now = tkinter.filedialog.askopenfilename()
            self.label = Label(self.root, text=self.music_now.split('/')[-1], )
            mixer.music.unload()
            mixer.music.load(self.music_now)
            self.label.place(relx=0.42, rely=0.38)
            self.start = 1
        else:

            self.label = Label(self.root, text=listbox[0])
            mixer.music.unload()
            mixer.music.load(self.playlist[listbox[1][0]].path)
            self.label.place(relx=0.42, rely=0.38)
            self.start = 1
        self.can.bind('<B1-Motion>', self.volume)

    def bind_listbox(self, event):

        self.choose_music((self.playlist_listbox.get(self.playlist_listbox.curselection()), self.playlist_listbox.curselection()))

        return True

    def stop_music(self):
        if self.start:
            mixer.music.play()
            self.start = 0

        if not self.music_now_playing:
            mixer.music.unpause()
            self.music_now_playing = True
            self.thread.start()
        else:
            mixer.music.pause()
            self.music_now_playing = False
            self.thread_stop_now = True
            self.thread = threading.Thread(target=self.loop_music)
            self.thread.daemon = True

    def user_playlist(self):
        if not self.playlist_work:
            self.playlist_listbox = Listbox(self.root, relief='sunken', height=15, width=25)
            for i in self.playlist:
                self.playlist_listbox.insert(0, i)
            self.playlist_listbox.place(rely=0.6, relx=0.05)
            self.playlist_work = True
            self.playlist_listbox.bind('<<ListboxSelect>>', self.bind_listbox)

        else:
            self.playlist_listbox.destroy()
            self.playlist_work = False

    def add_to_playlist(self):
        if not self.music_now:
            messagebox.showwarning('Hmmm', 'Нечего добавить')

        else:
            self.playlist.append(Song(self.music_now))
            return True

    def one_frame_of_bit(self):
        random_choose = random.choice(self.matrix_labels[0][2:8])
        random_choose_index = self.matrix_labels[0].index(random_choose)
        random_choose_height = random.choice([3, 4,5,6, 7, 8])
        buffer = []
        side_right = random_choose_height - random.choice([2,1])
        side_left = random_choose_height - random.choice([2,1])
        for i in range(random_choose_height):
            self.matrix_labels[i][random_choose_index].configure(background='orange')
            time.sleep(0.008)
            self.root.update()
            buffer.append((i, random_choose_index))
            if i < side_right:
                self.matrix_labels[i][random_choose_index+1].configure(background='orange')
                time.sleep(0.008)
                self.root.update()
                buffer.append((i, random_choose_index+1))
            if i < side_left:
                self.matrix_labels[i][random_choose_index - 1].configure(background='orange')
                time.sleep(0.008)
                self.root.update()
                buffer.append((i, random_choose_index-1))
            if i < (side_left - 2):
                self.matrix_labels[i][random_choose_index - 2].configure(background='orange')
                time.sleep(0.008)
                self.root.update()
                buffer.append((i, random_choose_index-2))
            if i < (side_right - 1):
                self.matrix_labels[i][random_choose_index + 2].configure(background='orange')
                time.sleep(0.008)
                self.root.update()
                buffer.append((i, random_choose_index+2))
        for x in buffer[::-1]:
            self.matrix_labels[x[0]][x[1]].configure(background='whitesmoke')
            time.sleep(0.005)
            self.root.update()

        return 1

    def volume(self, event):
        coords = event.widget.coords(self.hah_1)
        mouse_y = self.can.winfo_pointery() - self.can.winfo_rooty()
        mouse_x = self.can.winfo_pointerx() - self.can.winfo_rootx()
        print(mixer.music.get_pos())
        if 310 <= mouse_y <= 450 and 580 <= mouse_x <= 620:
            if coords[1] < mouse_y:
                self.can.move(self.hah_1, 0, (mouse_y - coords[1]))
            else:
                self.can.move(self.hah_1, 0, -(coords[1] - mouse_y))
                print('Выбрано другое')
            if 310 <= mouse_y <= 340:
                mixer.music.set_volume(0.9)
            elif 340 <= mouse_y <= 380:
                mixer.music.set_volume(0.6)
            elif 380 <= mouse_y <= 400:
                mixer.music.set_volume(0.3)
            elif 400 <= mouse_y <= 420:
                mixer.music.set_volume(0.15)
            elif 420 <= mouse_y <= 440:
                mixer.music.set_volume(0.07)
            elif 440 <= mouse_y <= 450:
                mixer.music.set_volume(0.0)



# def create_image(canvas, coords):
#     image = canvas.create_image(coords[0], coords[1], image=coords[2])
#     return image
#
#
# def animation(master, canvas, image, speed=(1, 1), anim_delay=3, canvas_image=False, button=False):
#     size_image_x, size_image_y = image.size
#     coords_x, coords_y = 120, 120
#     map_animation = {}
#     x_velocity, y_velocity = speed
#     if button:
#         button.destroy()
#     time_now = dt.datetime.now().time()
#     time_animation = dt.timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second + anim_delay)
#
#     imagtk = ImageTk.PhotoImage(image)
#     my_image = canvas.create_image(size_image_x, size_image_y, image=imagtk, anchor=N)
#     if not canvas_image:
#         canvas.delete(canvas_image)
#         my_image = canvas_image
#
#     time_nower = dt.datetime.now().time()
#     for_anim = dt.timedelta(hours=time_nower.hour, minutes=time_nower.minute, seconds=time_nower.second)
#
#     while for_anim <= time_animation:
#         if for_anim <= time_animation - dt.timedelta(seconds=anim_delay / 3):
#             canvas.delete(my_image)
#             coords_x += 1
#             coords_y += 1
#             map_animation[str(coords_y)] = coords_x
#             size_image_x += 1
#             size_image_y += 1
#             size = size_image_x, size_image_y
#             imagtk = ImageTk.PhotoImage(image.resize(size))
#             my_image = canvas.create_image(coords_x, coords_y, image=imagtk)
#             canvas.move(my_image, x_velocity, y_velocity)
#
#         else:
#             canvas.delete(my_image)
#             coords_x += 1
#             coords_y += 1
#             map_animation[str(coords_y)] = coords_x
#             size_image_x += 0.4
#             size_image_y += 0.4
#             size = size_image_x, size_image_y
#             imagtk = ImageTk.PhotoImage(image.resize(size))
#             my_image = canvas.create_image(coords_x, coords_y, image=imagtk)
#             canvas.move(my_image, x_velocity * 1.1, y_velocity * 1.1)
#         time_nower = dt.datetime.now().time()
#         for_anim = dt.timedelta(hours=time_nower.hour, minutes=time_nower.minute, seconds=time_nower.second)
#         master.update()
#
#     print(map_animation)

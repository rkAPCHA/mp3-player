import json
import time
from tkinter import *
from tkinter import filedialog
from stuff_for_main import Interface
from PIL import Image, ImageTk
from pygame import mixer
mixer.init(buffer=1024)

import base64

# from stuff_for_main import animation





# Настройки программы
WIDTH = 800
HEIGHT = 700
xVelocity = -0.7
yVelocity = 1

SIZE_DISK_X = 233
SIZE_DISK_Y = 217

# Сама программа
root = Tk()
root.title('Best MP3-plr')
root.geometry(f'{WIDTH}x{HEIGHT}')
root.configure(background='#ffffff')

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white', highlightbackground='#ffffff',
                    highlightcolor='#ffffff')
canvas.place(relx=0.0)

from PIL import Image

image = Image.open('disk.png')
imagetk = ImageTk.PhotoImage(image)
disk = canvas.create_image(120, 110, image=imagetk)
rect = canvas.create_rectangle(600,300,100,0, fill='#FF6600', outline='#ffffff', )
canvas.move(rect, 0, -500)





def drag(event):
    global disk
    coords = event.widget.coords(disk)

    mouse = canvas.winfo_pointery() - canvas.winfo_rooty()

    if 100 <= mouse <= 400:
        if coords[1] < mouse :
            canvas.move(rect,0, mouse-coords[1])
            canvas.move(disk, (mouse - coords[0]), (mouse - coords[1]))

        else:
            canvas.move(rect, 0, -(coords[0]-mouse))
            event.widget.move(disk, -(coords[0]-mouse), -(coords[1]-mouse) )
            print('Выбрано другое')
    elif mouse >= 400:
        canvas.unbind('<B1-Motion>')

        inter = Interface(root, canvas)

        inter.animation()




canvas.bind('<B1-Motion>', drag)




# label_1 = Label(root, background='#F3A505')
# label_1.configure(width=1,pady=0.2)
# label_1.place(x=60, y=230)
# label_2 = Label(root, background='#F3A505')
# label_2.configure(width=1,pady=0.2)
# label_2.place(x=60, y=205)


root.mainloop()


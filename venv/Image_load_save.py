from tkinter import *
from tkinter import filedialog
import tkinter
import os
import cv2

"""
root = tkinter.Tk() # 创建一个Tkinter.Tk()实例
root.withdraw() # 将Tkinter.Tk()实例隐藏
default_dir = r"/home/pbihao/Pictures"
file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
image = cv2.imread(file_path)
cv2.imshow("sdf",image)
cv2.waitKey(0)
"""
default_dir = r"/home/pbihao/Pictures"
def load():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile(title = u'加载图片', initialdir = (os.path.expanduser(default_dir)))
    return str(file_path)
def save():
    file_name = filedialog.asksaveasfilename(title = u'保存图片', initialdir = (os.path.expanduser(default_dir)),
                                             filetypes = [("PNG", '.png'), ("BMP", '.bmp'), ("GIF", '.gif'),
                                                          ("JPG", '.jpg'), ("JPEG", '.jpeg')])
    return str(file_name)

load()
save()
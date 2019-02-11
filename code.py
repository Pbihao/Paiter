from Data import *
import math
import pygame
from pygame.locals import *
import tkinter
from tkinter import filedialog
from tkinter import *
import os
import cv2

IMAGE_SIZE = pygame.Rect(100, 50, 1050, 900)

#加载和保存图片
default_dir = r"/home/pbihao/Pictures"
def load(screen):
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile(title = u'加载图片', initialdir = (os.path.expanduser(default_dir)))
    img = pygame.image.load(file_path.name).convert_alpha()
    screen.blit(img, IMAGE_SIZE.topleft)
#可改进：在加载图片以后可以根据画板的大小来对图片进行调节
#至于为什么我自己不做呢？懒
def save(screen):
    root = tkinter.Tk()
    root.withdraw()
    img = screen.subsurface(IMAGE_SIZE).copy()
    file_name = filedialog.asksaveasfilename(title = u'保存图片', initialdir = (os.path.expanduser(default_dir)),
                                             filetypes = [("PNG", '.png'), ("BMP", '.bmp'), ("GIF", '.gif'),
                                                          ("JPG", '.jpg'), ("JPEG", '.jpeg')])

    pygame.image.save(img, file_name)

#给出对角线两点，返回左上点和长宽
def calc_rect(p1, p2):
    ans = []
    ans.append(min(p1[0], p2[0]))
    ans.append(min(p1[1], p2[1]))
    ans.append(abs(p1[0] - p2[0]))
    ans.append(abs(p1[1] - p2[1]))
    return ans

def cut(screen):
    img = screen.subsurface(IMAGE_SIZE).copy()
    bg = None
    while True:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                if not IMAGE_SIZE.collidepoint(event.pos):
                    return
                elif bg == None:
                    bg = event.pos
            elif event.type == MOUSEMOTION:
                if bg == None:
                    continue
                screen.blit(img, IMAGE_SIZE.topleft)
                ans = calc_rect(bg, event.pos)
                rect = pygame.Rect(ans[0], ans[1], ans[2], ans[3])
                pygame.draw.rect(screen,COLOR_BLACK,rect,1)
            elif event.type == MOUSEBUTTONUP:
                if bg == None:
                    continue
                screen.blit(img, IMAGE_SIZE.topleft)
                ans = calc_rect(bg, event.pos)
                rect = pygame.Rect(ans[0], ans[1], ans[2], ans[3])
                pygame.draw.rect(screen, COLOR_BLACK, rect, 1)
                dst = screen.subsurface(rect).copy()
                pygame.draw.rect(screen, COLOR_WHITE, IMAGE_SIZE, 1000)

                screen.blit(dst, IMAGE_SIZE.topleft)
                rect[0] = IMAGE_SIZE.topleft[0]
                rect[1] = IMAGE_SIZE.topleft[1]
                pygame.draw.rect(screen, COLOR_WHITE, rect, 1)

                pygame.display.update()
                return


        pygame.display.update()


#实现了画笔的基本功能，至于橡皮擦其实就是白色的画笔
class Pen(object):
    def __init__(self, screen):
        self.drawing = False
        self.last_pos = None
        self.size = 3
        self.color = COLOR_BLACK
        self.screen = screen
    def get_size(self):
        return self.size
    def change_size(self, size):
        if size < 1:
            size = 1
        elif size > 32:
            size = 32
        self.size = size
    def get_color(self):
        return self.color
    def change_color(self, color):
        self.color = color
    def to_eraser(self):
        self.color = COLOR_WHITE
    def to_pen(self):
        self.color = COLOR_BLACK
    def start_draw(self, pos):
        self.last_pos = pos
        self.drawing = True
    def end_draw(self):
        self.drawing = False
    def get_points(self, pos):
        dx = (pos[0] - self.last_pos[0])
        dy = (pos[1] - self.last_pos[1])
        dz = math.sqrt(dx * dx + dy * dy)
        dx /= dz
        dy /= dz
        points = []
        points.append((self.last_pos[0], self.last_pos[1]))
        for i in range(int(dz)):
            points.append((points[-1][0] + dx, points[-1][1] + dy))
        points = map(lambda x : (int(x[0] + 0.5), int(x[1] + 0.5)), points)
        return list(set(points))
    def draw(self, pos):
        if self.drawing:
            now_color = self.color
            if not IMAGE_SIZE.collidepoint(pos):
                self.color = COLOR_WHITE
            points = self.get_points(pos)
            for p in points:
                pygame.draw.circle(self.screen, self.color, p, self.size)
            self.last_pos = pos
            self.color = now_color

#实现菜单模块的基本功鞥
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.pen = None
        self.rect_pen = pygame.Rect(SPACE, SPACE, BIG_SIZE, BIG_SIZE)
        self.rect_eraser = pygame.Rect(SPACE, SPACE + BIG_SIZE, BIG_SIZE, BIG_SIZE)
        self.rect_sizes = [pygame.Rect(SPACE + i * SMALL_SIZE, SPACE + BIG_SIZE * 2, SMALL_SIZE, SMALL_SIZE)
                         for i in range(2)]
        self.rect_color = [pygame.Rect(SPACE + SMALL_SIZE * (i % 2), SPACE + BIG_SIZE * 4 + SMALL_SIZE * (i / 2), SMALL_SIZE, SMALL_SIZE)
                           for i in range(16)]

        self.rect_load = pygame.Rect(SPACE, 544, BIG_SIZE, BIG_SIZE)
        self.rect_save = pygame.Rect(SPACE, 544 + BIG_SIZE + SPACE, BIG_SIZE, BIG_SIZE)
        self.rect_cut = pygame.Rect(SPACE, 544 + (BIG_SIZE + SPACE) * 2, BIG_SIZE, BIG_SIZE)


        self.i_pen = pygame.image.load("images/pen.png").convert_alpha()
        self.i_eraser = pygame.image.load("images/eraser.png").convert_alpha()
        self.i_sizes = [pygame.image.load("images/big.png").convert_alpha(),
                      pygame.image.load("images/small.png").convert_alpha()]
        self.i_load = pygame.image.load("images/load.png").convert_alpha()
        self.i_save = pygame.image.load("images/save.png").convert_alpha()
        self.i_cut = pygame.image.load("images/cut.png").convert_alpha()

    def set_pen(self, pen):
        self.pen = pen
    def draw(self):

        self.screen.blit(self.i_pen, self.rect_pen.topleft)
        self.screen.blit(self.i_eraser, self.rect_eraser.topleft)
        for i in range(2):
            self.screen.blit(self.i_sizes[i], self.rect_sizes[i].topleft)
        RECT = (SPACE, SMALL_SIZE + BIG_SIZE * 2 + SPACE, 64, 64)
        POS = (SPACE + int(BIG_SIZE / 2), SMALL_SIZE + int(BIG_SIZE * 2.5) + SPACE)
        self.screen.fill(COLOR_WHITE, RECT)
        pygame.draw.rect(self.screen, COLOR_BLACK, RECT, 1)
        pygame.draw.rect(self.screen, COLOR_BLACK, IMAGE_SIZE, 5)
        if self.pen.get_color() == COLOR_WHITE:
            pygame.draw.circle(self.screen, COLOR_BLACK, POS, self.pen.get_size(), 1)
        else:
            pygame.draw.circle(self.screen, self.pen.get_color(), POS, self.pen.get_size())
        for i in range(16):
            pygame.draw.rect(self.screen, COLORS[i], self.rect_color[i])
        self.screen.blit(self.i_load, self.rect_load.topleft)
        self.screen.blit(self.i_save, self.rect_save.topleft)
        self.screen.blit(self.i_cut, self.rect_cut.topleft)
    def click_button(self, pos):
        if self.rect_pen.collidepoint(pos):
            self.pen.to_pen()
            return
        if self.rect_eraser.collidepoint(pos):
            self.pen.to_eraser()
            return
        for i in range(2):
            if self.rect_sizes[i].collidepoint(pos):
                if i == 0:
                    self.pen.change_size(self.pen.get_size() + 1)
                else:
                    self.pen.change_size(self.pen.get_size() - 1)
                return
        for i in range(16):
            if self.rect_color[i].collidepoint(pos):
                self.pen.change_color(COLORS[i])
                return
        if self.rect_load.collidepoint(pos):
            load(self.screen)
            return
        if self.rect_save.collidepoint(pos):
            save(self.screen)
            return
        if self.rect_cut.collidepoint(pos):
            cut(self.screen)
            return


#整个程序的总控
class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode(PAITER_SIZE)
        self.screen.fill(COLOR_WHITE)
        pygame.display.set_caption("PBIHAO")
        self.pen = Pen(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_pen(self.pen)
        self.block = pygame.time.Clock()
    def run(self):
        while True:
            self.block.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] < 74:
                        self.menu.click_button(event.pos)
                    else:
                        self.pen.start_draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.pen.end_draw()
                elif event.type == MOUSEMOTION:
                    self.pen.draw(event.pos)
            self.menu.draw()
            pygame.display.update()




def main():
    paiter = Painter()
    paiter.run()

if __name__ == "__main__":
    main()
import random
import math
from time import sleep

import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Dead']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.hp = 2
        self.is_dead_animation_complete = False

    def update(self):
        if self.hp > 0:
            # 살아있는 경우 걷기 애니메이션
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
            if self.x > 1600:
                self.dir = -1
            elif self.x < 800:
                self.dir = 1
            self.x = clamp(800, self.x, 1600)
        else:
            if not self.is_dead_animation_complete:
                self.frame += 0.1
                if self.frame >= 9:
                    self.frame = 9
                    self.is_dead_animation_complete = True


    def draw(self):
        if self.hp == 2:
            if self.dir < 0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 200, 200)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 200, 200)
        elif self.hp == 1:
            if self.dir < 0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
        else:
            if not self.is_dead_animation_complete:
                Zombie.images['Dead'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                game_world.remove_object(self)





    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 50, self.y -100, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        # fill here
        if group == 'zombie:ball':
            self.hp -= 1
            if self.hp == 1:
                self.y -= 50


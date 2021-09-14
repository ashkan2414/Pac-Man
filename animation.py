import globals


class Animator:

    def __init__(self):
        self.animations = {None: None}
        self.current_animation = None
        self.current_frame = 0
        self.current_frame_num = 0
        self.current_time = 0
        self.finished = False

    def start(self):
        self.current_time = 0
        self.current_frame_num = 0

    def update(self):
        if self.current_animation and not self.finished:
            self.current_time += globals.delta_time

            if self.current_animation.loop:
                while self.current_time >= self.current_animation.duration:
                    self.current_time -= self.current_animation.duration
            else:
                self.finished = self.current_time >= self.current_animation.duration

            self.current_frame_num = round(self.current_time * self.current_animation.frame_rate)
            self.current_frame = self.current_animation.get_frame(self.current_frame_num)

    def get_current_frame(self):
        return self.current_frame

    def add_animation(self, animation):
        self.animations[animation.id] = animation

    def set_animation(self, animation_id):

        if self.current_animation and self.current_animation.id == animation_id:
            return

        if animation_id in self.animations:
            self.current_animation = self.animations.get(animation_id)
            self.finished = False
            self.current_frame_num = 0
            self.current_time = 0


class Animation:

    def __init__(self, id, frames, frame_rate, loop):
        self.id = id
        self.frames = frames
        self.frame_rate = frame_rate
        self.loop = loop
        self.duration = len(frames) / frame_rate

    def get_frame(self, frame_num):

        frame_num = round(frame_num)
        if self.loop:
            while frame_num >= len(self.frames):
                frame_num -= len(self.frames)
            while frame_num < 0:
                frame_num += len(self.frames)
        else:
            if frame_num >= len(self.frames):
                frame_num = len(self.frames)-1
            elif frame_num < 0:
                frame_num = 0

        return self.frames[frame_num]

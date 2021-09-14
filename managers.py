import globals
from settings import *
from enum_types import *


class TimedEventManager:
    on_going_calls = []

    @staticmethod
    def update():
        for timed_event in TimedEventManager.on_going_calls:
            timed_event.update()

    @staticmethod
    def add_timed_event(event, time):
        TimedEventManager.on_going_calls.append(TimedEvent(event, time))

    @staticmethod
    def remove_timed_event(timed_event):
        TimedEventManager.on_going_calls.remove(timed_event)

    @staticmethod
    def remove_timed_events_of_type(event_type):
        for timed_event in TimedEventManager.on_going_calls:
            if timed_event.event.type == event_type:
                TimedEventManager.on_going_calls.remove(timed_event)
                del timed_event


class TimedEvent:

    def __init__(self, event, time):
        self.timer = 0
        self.event = event
        self.time = time

    def update(self):
        self.timer += globals.delta_time
        if self.timer >= self.time:
            pygame.event.post(self.event)
            TimedEventManager.remove_timed_event(self)


class SoundManager:
    sounds = {}

    @staticmethod
    def init():
        for sound, file_name in SOUND_FILES.items():
            SoundManager.sounds[sound] = Sound(pygame.mixer.Sound(os.path.join(SOUND_FILE_PATH, file_name)))
            SoundManager.sounds.get(sound).sound.set_volume(SOUND_VOLUME.get(sound))

    @staticmethod
    def update():
        for sound in SoundManager.sounds.values():
            sound.update()

    @staticmethod
    def instant_stop():
        for sound in SoundManager.sounds.values():
            sound.instant_stop()


class Sound:

    def __init__(self, sound):
        self.sound = sound
        self.channel = None
        self.queue = False
        self.timer = 0

    def update(self):
        if not self.is_playing():
            self.channel = None
            if self.queue:
                self.queue = False
                self.play()

        if self.timer > 0:
            self.timer -= globals.delta_time
            if self.timer <= 0:
                self.play()

    def play(self, loops=0, playmode=SoundPlayMode.LAYER, time=0):

        if playmode == SoundPlayMode.RESTART:
            self.sound.stop()
            self.timer = 0
        elif playmode == SoundPlayMode.CONTINUE:
            if self.is_playing():
                self.queue = True
                return
        elif playmode == SoundPlayMode.TIMED:
            self.timer = time
            return

        self.channel = self.sound.play(loops)

    def instant_stop(self):
        self.sound.stop()
        self.stop()

    def stop(self):
        self.queue = False
        self.timer = 0

    def is_playing(self):
        return self.channel is not None and self.channel.get_busy() or self.timer > 0

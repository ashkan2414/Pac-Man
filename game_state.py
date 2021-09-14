from entity import *
from managers import *
from maze import *
from ui_elements import *


class StartMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)

        self.title_logo = Icon(self, BoundScale(0.5, 0.2, 0.7, 0.2), pygame.image.load(os.path.join(ICON_FILE_PATH, START_MENU_TITLE_LOGO)))
        self.child_game_components.append(self.title_logo)

        self.start_button = Button(self, BoundScale(0.55, 0.55, 0.4, 0.1),
                                   Animation(ButtonState.NORMAL, load_animation(START_BUTTON_NORMAL_ANIMATION), 15, True),
                                   Animation(ButtonState.HOVER, load_animation(START_BUTTON_HOVER_ANIMATION), 15, True),
                                   func=self.start_game)

        self.child_game_components.append(self.start_button)

        self.quit_button = Button(self, BoundScale(0.55, 0.65, 0.4, 0.1),
                                   Animation(ButtonState.NORMAL, load_animation(QUIT_BUTTON_NORMAL_ANIMATION), 15,
                                             True),
                                   Animation(ButtonState.HOVER, load_animation(QUIT_BUTTON_HOVER_ANIMATION), 15, True),
                                   func=self.quit_game)

        self.child_game_components.append(self.quit_button)

    @staticmethod
    def start_game():
        globals.game.set_game_state(GameStateType.GAME_MENU)

    @staticmethod
    def quit_game():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()


class SettingMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)


class GameMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)

        maze_scale = BoundScale(0.5, 0.54, 0.95, 0.87)

        self.maze = Maze(self, maze_scale)
        self.child_game_components.append(self.maze)
        self.ghosts = {GhostType.BLINKY: Blinky(self, maze_scale),
                       GhostType.INKY: Inky(self, maze_scale),
                       GhostType.PINKY: Pinky(self, maze_scale),
                       GhostType.CLYDE: Clyde(self, maze_scale)}
        self.child_game_components += list(self.ghosts.values())
        self.pacman = Pacman(self, maze_scale)
        self.child_game_components.append(self.pacman)

        self.score_text = Text(self, BoundScale(0.14, 0.05, 0.15, 0.04), "", WHITE, FONT_NAME, 200, True)
        self.child_game_components.append(self.score_text)

        self.highscore_text_label = Text(self, BoundScale(0.5, 0.03, 0.15, 0.04), "HIGH SCORE", WHITE, FONT_NAME, 200, True)
        self.child_game_components.append(self.highscore_text_label)

        self.highscore_text = Text(self, BoundScale(0.5, 0.07, 0.15, 0.04), "", WHITE, FONT_NAME, 200, True)
        self.child_game_components.append(self.highscore_text)

        self.life_bar = IconBar(self, BoundScale(0.86, 0.05, 0.15, 0.04),
                                pygame.image.load(os.path.join(ICON_FILE_PATH, PACMAN_LIFE_ICON_IMAGE)), PACMAN_LIVES)
        self.child_game_components.append(self.life_bar)

        self.game_over_text = Text(self, BoundScale(0.5, 0.6, 0.3, 0.1), "GAME OVER", RED, FONT_NAME, 200, True)
        self.child_game_components.append(self.game_over_text)

        self.frightened_mode = False
        self.current_bg_sound = None
        self.play_bg_sound = False

    def start(self):
        self.set_enable(True)
        self.game_over_text.set_enable(False)

        self.game_start()
        globals.points_left = 0
        super().start()

    def process_event(self, event):
        if event.type == GAME_START:
            self.play_bg_sound = True
        elif event.type == FRIGHTENED_MODE_START:
            self.frightened_mode = True
        elif event.type == FRIGHTENED_MODE_END:
            self.frightened_mode = False
        elif event.type == GHOST_EATEN_START:
            self.play_bg_sound = False
        elif event.type == GHOST_EATEN_END:
            self.play_bg_sound = True
        elif event.type == LEVEL_RESET:
            self.game_start()
        elif event.type == LEVEL_FINISH:
            self.play_bg_sound = False
            TimedEventManager.add_timed_event(pygame.event.Event(NEXT_LEVEL), LEVEL_FINISH_DURATION)
            SoundManager.sounds.get(SoundTrack.LEVEL_FINISH).play()
        elif event.type == NEXT_LEVEL:
            self.start()
        elif event.type == GAME_OVER:
            self.game_over_text.set_enable(True)
            TimedEventManager.add_timed_event(pygame.event.Event(RETURN_TO_START), GAME_OVER_DURATION)
        elif event.type == RETURN_TO_START:
            self.parent.set_game_state(GameStateType.START_MENU)
        super().process_event(event)

    def update(self):
        if self.play_bg_sound:
            if globals.ghosts_eaten > 0:
                self.set_background_sound(SoundTrack.GHOST_RETREATING)
            else:
                if self.frightened_mode:
                    self.set_background_sound(SoundTrack.SCARED_GHOST_SIREN)
                else:
                    self.set_background_sound(SoundTrack.GHOST_SIREN)
        else:
            self.set_background_sound(None)

        self.score_text.set_text(add_text_digit_padding(str(self.pacman.points), DEFAULT_POINTS_DIGITS))
        self.highscore_text.set_text(add_text_digit_padding(str(globals.highscore), DEFAULT_POINTS_DIGITS))
        self.life_bar.set_current_num(self.pacman.lives)
        super().update()

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()

    def set_background_sound(self, sound):
        if sound == self.current_bg_sound:
            return
        if self.current_bg_sound is not None:
            SoundManager.sounds.get(self.current_bg_sound).instant_stop()
        self.current_bg_sound = sound
        if self.current_bg_sound is not None:
            SoundManager.sounds.get(self.current_bg_sound).play(-1)

    def game_start(self):
        globals.ghosts_eaten = 0
        self.frightened_mode = False
        self.current_bg_sound = None
        self.play_bg_sound = False
        TimedEventManager.add_timed_event(pygame.event.Event(GAME_START), GAME_START_DURATION)
        SoundManager.sounds.get(SoundTrack.GAME_START).play()

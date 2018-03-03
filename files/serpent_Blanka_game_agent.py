from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey
from serpent.sprite_locator import SpriteLocator
sprite_locator = SpriteLocator()
import serpent.cv
import offshoot

import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

from .helpers.terminal_printer import TerminalPrinter

class SerpentBlankaGameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

        self.printer = TerminalPrinter()
        self.sprite_locator = SpriteLocator()

    def setup_play(self):
        move_inputs = {
            "MOVE UP": [KeyboardKey.KEY_W],
            "MOVE LEFT": [KeyboardKey.KEY_A],
            "MOVE DOWN": [KeyboardKey.KEY_S],
            "MOVE RIGHT": [KeyboardKey.KEY_D],
            "MOVE TOP-LEFT": [KeyboardKey.KEY_W, KeyboardKey.KEY_A],
            "MOVE TOP-RIGHT": [KeyboardKey.KEY_W, KeyboardKey.KEY_D],
            "MOVE DOWN-LEFT": [KeyboardKey.KEY_S, KeyboardKey.KEY_A],
            "MOVE DOWN-RIGHT": [KeyboardKey.KEY_S, KeyboardKey.KEY_D],
            "DON'T MOVE": []
        }
        fight_inputs = {
            "L-PUNCH": [KeyboardKey.KEY_G],
            "M-PUNCH": [KeyboardKey.KEY_H],
            "H-PUNCH": [KeyboardKey.KEY_J],
            "L-KICK": [KeyboardKey.KEY_B],
            "M-KICK": [KeyboardKey.KEY_N],
            "H-KICK": [KeyboardKey.KEY_M],
        }

        self.printer.add("Game started")
        self.printer.flush()

    def handle_play(self, game_frame):
        start_button_location = sprite_locator.locate(sprite=self.game.sprites['SPRITE_MENU_BUTTON_START'], game_frame=game_frame)
        training_button_location = sprite_locator.locate(sprite=self.game.sprites['SPRITE_MENU_BUTTON_TRAINING'], game_frame=game_frame)

        if (start_button_location):
            self.handle_play_readnews(game_frame)
        elif (training_button_location):
            self.handle_play_start_training(game_frame)
        else:
            return

    def handle_play_readnews(self, game_frame):
        print ("Reading News...")
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_B)
        time.sleep(1)

    def handle_play_start_training(self, game_frame):
        print ("Starting Training Mode")
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_S)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_D)
        time.sleep(0.1)
        self.input_controller.tap_key(KeyboardKey.KEY_B)
        time.sleep(1)

    def handle_play_level_select(self, game_frame):
        print ("Choosing Level")
        self.input_controller.tap_key(KeyboardKey.KEY_B)

    def handle_play_player_select(self, game_frame):
        print ("Choosing Player")
        self.input_controller.tap_key(KeyboardKey.KEY_B)

    def handle_play_fight_training(self, game_frame):
        print("Fight Training in Progress")

        fightzone_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["FIGHTZONE"])
        timer_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["TIMER"])

        p1_health_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P1_HEALTH"])
        p1_trigger_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P1_TRIGGER"])
        p1_ca_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P1_CA"])
        p1_dizzy_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P1_DIZZY"])

        p2_health_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P2_HEALTH"])
        p2_trigger_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P2_TRIGGER"])
        p2_ca_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P2_CA"])
        p2_dizzy_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["P2_DIZZY"])

        pp.pprint(fightzone_frame)

        self.visual_debugger.store_image_data(
            fightzone_frame,
            image_shape = fightzone_frame.shape,
            bucket = "0"
        )

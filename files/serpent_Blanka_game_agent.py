from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey
from serpent.machine_learning.context_classification.context_classifiers import CNNInceptionV3ContextClassifier
from serpent.sprite_locator import SpriteLocator
import serpent.ocr as ocr
import serpent.cv
import skimage
import numpy as np

from .helpers.terminal_printer import TerminalPrinter

import itertools
import collections
import offshoot

class SerpentBlankaGameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

        self.printer = TerminalPrinter()

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


        plugin_path = offshoot.config["file_paths"]["plugins"]

        context_classifier_path = f"{plugin_path}/SerpentBlankaGameAgentPlugin/files/ml_models/context_classifier.model"

        from serpent.machine_learning.context_classification.context_classifiers.cnn_inception_v3_context_classifier import CNNInceptionV3ContextClassifier
        context_classifier = CNNInceptionV3ContextClassifier(input_shape=(640, 480, 3))

        context_classifier.prepare_generators()
        context_classifier.load_classifier(context_classifier_path)

        self.machine_learning_models["context_classifier"] = context_classifier

        self.printer.add("Game started")
        self.printer.flush()

    def handle_play(self, game_frame):
        context = self.machine_learning_models["context_classifier"].predict(game_frame.frame)      

        if context is None:
            context = "Unknown"

        if context.startswith("main_"):
            self.handle_play_main_menu(game_frame)

        if context.startswith("level_"):
            self.handle_play_level_select(game_frame)

        if context.startswith("player_"):
            self.handle_play_player_select(game_frame)

        if context.startswith("fight_"):
            self.handle_play_fight_training(game_frame)

    def handle_play_main_menu(self, game_frame):
        print ("Starting Training Mode")
        for name, sprite in self.game.sprites.items():
            print(name)

    def handle_play_level_select(self, game_frame):
        print ("Choosing Level")
        self.input_controller.tap_key(KeyboardKey.KEY_B)

    def handle_play_player_select(self, game_frame):
        print ("Choosing Player")
        self.input_controller.tap_key(KeyboardKey.KEY_B)

    def handle_play_fight_training(self, game_frame):
        print("Fight Training in Progress")

        time_area_frame = serpent.cv.extract_region_from_image(game_frame.frame, self.game.screen_regions["time"])

        self.visual_debugger.store_image_data(
            game_frame.frame,
            image_shape = game_frame.frame.shape,
            bucket = "0"
        )

        self.visual_debugger.store_image_data(
            time_area_frame,
            image_shape = time_area_frame.shape,
            bucket = "1"
        )
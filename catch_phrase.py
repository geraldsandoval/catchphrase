
import json
from signal import signal, SIGTERM, SIGHUP, pause
import RPi.GPIO as GPIO 
from rpi_lcd import LCD
from time import sleep
from time import time
from os import listdir
from os.path import isfile, join
import random
from threading import Thread

# COMICS, DISNEY, ENTERTAINMENT, EVERYTHING, FANTASY, HORROR, SCIFI, TECH


class PhraseCategory(object):
    def __init__(self, name, categories, phrases):
         self.name = name
         self.categories = categories
         self.phrases = phrases


class CatchPhrase(object):
    def __init__(self):
        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)
        self.game_state = "IDLE"
        self.category_index = 0
        self.current_category = ""
        self.current_phrase = ""
        self.phrase_bank = []
        self.categories = []
        self.phrases_for_round = []
        self.team_one_score = 0
        self.team_two_score = 0
        self.winning_score = 7
        self.lcd = LCD(address=0x27)
        self.timer = None
        sleep(1)
        self.init_lcd()
        self.init_gpio()
        self.game_loop()

    def safe_exit(self, signum, frame):
        self.lcd.clear()
        GPIO.cleanup() 
        exit(1)

    def init_lcd(self):
        self.lcd.text("Hello!", 1)
        self.lcd.text("Select Category!", 2)

    def init_gpio(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BOARD)

        self.init_button(gpio_pin=29, callback_func=self.skip)
        self.init_button(gpio_pin=31, callback_func=self.choose_category)
        self.init_button(gpio_pin=35, callback_func=self.add_point_team_one)
        self.init_button(gpio_pin=37, callback_func=self.add_point_team_two)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(12, GPIO.LOW)

    def init_button(self, gpio_pin, callback_func):
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=callback_func, bouncetime=1000)

    def get_phrase_files(self):
        phrases_path = "./phrases/"
        return [f for f in listdir(phrases_path) if isfile(join(phrases_path, f))]

    def read_game_database(self):
        phrase_files = self.get_phrase_files()
        for phrase_file in phrase_files:
            with open("./phrases/" + phrase_file) as json_phrases:
                self.add_phrases_to_game(phrases=json.load(json_phrases))

    def add_phrases_to_game(self, phrases):
        self.phrase_bank.append(PhraseCategory(phrases['name'], phrases['categories'], phrases['phrases']))
        for category in phrases['categories']:
            if category not in self.categories:
                self.categories.append(category)
                
    def start_game(self):
        for bank in self.phrase_bank:
            if self.current_category in bank.categories:
                self.phrases_for_round += bank.phrases
        self.game_state = "ACTIVE"
        self.get_new_phrase()
        self.timer = Thread(target=self.start_timer, daemon=True)
        self.timer.start()

    def start_timer(self):
        start = time()
        end = start + 60
        while time() < end: 
            if end - time() > 30:
                print("t>30")
                GPIO.output(12, GPIO.HIGH)
                sleep(0.2)
                GPIO.output(12, GPIO.LOW)
                sleep(0.8)
            elif 30 > end - time() > 15:
                print("30 > t > 15")
                GPIO.output(12, GPIO.HIGH)
                sleep(0.2)
                GPIO.output(12, GPIO.LOW)
                sleep(0.3)
            else:
                print("15 > t")
                GPIO.output(12, GPIO.HIGH)
                sleep(0.2)
                GPIO.output(12, GPIO.LOW)
                sleep(0.05)
            GPIO.output(12, GPIO.LOW)
        self.game_state = "IDLE"
        self.phrases_for_round = []
        self.update_lcd("WHO WON THE ROUND?!")

    def get_new_phrase(self):
        phrase_index = random.randint(0, len(self.phrases_for_round) - 1)
        self.current_phrase = self.phrases_for_round[phrase_index]
        self.update_lcd(self.current_phrase)
        del self.phrases_for_round[phrase_index]

    def update_lcd(self, text):
        self.lcd.clear()
        self.lcd.text(text[0:16], 1)
        self.lcd.text(text[16:32], 2)

    def skip(self, channel):
        print("SKIP PRESSED")
        if self.game_state == "IDLE":
            self.update_lcd("SKIP PRESSED")
            self.start_game()
        elif self.game_state == "ACTIVE":
            self.get_new_phrase()
        sleep(0.25)

    def choose_category(self, channel):
        if self.game_state == "IDLE":
            print("CATEGORY PRESSED")
            self.current_category = self.categories[self.category_index % len(self.categories)]
            self.update_lcd(self.current_category)
            self.category_index += 1
        sleep(0.5)

    def add_point(self, team):
        if team == 1:
            self.team_one_score += 1
            if self.team_one_score == self.winning_score:
                self.update_lcd(f"TEAM ONE WON!")
                self.team_one_score = 0
                self.team_two_score = 0
                self.game_state = "IDLE"
            else:
                self.update_lcd(f"TEAM ONE M'LORD! (T1: {self.team_one_score}, T2: {self.team_two_score})")
                sleep(2)
        else:
            self.team_two_score += 1
            if self.team_two_score == self.winning_score:
                self.update_lcd(f"TEAM TWO WON!")
                self.team_one_score = 0
                self.team_two_score = 0
                self.game_state = "IDLE"
            else:
                self.update_lcd(f"TEAM TWO M'LORD! (T1: {self.team_one_score}. T2: {self.team_two_score})")
                sleep(2)
        self.update_lcd("Select Category!")

    def add_point_team_one(self, channel):
        print("TEAM ONE PRESSED")
        if self.game_state == "IDLE":
            self.team_one_score += 1
            if self.team_one_score == self.winning_score:
                self.update_lcd(f"TEAM ONE WON!")
                self.team_one_score = 0
                self.team_two_score = 0
                self.game_state = "IDLE"
                sleep(2)
            else:
                self.update_lcd(f"TEAM ONE M'LORD! (T1: {self.team_one_score}, T2: {self.team_two_score})")
                sleep(2)
            self.update_lcd("Select Category!")

    def add_point_team_two(self, channel):
        print("TEAM TWO PRESSED")
        if self.game_state == "IDLE":
            self.team_two_score += 1
            if self.team_two_score == self.winning_score:
                self.update_lcd(f"TEAM TWO WON!")
                self.team_one_score = 0
                self.team_two_score = 0
                self.game_state = "IDLE"
                sleep(2)
            else:
                self.update_lcd(f"TEAM TWO M'LORD! (T1: {self.team_one_score}. T2: {self.team_two_score})")
                sleep(2)
            self.update_lcd("Select Category!")

    def start(self, channel):
        pass

    def game_loop(self):
        self.read_game_database()
        while True:
            try:
                sleep(0.1)
            except KeyboardInterrupt:
                break
        self.lcd.clear()
        GPIO.cleanup() 
        exit(1)
        

if __name__ == "__main__":
    catch_phrase = CatchPhrase()
    #catch_phrase.read_game_database()
    #catch_phrase.print_phrases()


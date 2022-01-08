
import json
from signal import signal, SIGTERM, SIGHUP, pause
import RPi.GPIO as GPIO 
from rpi_lcd import LCD
from time import sleep

# COMICS, DISNEY, ENTERTAINMENT, EVERYTHING, FANTASY, HORROR, SCIFI, TECH


class CatchPhrase(object):
    def __init__(self):
        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)
        self.available_categories = {}
        self.phrases = {}
        self.team_one_score = 0
        self.team_two_score = 0
        self.lcd = LCD(address=0x27)
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

    def init_button(self, gpio_pin, callback_func):
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=callback_func, bouncetime=1000)


    '''
    # TODO: manage phrase database/handling
    def read_game_database(self):
        with open("phrases/starwars.json") as json_phrases:
            self.add_phrases_to_game(phrases=json.load(json_phrases))

    def add_phrases_to_game(self, phrases):
        for phrase, categories in phrases.items():
            self.phrases[phrase] = categories

    def print_phrases(self):
        for phrase, categories in self.phrases.items():
            print(phrase)
    '''

    def update_lcd(self, text):
        #self.lcd.clear()
        self.lcd.text(text[0:16], 1)
        self.lcd.text(text[16:32], 2)

    def skip(self, channel):
        print("SKIP PRESSED")
        #self.update_lcd("SKIP PRESSED")
        sleep(0.5)

    def choose_category(self, channel):
        print("CATEGORY PRESSED")
        #self.update_lcd("CATEGORY PRESSED")
        sleep(0.5)

    def add_point_team_one(self, channel):
        print("TEAM ONE PRESSED")
        #self.update_lcd("TEAM ONE PRESSED")
        sleep(0.5)

    def add_point_team_two(self, channel):
        print("TEAM TWO PRESSED")
        #self.update_lcd("TEAM TWO PRESSED")
        sleep(0.5)

    def start(self, channel):
        pass

    def game_loop(self):
        input("here")
        #while True:
        #    sleep(0.3)


if __name__ == "__main__":
    catch_phrase = CatchPhrase()
    #catch_phrase.read_game_database()
    #catch_phrase.print_phrases()


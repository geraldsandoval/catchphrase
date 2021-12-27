
import json
from enum import Enum

# COMICS, DISNEY, ENTERTAINMENT, EVERYTHING, FANTASY, HORROR, SCIFI, TECH


class CatchPhrase(object):
    def __init__(self):
        self.phrases = {}
        self.already_played = []
        self.team_one_score = 0
        self.team_two_score = 0

    def read_game_database(self):
        with open("phrases/starwars.json") as json_phrases:
            self.add_phrases_to_game(phrases=json.load(json_phrases))

    def add_phrases_to_game(self, phrases):
        for phrase, categories in phrases.items():
            self.phrases[phrase] = categories

    def print_phrases(self):
        for phrase, categories in self.phrases.items():
            print(phrase)

    def skip(self):
        pass

    def choose_category(self):
        pass

    def add_point(self, team):
        # TODO: Say "TEAM X MY LORD", where x is the team number
        pass

    def start(self):
        pass


if __name__ == "__main__":
    catch_phrase = CatchPhrase()
    catch_phrase.read_game_database()
    catch_phrase.print_phrases()

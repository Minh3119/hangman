import os
import io
import time
from colorama import init, Fore
import random

init(autoreset=True)
STATUS = ("correct","wrong","duplicated","win")
QUIT = {"quit","esc","exit","forfeit"}

class Game():
    def __init__(self, hearts:int) -> None:
        self.hiddenWord = None
        self.playerHearts = hearts
        self.correctLetters = []
        self.guessed = []

        self.letters = []
        if not self.hiddenWord:
            self._set_hiddenWord()
        self._set_letters()

    
    def _set_letters(self):
        found = []
        for char in self.hiddenWord:
            if char not in found:
                found.append(char)
        self.letters = found
    
    def _set_hiddenWord(self):        
        with open("./word_bank.txt","r") as f:
            #print(random_int)
            lines = f.readlines()
            random_int = random.randint(1, len(lines))
            w = lines[random_int-1].strip()
            self.hiddenWord = w
            #print(w)
            #time.sleep(3)

    def remove_one_heart(self):
        self.playerHearts -= 1
    
    def check_letter(self, letter:str):
        # likely the most important function
        if letter not in self.guessed:
            if letter in self.letters:                
                self.guessed.append(letter)
                self.correctLetters.append(letter)
                if len(self.letters) == len(self.correctLetters):
                    return STATUS[3]
                return STATUS[0]
            self.guessed.append(letter)
            self.remove_one_heart()
            return STATUS[1]
        return STATUS[2]

    def get_word_output_display(self):
        ss = io.StringIO()
        ss.write(f"{Fore.CYAN} Hidden word: ")
        for char in self.hiddenWord:
            if char in self.correctLetters:
                ss.write(char)
            else:
                ss.write("_")
        
        ss.write(f"\n\n{Fore.LIGHTBLUE_EX}Reveal this word by guessing one letter at a time.")
        return ss.getvalue()
    
    def get_hearts_output_display(self):
        ss = io.StringIO()
        ss.write(f"{Fore.LIGHTRED_EX}  Hearts:  ")
        for i in range(self.playerHearts):
            ss.write(f"{Fore.LIGHTRED_EX}♡")

        ss.write(f"{Fore.LIGHTRED_EX} ({self.playerHearts})")
        return ss.getvalue()
    


def main():
    print(f"{Fore.CYAN}>>> Launching the game >>>")
    time.sleep(2)
    game = Game(5)
    text = Fore.YELLOW
    update_output(game, text=text+"Welcome to the game I created by copying the code on the internet H-A-N-G-M-A-N v0.69")
    while game.playerHearts > 0:
        text = Fore.YELLOW
        player_input = str(input()).strip().lower()
        if player_input in QUIT:
            os.system("cls")
            print("You quitted the game.")
            return
        if len(player_input) > 1:
            update_output(game, text+"You can only guess 1 LETTER at a time!")
            continue
        check_result = game.check_letter(player_input) # developing ...
        if check_result == STATUS[0]:
            text += "FOUND ONE! Keep going"
        elif check_result == STATUS[1]:
            text += "OOPS Wrong one. Try again"
        elif check_result == STATUS[2]:
            text += "You already guessed that letter"
        elif check_result == STATUS[3]:
            os.system("cls")
            print(f"""
                {Fore.LIGHTMAGENTA_EX}============================================================
                {Fore.YELLOW}CONGRATS! You found the word: "{game.hiddenWord}"
                {Fore.LIGHTMAGENTA_EX}============================================================\n
                {Fore.WHITE} > Thanks for playing. This game is fun, right? Right??
                """)
            return
        update_output(game, text)
    os.system("cls")
    print(f'{Fore.YELLOW} Out of hearts...\nYou lost. The hidden word was "{game.hiddenWord}"')
    return


def update_output(game:Game, text:None):
    os.system("cls")
    print(game.get_hearts_output_display())
    print(game.get_word_output_display())
    if text:
        print(">>> "+text+f" {Fore.WHITE}<<<\n")
    print(f"{Fore.GREEN}Type your guess here:")


if __name__ == "__main__":
    main()

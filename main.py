import os
import io
import time
from colorama import init, Fore
import random

init(autoreset=True)
STATUS = ("correct", "wrong", "duplicated", "win")
QUIT = {"quit", "esc", "exit", "forfeit"}
# mode 1 = 7 hearts, mode 2 = 5 hearts, mode 3 = 3 hearts
DIFFICULTY = {1: 7, 2: 5, 3: 3}


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Game():
    def __init__(self, hearts: int) -> None:
        self.hiddenWord = ""
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
        with open("./word_bank.txt", "r") as f:
            lines = f.readlines()
            random_int = random.randint(1, len(lines))
            w = lines[random_int-1].strip()
            self.hiddenWord = w

    def remove_one_heart(self):
        self.playerHearts -= 1

    # likely the most important function
    def check_letter(self, letter: str):
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

        ss.write(
            f"\n\n{Fore.LIGHTBLUE_EX}Reveal this word by guessing one letter at a time.")
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
    time.sleep(1)

    hearts = specify_difficulty_as_hearts()
    game = Game(hearts)

    text = Fore.YELLOW
    update_output(game, text=text+"Welcome to H-A-N-G-M-A-N v0.69")
    while game.playerHearts > 0:
        text = Fore.YELLOW
        player_input = str(input()).strip().lower()
        if player_input in QUIT:
            clear_console()
            print("You quitted the game.")
            return
        if len(player_input) > 1:
            update_output(game, text+"You can only guess 1 LETTER at a time!")
            continue
        check_result = game.check_letter(player_input)  # developing ...
        if check_result == STATUS[0]:
            text += "FOUND ONE! Keep going"
        elif check_result == STATUS[1]:
            text += "OOPS Wrong one. Try again"
        elif check_result == STATUS[2]:
            text += "You already guessed that letter"
        elif check_result == STATUS[3]:
            clear_console()
            print(f"""
                {Fore.LIGHTMAGENTA_EX}============================================================
                {Fore.YELLOW}CONGRATS! You found the word: "{game.hiddenWord}"
                {Fore.LIGHTMAGENTA_EX}============================================================\n
                {Fore.WHITE} > I hope you had fun!
                """)
            return
        update_output(game, text)
    clear_console()
    print(f'{Fore.YELLOW} Out of hearts...\nYou lost. The hidden word was "{game.hiddenWord}"')
    return


def specify_difficulty_as_hearts():
    clear_console()
    print(f"""
    Please choose a difficulty by typing the number:
    1. Easy (7 hearts)   : suitable for beginners
    2. Medium (5 hearts) : still ez tho
    3. Hard (3 hearts)   : experts only        
    """)
    print("Your choice:")
    while True:
        inp = input()
        try:
            inp = int(inp)
        except KeyboardInterrupt:
            exit()
        except:
            try:
                inp = str(inp).strip().lower()
            except:
                pass
            else:
                if inp in QUIT:
                    clear_console()
                    print(" You quitted the game.")
                    exit()

            print(f"\nPlease choose it by typing number only (1 or 2 or 3)\nYour choice:")
            continue

        if inp not in (1, 2, 3):
            print(f"\nPlease choose it by typing number only (1 or 2 or 3)\nYour choice:")
            continue

        break

    return DIFFICULTY[inp]


def update_output(game: Game, text: str):
    clear_console()
    print(game.get_hearts_output_display())
    print(game.get_word_output_display())
    if text:
        print(">>> "+text+f" {Fore.WHITE}<<<\n")
    print(f"{Fore.GREEN}Type your guess here:")


if __name__ == "__main__":
    main()

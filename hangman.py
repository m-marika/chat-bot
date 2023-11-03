from random import choice

with open('words.txt', 'r', encoding='utf-8') as f:
    WORDS = [line.strip().lower() for line in f.readlines()]


class HangmanGame:
    def __init__(self):
        self.game_on = False

    def start(self):
        self.game_on = True
        self.used = []
        self.word = choice(WORDS)
        self.so_far = ['-']*len(self.word)
        self.wrong = 0
        self.max_wrong = len(HANGMAN) - 1

    def info(self):
        msg = HANGMAN[self.wrong]
        msg += '\n You were used:'
        msg += str(self.used) + '\n'
        msg += ' '.join(self.so_far)
        msg += '\n\n Write new letter'
        return msg

    def game_step(self, letter):
        if letter in self.used:
            return 'Letter were used'
        else:
            self.used.append(letter)
            if letter in self.word:
                msg = f'\n Yes! \"{letter}\" is in word'
                index = [i for i in range(len(self.word)) if self.word[i] == letter]
                for ind in index:
                    self.so_far[ind] = letter
                if self.so_far.count('_') == 0:
                    msg += f'\n Well done! You win! Word {self.word}'
                    self.game_on = False
                else:
                    msg += self.info()
                return msg
            else:
                msg = f'\n Wrong! \"{letter}\" not in word'
                self.wrong += 1
                if self.wrong >= self.max_wrong:
                    msg += HANGMAN[self.max_wrong]
                    msg += '\n You lose!'
                    msg += f'\n Right answer is {self.word}'
                    self.game_on = False
                else:
                    msg += self.info()

                return msg


HANGMAN = [
        """
           _____
          |     |
          |
          |
          |
          |
        """,
        """
           _____
          |     |
          |     O
          |
          |
          |
        """,
        """
           _____
          |     |
          |     O
          |     |
          |
          |
        """,
        """
           _____
          |     |
          |     O
          |    /|
          |
          |
        """,
        """
           _____
          |     |
          |     O
          |    /|\\
          |
          |
        """,
        """
           _____
          |     |
          |     O
          |    /|\\
          |    /
          |
        """,
        """
           _____
          |     |
          |     O
          |    /|\\
          |    / \\
          |
        """
    ]

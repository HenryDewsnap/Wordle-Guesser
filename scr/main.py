import copy
import csv

WL_LTR_OFFSET = 3
UU_LTR_OFFSET = 1

def lf(words):
    letter_frequency = {}
    for word in words[0]:
        for letter in word:
            if letter in letter_frequency: letter_frequency[letter] += 1
            else: letter_frequency[letter] = 1
    for letter in letter_frequency: letter_frequency[letter] /= len(words[0])
    return letter_frequency

def val(words, lf, wl_letters, uu_letters):
    values = []
    for word in words[0]:
        values.append([word, 0])
        for letter in word:
            values[-1][1] += lf[letter]
            if letter in wl_letters: values[-1][1] += WL_LTR_OFFSET
            if letter in uu_letters: values[-1][1] += UU_LTR_OFFSET
    return values

class wordle_guesser:
    def __init__(self):
        self.in_use_words = []
        with open("words.csv", "r") as f:
            for word in csv.reader(f): self.in_use_words.append(word)
        
        self.known_not_positions = [] #the yellow positions
        self.known_positions = [None, None, None, None, None] ##The green ones
        self.uu_letters = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"] ##The light gray ones
        self.bl_letters = [] ##The gray ones
        self.wl_letters = [] ##The yellow ones

        self.get_info()

    def get_info(self):
        self.lf = lf(self.in_use_words)
        self.wv = val(self.in_use_words, self.lf, self.wl_letters, self.uu_letters)

    def check_conditions(self):
        for word in range(len(self.wv)): self.wv[word][1] = 0

        for bl_letter in self.bl_letters:
            for word in copy.copy(self.in_use_words[0]):
                for letter in word:
                    if letter == bl_letter: 
                        self.in_use_words[0].remove(word)
                        break

        for known_pos in range(len(self.known_positions)):
            if self.known_positions[known_pos] != None:
                for word in copy.copy(self.in_use_words[0]):
                    if word[known_pos] != self.known_positions[known_pos] or self.known_positions[known_pos] in f"{word[0:known_pos]}{word[known_pos+1::]}": self.in_use_words[0].remove(word)

        for known_not_pos in self.known_not_positions:
            print(known_not_pos)
            for word in copy.copy(self.in_use_words[0]):
                if word[known_not_pos[1]] == known_not_pos[0]: self.in_use_words[0].remove(word)

        for letter in self.bl_letters:
            if letter in self.uu_letters: self.uu_letters.remove(letter)

        self.get_info()
        self.wv.sort(key=lambda x: x[1])


if __name__ == "__main__":
    wg = wordle_guesser()
    while True:
        wg.check_conditions()
        for wv in wg.wv: print(f"Word: {wv[0]} ¦¦ Certainty: {wv[1]}")
        
        wg.bl_letters += input("New Black Listed Letters (SEPERATED BY ','): ").split(",")
        
        
        while True:
            if input("Any WhiteListed letters? (y/n): ") == "n": break
            data = [input("Letter: "), int(input("Position: "))-1]
            wg.known_not_positions.append(data)
            wg.wl_letters.append(data[0])


        while True:
            if input("Are there any known positions? (y/n): ") == "n": break

            wg.known_positions[int(input("Location (INT): "))-1] = input("Character (CHAR): ")

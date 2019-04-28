import re
from nltk.stem import WordNetLemmatizer


class WordToNumber:

    def __init__(self, word_number):
        self.word_number = word_number
        self.word_number_list = []
        self.number = 0

        # Where the magic happens
        self.number = self.word_to_num()

    group_1 = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90
    }
    group_2 = {
        'hundred': 100
    }
    group_3 = {
        'thousand': 1000,
        'million': 1000000,
        'billion': 1000000000,
        'trillion': 1000000000000
    }
    group_4 = {
        'point': '.',
        'minus': '-'
    }

    def remove_punctuation(self):
        if not isinstance(self.word_number, str):
            raise ValueError("Wrong type, please insert a string")
        self.word_number = re.sub(r'[^\w\s]', '', self.word_number)

    def to_lower(self):
        self.word_number = self.word_number.lower()

    def filter_words(self):
        self.word_number_list = [word for word in self.word_number_list if
                                 word in list(self.group_1.keys()) + list(self.group_2.keys()) + list(
                                     self.group_3.keys()) + list(self.group_4.keys())]

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        self.word_number_list = [lemmatizer.lemmatize(word) for word in self.word_number.split()]

    def word_to_num(self, i=0):

        # Taking it through the pipe:
        self.remove_punctuation()
        self.to_lower()
        self.lemmatize()
        self.filter_words()
        is_negative = False

        res = 0

        while i < len(self.word_number_list):

            try:
                if i == 0 and self.group_4[self.word_number_list[i]] == '-':
                    is_negative = True
                    i += 1
                    continue
                elif self.group_4[self.word_number_list[i]] == '.':
                    val_after_point = self.word_to_num(i + 1)
                    val_after_point = val_after_point / 10**len(str(val_after_point))
                    res = res + val_after_point
                    if is_negative:
                        res *= -1
                    return res
            except KeyError:
                pass

            # Finding a number smaller than a hundred
            multiplier, i = self.find_multiplier(i)
            if i == len(self.word_number_list):
                res += multiplier
            else:
                # Try to find a hundred, if a smaller val was found before it, multiply the smaller with it
                try:
                    if not i < len(self.word_number_list):
                        res += multiplier
                        continue
                    hundred = self.group_2[self.word_number_list[i]]
                    multiplier = multiplier*hundred
                    i += 1
                except KeyError:  # No hundred was found, continue regularly
                    pass
                # Try to find a value from the third group, if found and there is a smaller value before it
                # multiply the smaller with it
                try:
                    if not i < len(self.word_number_list):
                        res += multiplier
                        continue
                    val = self.group_3[self.word_number_list[i]]
                    res += multiplier * val
                    i += 1
                except KeyError:
                    if multiplier > 0:
                        res += multiplier
        if is_negative:
            res *= -1
        return res

    # Helper function to find a multiplier
    def find_multiplier(self, i):
        res = 0
        while i < len(self.word_number_list):
            try:
                res += self.group_1[self.word_number_list[i]]
                i += 1
            except KeyError:
                break
        try:
            if self.group_1[self.word_number_list[i - 1]] == 0:
                return res, i
        except KeyError:
            pass
        if res > 0:
            return res, i
        else:
            return 1, i




"""
    Class LetterGenerator, for generating letter combinations
    :return list:
"""


class LetterGenerator:

    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.result_list = list()

    """
        Function generates all possible combinations of two letters
    """
    def two_cmb(self, alpha_list: list, num_letter=0):
        """
        :param alpha_list:
        :param num_letter:
        :return: list
        """
        if num_letter >= len(alpha_list):
            return []
        else:
            [self.result_list.append(alpha_list[num_letter] + alpha) for alpha in alpha_list]
            num_letter += 1
            self.two_cmb(alpha_list, num_letter)
        return self.result_list

    """
        Function generates all possible combinations of three letters
    """
    def three_cmb(self, alpha_list: list, num_letter_one=0, num_letter_two=1) -> list:
        """
        :param alpha_list:
        :param num_letter_one:
        :param num_letter_two:
        :return: list
        """
        if num_letter_two >= len(alpha_list):
            return []
        else:
            [self.result_list.append(alpha_list[num_letter_one] + alpha_list[num_letter_two] + alpha) for alpha in alpha_list]
            num_letter_one += 1
            num_letter_two += 1
            self.three_cmb(alpha_list, num_letter_one, num_letter_two)
        return self.result_list
    """
        Generate combinations letters for query 
    """
    def start_generate(self):
        self.two_cmb(self.alphabet)
        self.three_cmb(self.alphabet)
        self.result_list = self.result_list + self.alphabet

    """
        Return list with combinations letters for query 
    """
    def det_result_list(self):
        return self.result_list
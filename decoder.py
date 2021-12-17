import copy


class LZWDecoder:
    def __init__(self):
        self.code_words = dict()
        self.byte_values: str = ''

    def _prepopulate_dict(self):
        """
        Initialize dictionary with alphabet
        :return: void
        """
        for i in range(256):
            # values have to be string for easier concatenation
            self.code_words[str(i)] = [str(i)]

    def _code_words_contains(self, value: [int]) -> int:
        """
        Check if code_words contains given value, if so returns key under which this value can be found
        :param value: value to lookup
        :return: key for which value was found
        """
        for key in self.code_words.keys():
            # element-wise comparation
            if self.code_words[key] == value:
                return key
        return -1

    def _create_dict_and_decode(self):
        """
        Create code_words dictionary and decode compressed values
        :return: void
        """
        is_first_run = True
        i = 0
        max_idx = 256
        result: str = ''
        for key in self.byte_values:
            # we do not append to last term in code_words in first run as there is no additional
            # element at the end
            if not is_first_run:
                # append to the last code_word first element of value under given key
                value_for_key = self.code_words[key]
                first_elem_of_value = value_for_key[0]
                last_key = list(self.code_words.keys())[-1]
                self.code_words[last_key].append(first_elem_of_value)
            is_first_run = False
            decoded_value = copy.deepcopy(self.code_words[key])
            self.code_words[str(max_idx)] = decoded_value
            max_idx += 1
            result += f'{" ".join(decoded_value)} '
        return result.strip()

    def decode(self, input_file: str):
        self._prepopulate_dict()
        with open(input_file, 'r') as file:
            content = ''.join(file.readlines())
        self.byte_values = content.split(' ')
        return self._create_dict_and_decode()

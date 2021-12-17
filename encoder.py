class LZWEncoder:
    def __init__(self):
        self.code_words = dict()
        self.byte_values: str = ''

    def _translate_to_bytes(self, content: str) -> []:
        """
        Migrate bits to bytes. There is no need to pad content, as unpadded values
        will be treated as LSBs
        :param content: content to transform
        :return: byte translated content
        """
        result: [] = []
        for i in range(0, len(content), 8):
            token = content[i: i + 8]
            result.append(int(token, 2))
        return result

    def _prepopulate_dict(self):
        """
        Initialize dictionary with alphabet
        :return: void
        """
        for i in range(256):
            self.code_words[i] = [i]

    def _code_words_contains(self, value: [int]) -> int:
        """
        Check if code_words contains given value, if so returns key under which this value can be found
        :param value: value to lookup
        :return: key for which value was found
        """
        for key in self.code_words.keys():
            if self.code_words[key] == value:
                return key
        return -1

    def _create_dict_and_encode(self) -> str:
        """
        Create code_words dict and encode content
        :return: void
        """
        i = 0
        # next biggest index to be created
        max_idx = 256
        result: str = ''
        # for each byte
        while i < len(self.byte_values):
            k = 1
            # iterate over consecutive bytes
            while k <= len(self.byte_values) - i:
                token = self.byte_values[i: i + k]
                # until we find first sequence of bytes we do not have in code_words
                if self._code_words_contains(token) == -1:
                    # if so add it to code_words
                    self.code_words[max_idx] = self.byte_values[i: i + k]
                    max_idx += 1
                    # and to result as key under which this sequence without last byte was be stored
                    result += f'{str(self._code_words_contains(token[:-1]))} '
                    break
                # increase to prevent iterating over this same values all oevr the time
                k += 1
            # if in some case last sequence of bytes was already created in code_words, we should add it here
            # as loop above will only add new, not existing, values to result
            if k > len(self.byte_values) - i:
                result += f'{str(self._code_words_contains(self.byte_values[i: i + k - 1]))}'
            # increase main counter, as slice operator is exclusive for "to" parameter and inclusive for "from" parameter
            # and here we are switching it we have decreas k by one
            i += k - 1
        return result

    def _save_to_file(self, output_file: str, content: str):
        with open(output_file, 'w+') as file:
            file.write(content)

    def encode(self, input_file: str, output_file: str):
        self._prepopulate_dict()
        with open(input_file, 'r') as file:
            content = ''.join(file.readlines())
        content = content.replace(' ', '')
        self.byte_values = self._translate_to_bytes(content)
        self._save_to_file(
            output_file,
            self._create_dict_and_encode()
        )

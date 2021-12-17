from decoder import LZWDecoder
from encoder import LZWEncoder


def main():
    encoder = LZWEncoder()
    encoder.encode('data/test.txt.8bit.01', 'data/encoded.enc')

    decoder = LZWDecoder()
    print(decoder.decode('data/encoded.enc'))


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

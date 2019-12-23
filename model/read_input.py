import argparse

class InputParser(argparse.ArgumentParser):

    '''
    A command-line interface that is implemented with argparse.ArgumentParser
    '''

    def __init__(self):
        super(InputParser,self).__init__()

        # Adding arguments

        self.add_argument("-i", "--image", type=str,
            help="path to input image")

        self.add_argument("-east", "--east", type=str,
            help="path to pre-trained EAST text detector")

        self.add_argument("-w", "--width", type=int, default=320,
            help="resized image width [multiple of 32]")

        self.add_argument("-e", "--height", type=int, default=320,
            help="resized image height [multiple of 32]")

        self.add_argument("-c", "--min-confidence", type=float, default=0.5,
            help="minimum probability required to identify region")

        self.add_argument("-s", "--save-image", type=str,
            help="file name for saving image [no file suffix]")


        # Retrieve arguments
        self.args = vars(self.parse_args())

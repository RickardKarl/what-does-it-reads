import sys
import PIL 
from PIL import Image
import argparse

class ResizeImageInputParser(argparse.ArgumentParser):

    '''
    A command-line interface that is implemented with argparse.ArgumentParser
    '''

    def __init__(self):
        super(ResizeImageInputParser,self).__init__()

        # Adding arguments

        self.add_argument("-i", "--image", type=str,
            help="path to input image")

        self.add_argument("-n", "--name", type=str,
            help="new file name of resized image")

        self.add_argument("-w", "--width", type=int, default=320,
            help="image width to resize with respect to")


        # Retrieve arguments
        self.args = vars(self.parse_args())

        

def resize_image(file_path, resized_file_name = None, base_width = 300):
    """ 
    Resize image but keeps aspect ratio intact 
    """
    
    if resized_file_name == None:
        old_file_name = file_path.split("/")[-1]
        resized_file_name = "resized_" + old_file_name

    # Load image
    img = Image.open(file_path)
    # Get new heigth given the width
    width_percent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(width_percent)))

    # Resize image and save it
    img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
    img.save(resized_file_name)


if __name__ == "__main__":

    parser = ResizeImageInputParser()
    args = parser.args
    
    resize_image(args['image'],
                resized_file_name=args['name'],
                base_width=args['width'])

    print("Resized image {}, it was saved as {}".format(args['image'], args['name']))
import robots.cropper
import sys

if __name__ == "__main__":

    #Check if a filename has been defined by user
    if (len(sys.argv) != 2):
        raise("File was not determined!")
    
    robots.cropper.cropper(sys.argv[1])
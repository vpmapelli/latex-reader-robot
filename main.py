import robots.cropper
import robots.mathpix
import sys

if __name__ == "__main__":

    #Check if a filename has been defined by user
    if (len(sys.argv) != 2):
        raise("File was not determined!")
    
    robots.cropper.run(sys.argv[1])
    robots.mathpix.run(sys.argv[1])
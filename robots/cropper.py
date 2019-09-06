import PyPDF2
import os
from wand.image import Image
from wand.color import Color

def openFile(filename):
    '''Simple wrapper to open a pdf file'''
    return PyPDF2.PdfFileReader(filename,'rb')

def readPagesAndSaveAnnotsPositions(reader):
    '''Input: PyPDF2.PdfFileReader object'''

    fileRectList = []
    for pageNum in range(reader.numPages):
        page = reader.getPage(pageNum)
        pageRectList = searchPolygonAnnottations(page)
        fileRectList.append(pageRectList)
    
    return fileRectList

def searchPolygonAnnottations(page):
    '''Search for polygon annottations in a page'''

    rectList = []
    if '/Annots' in page:
        annottsObjects = page['/Annots'].getObject()
        numOfAnnottations = len(annottsObjects)
        
        for i in range(numOfAnnottations):
            if '/Rect' in annottsObjects[i].getObject():
                rectList.append(annottsObjects[i].getObject()['/Rect'])
        
    return rectList

def cropEquations(filename, fileAnnotsList = []):
    '''Iterate through fileAnnotsList and generate a cropped pdf for each of them'''

    filenameWithoutExtension = filename.split(".")[0]
    for i,pageRectList in enumerate(fileAnnotsList):
        print("Page number = {}".format(i))
        if not pageRectList:
            print("No annotations found\n")
        else:
            for j,rect in enumerate(pageRectList):

                reader = openFile(filename)
                page = reader.getPage(i)

                # Trying to crop with mediaBox first
                page.mediaBox.setLowerLeft(rect[0:2])
                page.mediaBox.setUpperRight(rect[2:])

                writer = PyPDF2.PdfFileWriter()
                outFilename = "./" + filenameWithoutExtension + "/pg{}_eq{}".format(i+1,j) + ".pdf"
                os.makedirs(filenameWithoutExtension, exist_ok=True)
                outstream = open(outFilename,'wb+')

                writer.addPage(page)
                writer.removeLinks()

                writer.write(outstream)
                print("Generated {} pdf file".format(j))
            print("\n")

def convertPDFeqsToPNG(filename):
    '''Converting all cropped pdf files to png images'''

    for localPath, _, files in os.walk("./" + filename.split(".")[0]):
        for file in files:
            with Image(filename=localPath+"/"+file, resolution=300) as img:
                with Image(width=img.width, height=img.height, background=Color("White")) as bg:
                    bg.composite(img,0,0)
                    bg.save(filename=localPath+"/"+file.split(".")[0]+".png")
                    print("Converted {} to {}".format(file,file.split(".")[0]+".png"))
            
            #Remove original pdf
            os.remove(localPath+"/"+file)
            print("Deleting {}".format(file))


def run(filename):
    '''Run cropper robot'''

    reader = openFile(filename)
    fileAnnotsList = readPagesAndSaveAnnotsPositions(reader)
    cropEquations(filename, fileAnnotsList)
    convertPDFeqsToPNG(filename)

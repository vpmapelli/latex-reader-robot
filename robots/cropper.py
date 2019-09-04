import PyPDF2

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


def run(filename):
    '''Run cropper robot'''
    reader = openFile(filename)
    fileAnnotsList = readPagesAndSaveAnnotsPositions(reader)

    for i,pageList in enumerate(fileAnnotsList):
        print("Page number = {}".format(i))
        if not pageList:
            print("No annotations found\n")
        else:
            for rect in pageList:
                print("Annotation position: {}".format(rect))
            print("\n")
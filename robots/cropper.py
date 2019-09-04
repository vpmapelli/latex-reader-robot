import PyPDF2

def openFile(filename):
    '''Simple wrapper to open a pdf file'''
    return PyPDF2.PdfFileReader(filename,'rb')

def readPages(reader):
    '''Read all pages from a pdf file
    Input: PyPDF2.PdfFileReader object'''

    for pageNum in range(reader.numPages):
        page = reader.getPage(pageNum)
        print(pageNum)
        # print(page)
        searchPolygonAnnottations(page)

def searchPolygonAnnottations(page):
    '''Search for polygon annottations in a page'''
    if '/Annots' in page:
        annottsObjects = page['/Annots'].getObject()
        numOfAnnottations = len(annottsObjects)
        
        for i in range(numOfAnnottations):
            print(annottsObjects[i].getObject(),"\n")
            if '/Rect' in annottsObjects[i].getObject():
                print("Found a polygon annotattion!")


        print("Found some annottations!\n\n")
    else:
        print("No annottations found!\n")

def run(filename):
    '''Run cropper robot'''
    reader = openFile(filename)
    readPages(reader)
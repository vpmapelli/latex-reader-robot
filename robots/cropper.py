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
        print(page,"\n\n")

def cropper(filename):
    '''Run cropper robot'''
    reader = openFile(filename)
    readPages(reader)
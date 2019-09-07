import sys
import base64
import requests
import json
import os

def loadCredential():

    with open("./credentials/mathPix.json") as json_file:
        data = json.load(json_file)
    return data

def querySingleImage(imagesPath,filename,credentials):
    filePath = imagesPath+"/"+filename

    image_uri = "data:image/jpg;base64," + base64.b64encode(open(filePath, "rb").read()).decode()

    r = requests.post("https://api.mathpix.com/v3/latex",
        data=json.dumps(
            {
                'src': image_uri, 
                "format_options":{
                        "text":{
                                "displaymath_delims":[
                                        "\n$$\n",
                                        "\n$$\n"
                                ],
                                "transforms":[
                                        "rm_spaces"
                                ],
                                "math_delims":[
                                        "\\(",
                                        "\\)"
                                ]
                        },
                        "latex_styled":{
                                "transforms":[
                                "rm_spaces"
                                ]
                        }
                },
                "skip_recrop":True,
                "ocr":[
                        "math",
                        "text"
                ],
                "formats":[
                        "text",
                        "text_display",
                        "latex_styled"
                ]
            }),
        headers=credentials)
        
    response = json.loads(r.text)
    return response

def queryAllImages(imagesIterator, credentials):
        '''Iterate through images and send to API data'''

        responsesList = []

        for localPath, _, files in imagesIterator:
                for image in files:
                        latexSingleImageDict = querySingleImage(localPath,image,credentials)
                        latexSingleImageDict['filename'] = image.split(".")[0]
                        responsesList.append(latexSingleImageDict)
        
        for item in responsesList:
                print(json.dumps(item, indent=4, sort_keys=True))

        allLatexList = map(checkForErrors, responsesList)

        return allLatexList, responsesList


def checkForErrors(responseDict):

        if "error" in responseDict:
                return "Error id: " + responseDict["error_info"]["id"] + "\n" + "Error message:" + responseDict["error_info"]["message"]
        else:
                return responseDict["latex_styled"]

def generateFile(allLatexList, allLatexReponseDicts):

        with open("./latex/equations.tex","w+") as texFile:
                for latexString in allLatexList:
                        texFile.write(latexString + "\n\n")
        
        with open("./latex/allDicts.txt", "w+") as dictFile:
                for dict in allLatexReponseDicts:
                        dictFile.write(json.dumps(dict, indent=4, sort_keys=True))


def run(filename):

    imagesPath = filename.split(".")[0]

    credentials = loadCredential()

    os.makedirs("latex", exist_ok=True)
    imagesIterator = os.walk("./" + imagesPath)

    allLatexList, allLatexReponseDicts = queryAllImages(imagesIterator, credentials)

    generateFile(allLatexList, allLatexReponseDicts)
#     latexDict = querySingleImage(imagesPath,"pg6_eq0.png",credentials)

    # with open("./latex/equations.tex",'w+') as texFile:
    #     texFile.write(latexDict["latex_styled"])


#     print(json.dumps(latexDict, indent=4, sort_keys=True))

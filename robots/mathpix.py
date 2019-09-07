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

def checkConfidenceRate(responseDict):

        if "latex_confidence_rate" in responseDict:
                if responseDict["latex_confidence_rate"] < 0.8:
                        return True
                else:
                        return False
        else:
                return False

        

def generateFile(allLatexList, allLatexResponseDicts,imagesPath):

        with open("./"+imagesPath+"/"+imagesPath+".tex","w+") as texFile:
                for i,latexString in enumerate(allLatexList):
                        texFile.write(allLatexResponseDicts[i]["filename"].replace("eq","Equation ").replace("_"," ").replace("pg","Page ")+"\n")
                        texFile.write("\\begin{equation}\n")
                        if checkConfidenceRate(allLatexResponseDicts[i]): texFile.write("% Confidence rate lower than 0.80\n")
                        texFile.write(latexString + "\n")
                        texFile.write("\\end{equation}\n\n")
        
        with open("./"+imagesPath+"/"+imagesPath+"_responseDicts.txt", "w+") as dictFile:
                for dict in allLatexResponseDicts:
                        dictFile.write(json.dumps(dict, indent=4, sort_keys=True))


def run(filename):

    imagesPath = filename.split(".")[0]

    credentials = loadCredential()

    imagesIterator = os.walk("./" + imagesPath)

    allLatexList, allLatexReponseDicts = queryAllImages(imagesIterator, credentials)

    generateFile(allLatexList, allLatexReponseDicts, imagesPath)
#     latexDict = querySingleImage(imagesPath,"pg6_eq0.png",credentials)

    # with open("./latex/equations.tex",'w+') as texFile:
    #     texFile.write(latexDict["latex_styled"])


#     print(json.dumps(latexDict, indent=4, sort_keys=True))

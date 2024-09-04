
import os
import shutil
import copy

import json

import numpy as np

import simpleimageio as sio
from simpleimageio import lin_to_srgb

import utils.errormetrics
import cv2

def make_safe_dir(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)

class ResultsViewer:

    def __init__(self, utils_dir):
        self.utils_dir = utils_dir

    def generateHTMLS(self, viewer_output_dir, results_dir, scenes_dir, scenes, testCaseDescription, testCases, showReference=False, perScene = True, layers=[], errors=[]):
        make_safe_dir(viewer_output_dir)
        make_safe_dir(viewer_output_dir + "/utils")
        shutil.copy(self.utils_dir + "/Chart.js", viewer_output_dir + "/utils/Chart.js")
        shutil.copy(self.utils_dir + "/ChartBox.js", viewer_output_dir + "/utils/ChartBox.js")
        shutil.copy(self.utils_dir + "/CopyrightBox.js", viewer_output_dir + "/utils/CopyrightBox.js")
        shutil.copy(self.utils_dir + "/ImageBox.js", viewer_output_dir + "/utils/ImageBox.js")
        shutil.copy(self.utils_dir + "/report.css", viewer_output_dir + "/utils/report.css")
        shutil.copy(self.utils_dir + "/TableBox.js", viewer_output_dir + "/utils/TableBox.js")
        allSceneResultsDict = []

        numLayers = len(layers)
        numErrors = len(errors)

        for scenedata in scenes:
            scene = scenedata[0]
            scene_variants = scenedata[1]
            for variant in scene_variants:
                scene_variant_dir = viewer_output_dir + "/"+ scene
                if variant != "":
                    scene_variant_dir += variant
                make_safe_dir(scene_variant_dir)

                sceneResultsDict = {}
                sceneResultsDict["title"] = scene + variant
                sceneResultsDict["elements"] = []

                typeId = {}
                typeCount = 0
                sceneResultsLayersDict = {}
                if numLayers > 0:
                    layerDict = {}
                    layerDict["title"] = "color"
                    layerDict["elements"] = []
                    sceneResultsDict["elements"].append(layerDict)
                    typeId["color"] = typeCount
                    typeCount += 1
                    for i in range(numLayers):
                        layerDict = {}
                        layerDict["title"] = layers[i]
                        layerDict["elements"] = []
                        sceneResultsDict["elements"].append(layerDict)
                        typeId[layers[i]] = typeCount
                        typeCount += 1

                for i in range(numErrors):
                    errorDict = {}
                    errorDict["title"] = errors[i]
                    errorDict["elements"] = []
                    sceneResultsDict["elements"].append(errorDict)
                    typeId[errors[i]] = typeCount
                    typeCount += 1

                if showReference:
                    reference_dict = {}
                    reference_image_exr =  scenes_dir + "/" + scene + "/" + scene + variant + "_ref" + ".exr"
                    print(reference_image_exr)
                    img = sio.read(reference_image_exr)
                    reference_image_png =  scene_variant_dir + "/" + scene + variant + "_ref" + ".png"
                    sio.image.write(reference_image_png, img)
                    reference_dict = {}
                    reference_dict["title"] = "Reference"
                    reference_dict["version"] = "-"
                    
                    if perScene:
                        reference_dict["image"] = scene + variant + "_ref" + ".png"
                    else:
                        reference_dict["image"] = scene + variant + "/" + scene + variant + "_ref" + ".png"
                    
                    if numLayers > 0:
                        sceneResultsDict["elements"][0]["elements"].append(reference_dict)
                    else:
                        sceneResultsDict["elements"].append(reference_dict)

                    if numLayers > 0:
                        limg = sio.read_layered_exr(reference_image_exr)
                        for i in range(numLayers):
                            img = np.zeros(img.shape)
                            if limg.__contains__(layers[i]):
                                img = limg[layers[i]]
                            test_case_layer_image_png =  scene_variant_dir + "/" + scene + variant + "_ref" + "-"+ layers[i] + ".png"
                            sio.image.write(test_case_layer_image_png, img)
                            layer_dict = {}
                            layer_dict["title"] = "Reference"
                            layer_dict["version"] = "-"
                            if perScene:
                                layer_dict["image"] = scene + variant + "_ref" + "-"+ layers[i] + ".png"
                            else:
                                layer_dict["image"] = scene + variant + "/" + scene + variant + "_ref" + "-"+ layers[i] + ".png"
                            sceneResultsDict["elements"][typeId[layers[i]]]["elements"].append(layer_dict)

                    if numErrors > 0:
                        for i in range(numErrors):
                            img = np.zeros(img.shape)
                            test_case_error_image_png =  scene_variant_dir + "/" + scene + variant + "_ref" + "-"+ errors[i] + ".png"
                            sio.image.write(test_case_error_image_png, img)
                            error_dict = {}
                            error_dict["title"] = "Reference"
                            error_dict["version"] = "-"
                            if perScene:
                                error_dict["image"] = scene + variant + "_ref" + "-"+ errors[i] + ".png"
                            else:
                                error_dict["image"] = scene + variant + "/" + scene + variant + "_ref" + "-"+ errors[i] + ".png"
                            sceneResultsDict["elements"][typeId[errors[i]]]["elements"].append(error_dict)

                
                for testCase in testCases:
                    
                    if not testCase.skipViewer:
                        result_dict = {}
                        test_case_result_image_exr =  results_dir + "/" + scene + variant + "/" + scene + variant + "-" + testCase.name + ".exr"
                        print(test_case_result_image_exr)
                        tcImg = sio.read(test_case_result_image_exr)
                        test_case_result_image_png =  scene_variant_dir + "/" + scene + variant + "-" + testCase.name + ".png"
                        sio.image.write(test_case_result_image_png, tcImg)
                        result_dict = {}
                        result_dict["title"] = testCase.name
                        result_dict["version"] = "-"
                        
                        if perScene:
                            result_dict["image"] = scene + variant + "-" + testCase.name + ".png"
                        else:
                            result_dict["image"] = scene + variant + "/" + scene + variant + "-" + testCase.name + ".png"
                        
                        if numLayers > 0:
                            sceneResultsDict["elements"][0]["elements"].append(result_dict)
                        else:
                            sceneResultsDict["elements"].append(result_dict)

                        if numLayers > 0:
                            limg = sio.read_layered_exr(test_case_result_image_exr)
                            for i in range(numLayers):
                                img = np.zeros(tcImg.shape)
                                if limg.__contains__(layers[i]):
                                    img = limg[layers[i]]
                                test_case_layer_image_png =  scene_variant_dir + "/" + scene + variant + "-" + testCase.name + "-"+ layers[i] + ".png"
                                sio.image.write(test_case_layer_image_png, img)
                                layer_dict = {}
                                layer_dict["title"] = testCase.name
                                layer_dict["version"] = "-"
                                if perScene:
                                    layer_dict["image"] = scene + variant + "-" + testCase.name + "-"+ layers[i] + ".png"
                                else:
                                    layer_dict["image"] = scene + variant + "/" + scene + variant + "-" + testCase.name + "-"+ layers[i] + ".png"
                                sceneResultsDict["elements"][typeId[layers[i]]]["elements"].append(layer_dict)

                        if numErrors > 0:
                            reference_image_exr =  scenes_dir + "/" + scene + "/" + scene + variant + "_ref" + ".exr"
                            refImg = sio.read(reference_image_exr)
                            for i in range(numErrors):
                                    [errorValue, errorImg] = errormetrics.calculateError(refImg, tcImg, errors[i], percentile=0.01, epsilon=0.001)
                                    #fgError = figuregen.util.image.relative_mse_outlier_rejection(img=tcImg, ref=refImg, )
                                    fgError = sio.relative_mse_outlier_rejection(img=tcImg, ref=refImg, percentage=0.01, epsilon=0.001)
                                    maxError = np.max(errorImg)
                                    print("errorValue = " , errorValue , "\t fgError = ", fgError)
                                    errorImg = cv2.applyColorMap(((np.clip(errorImg / (errorValue * 2), 0.0, 1.0))*255).astype(np.uint8), cv2.COLORMAP_AUTUMN).astype(np.float32) / 255.0    
                                    #errorImg = lin_to_srgb(errorImg)
                                    test_case_error_image_png =  scene_variant_dir + "/" + scene + variant + "-" + testCase.name + "-"+ errors[i] + ".png"
                                    sio.image.write(test_case_error_image_png, errorImg)
                                    error_dict = {}
                                    error_dict["title"] = testCase.name
                                    error_dict["version"] = "-"
                                    if perScene:
                                        error_dict["image"] = scene + variant + "-" + testCase.name + "-"+ errors[i] + ".png"
                                    else:
                                        error_dict["image"] = scene + variant + "/" + scene + variant + "-" + testCase.name + "-"+ errors[i] + ".png"
                                    sceneResultsDict["elements"][typeId[errors[i]]]["elements"].append(error_dict)

                if not perScene:
                    allSceneResultsDict.append(sceneResultsDict)

                if perScene:
                    htmlStr = ""
                    htmlStr += self.generateHeader("title", scene + variant)
                    htmlStr += self.generateBody(testCaseDescription, [sceneResultsDict], scene + variant)
                    htmlStr += self.generateFooter()
                    sceneViewHTML = open(scene_variant_dir +"/"+ "index.html","w")
                    sceneViewHTML.write(htmlStr)
                    sceneViewHTML.close()
                    #print(htmlStr)

        if not perScene:
            htmlStr = ""
            htmlStr += self.generateHeader(perScene=False)
            htmlStr += self.generateBody(testCaseDescription, allSceneResultsDict,perScene=False)
            htmlStr += self.generateFooter()
            sceneViewHTML = open(viewer_output_dir +"/"+ "index.html","w")
            sceneViewHTML.write(htmlStr)
            sceneViewHTML.close()
            #print(htmlStr)

    def generateHeader(self, title="Rendering Scripts", scene=None, perScene=True):
        htmlHeader = ""
        htmlHeader += "<!doctype html>" + "\n"
        htmlHeader += "<html lang='en'>" + "\n"
        htmlHeader += "<head>" + "\n"
        htmlHeader += "    <meta charset='utf-8'>" + "\n"
        htmlHeader += "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>" + "\n"
        htmlHeader += "    <meta name='description' content='"+ title + "'>" + "\n"
        htmlHeader += "    <title>'"+ title + "'</title>" + "\n"
        htmlHeader += "" + "\n"
        htmlHeader += "    <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600' rel='stylesheet' type='text/css'>" + "\n"
        htmlHeader += "    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css' integrity='sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4' crossorigin='anonymous'>" + "\n"
        htmlHeader += ""+ "\n"
        if perScene:
            htmlHeader += "    <link rel='stylesheet' href='../utils/report.css'>" + "\n"
        else:
            htmlHeader += "    <link rel='stylesheet' href='./utils/report.css'>" + "\n"
        htmlHeader += "" + "\n"
        htmlHeader += "</head>"+ "\n"

        return htmlHeader
    

    def generateBody(self, testCaseDescription, results_dict, perScene=False, scene=None):
        results_json = json.dumps(results_dict, indent=4, separators=(',', ': '))
        htmlBody = ""
        htmlBody += "<body >" + "\n"
        htmlBody += "    <div class='container content  scene-content' id='content'>" + "\n"
        htmlBody += "" + "\n"
        #htmlBody += "<p><a href='../../index.html'>Back to index</a></p>" + "\n"
        htmlBody += "<h1>" + testCaseDescription["title"]+ "</h1>" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "        <p>" + "\n"
        htmlBody += "            " + testCaseDescription["short"] + "\n"
        htmlBody += "        </p>" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "        <p>" + "\n"
        htmlBody += "            " + testCaseDescription["long"] + "\n"
        htmlBody += "        </p>" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "    </div>" + "\n"
        htmlBody += "" + "\n"
        if perScene:
            htmlBody += "    <script src='../utils/ImageBox.js'></script>" + "\n"
            htmlBody += "    <script src='../utils/Chart.js'></script>" + "\n"
            htmlBody += "    <script src='../utils/ChartBox.js'></script>" + "\n"
            htmlBody += "    <script src='../utils/TableBox.js'></script>" + "\n"
            htmlBody += "    <script src='../utils/CopyrightBox.js'></script>" + "\n"
        else:
            htmlBody += "    <script src='./utils/ImageBox.js'></script>" + "\n"
            htmlBody += "    <script src='./utils/Chart.js'></script>" + "\n"
            htmlBody += "    <script src='./utils/ChartBox.js'></script>" + "\n"
            htmlBody += "    <script src='./utils/TableBox.js'></script>" + "\n"
            htmlBody += "    <script src='./utils/CopyrightBox.js'></script>" + "\n"
        htmlBody += "    <script type='text/javascript'>" + "\n"
        htmlBody += "        var imageBoxes =" + "\n"
        htmlBody += results_json + ";" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "        content = document.getElementById('content');" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "        if (imageBoxes)" + "\n"
        htmlBody += "            new ImageBox(content, imageBoxes);" + "\n"
        htmlBody += "" + "\n"
        #htmlBody += "        new CopyrightBox(content, "Adjusted by the author from publicly available scenes to match test example for LayerDenoise [Munkberg and Hasselgren 2020]");
        htmlBody += "" + "\n"
        htmlBody += "        if (stats) {" + "\n"
        htmlBody += "            new ChartBox(content, stats);" + "\n"
        htmlBody += "            new TableBox(content, stats);" + "\n"
        htmlBody += "        }" + "\n"
        htmlBody += "    </script>" + "\n"
        htmlBody += "" + "\n"
        htmlBody += "</body>" + "\n"
        return htmlBody

    def generateFooter(self):
        htmlFooter = ""
        htmlFooter += "</html>" + "\n"
        return htmlFooter

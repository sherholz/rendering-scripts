import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import pandas as pd
import numpy as np

def plotSceneStatistic(data, statistic, scene, plotFileName):
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_xlabel("iteration")
    ax.set_ylabel(statistic)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for testCase in data:
        values = np.array(data[testCase][statistic])
        x = np.linspace(1,values.size+1,values.size);
        ax.plot(x, values, label=testCase)
    ax.legend()
    ax.set_title(scene)
    fig.savefig(plotFileName)

class OpenPGLStatisticPlotter:
    def plotStatistics(self, results_dir, scenes, testCases, statistics):
        #for each scene and each scene variant
        for scene, scene_variants, resolution in scenes:
            for variant in scene_variants:
                data={}
                sceneVariantName = scene+variant
                sceneResultsFolder = results_dir + "/" + sceneVariantName
                for testCase in testCases:
                    csvSurfaceFile = sceneResultsFolder + "/" +sceneVariantName + "-" + testCase.name + "-surface.csv"
                    df = pd.read_csv(csvSurfaceFile, sep=',', skipinitialspace=True)
                    data[testCase.name] = df
                for statistic in statistics:
                    plotFileName = sceneResultsFolder + "/" +sceneVariantName + "-" + statistic.replace(" ","") + ".png"
                    plotSceneStatistic(data, statistic, scene, plotFileName)
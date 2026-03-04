import numpy as np

def calculateError(refImg, img, errorType="relMSE", percentile=0.01, epsilon = 0.001):
    
    errorImg = np.zeros([refImg.shape[0],refImg.shape[1]])
    errorValue = 0.0
    if errorType == "relMSE":
        print("relMSE")
        errorImg = (img-refImg)**2 / (refImg**2+epsilon)
        errorImg = np.average(errorImg, axis=2)
        print(errorImg.shape)
    elif errorType == "MSE" or errorType == "RMSE":
        print("MSE")
        errorImg = (refImg-img)**2
        errorImg = np.average(errorImg, axis=2)

    elif errorType == "SMAPE":
        print("SMAPE")
        errorImg = np.abs(refImg-img)
        errorImg /= (refImg+img+epsilon) / 2
        errorImg = np.average(errorImg, axis=2)
    elif errorType == "PosNeg":
        errorImg = refImg-img
        errorImg = np.average(errorImg, axis=2)


    flatError = errorImg.flatten()
    flatError = np.sort(flatError)
    flatErrorSize = int(flatError.size * ((100.0-percentile)/ 100.0))
    errorMean = np.mean(flatError[0:flatErrorSize])
    errorVariance = np.var(flatError[0:flatErrorSize])

    if errorType == "RMSE":
        errorVariance = np.sqrt(errorMean)
    return [errorMean, errorVariance, errorImg]

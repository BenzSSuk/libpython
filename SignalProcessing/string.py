import numpy
import numpy as np

def numpyToString(arr, closeStringType='c', decimals=None):

    if isinstance(arr, numpy.ndarray):

        # if arr.dtype == 'float':
        #     with np.printoptions(suppress=True, precision=decimals):
        #         if decimals is None:
        #             decimals = 9
        #
        #         arr = np.round(arr, decimals=decimals)
        #         charRound = "%." + str(decimals) + "f"
        #         arrStr = np.array2string(arr, precision=decimals, formatter={'float_kind': lambda x: charRound % x},
        #                                  separator=',')
        #
        #         return arrStr
        #
        # elif arr.dtype == 'int':
        listArr = list(arr)

        if closeStringType == 'c':
            converted_list = [str(element) for element in listArr]
            stringArr = ",".join(converted_list)
            stringArr = "{" + stringArr + "}"

            return stringArr

        elif closeStringType == 'list':
            return str(listArr)

        # else:
        #     raise ValueError('Support only numpy array "float" and "int"')


        # with np.printoptions(suppress=True):
        #     if not decimals is None:
        #         arr = np.round(arr, decimals=decimals)
        #
        #     listArr = list(arr)
        #
        #     if closeStringType == 'c':
        #         converted_list = [str(element) for element in listArr]
        #         stringArr = ",".join(converted_list)
        #         stringArr = "{" + stringArr + "}"
        #
        #         return stringArr
        #
        #     elif closeStringType == 'list':
        #         return str(listArr)

    else:
        raise ValueError('Support only numpy array !')

def writeString(pathSave, stringWrite):
    # nameRaw = f'ppg_green_win_{index_window_log}.txt'
    # pathSaveRaw = os.path.join(folderFeature, nameRaw)
    text_raw = open(pathSave, "w")
    text_raw.write(stringWrite)
    text_raw.close()

def writeNumpy(pathSave, arr, closeStringType='c', decimals=None):
    arrString = numpyToString(arr, closeStringType=closeStringType, decimals=decimals)

    writeString(pathSave, arrString)

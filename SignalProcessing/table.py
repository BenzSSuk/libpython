import os

import pandas as pd
from .common import *

def read_csv_folder(pathFolder):
    listDir, listFolder, listName = findFile(pathFolder, '*.csv', 0)

    nFiles = len(listName)

    if nFiles == 1:
        df = pd.read_csv(listDir[0])

        return df

    elif nFiles > 1:
        listDF = []

        for ifile in range(len(listName)):
            df = pd.read_csv(listDir[ifile])

            listDF.append(df)

        return listDF

    else:
        df = []
        return df

def readCSVInfolder(pathFolder):
    listDir, listFolder, listName = findFile(pathFolder, '*.csv', 0)

    nFiles = len(listName)

    if nFiles == 1:
        df = pd.read_csv(listDir[0])

        return df

    elif nFiles > 1:
        listDF = []

        for ifile in range(len(listName)):
            df = pd.read_csv(listDir[ifile])

            listDF.append(df)

        return listDF

    else:
        df = []
        return df

def read_concat_write_csv_folder(folderLoad, folderSave, nameSave):
    listDir, listFolder, listName = findFile(folderLoad, '*.csv', 0)

    for ifile in range(len(listName)):
        df = pd.read_csv(listDir[ifile])

        if ifile == 0:
            dfAll = df
        else:
            dfAll = pd.concat((dfAll, df), axis=0)

    dfAll.to_csv(os.path.join(folderSave, nameSave))

# def splitDFAndDownSampling(df, headerSplit, nDownSampling):

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:43:22 2022

@author: pannawis
"""
import math
import numpy as np
from .common import *

def swapKeyAndValueDict(dictIn):
    dictNew = {}
    listKeys = list(dictIn.keys())
    
    for ikey in listKeys:
        value = dictIn[ikey]
        # print(f"key:{ikey}, value:{value}\n")        
        dictNew[value] = str(ikey)
    
    return dictNew
    

def renameHeaderDF(df, dictHeader, inverseDict = False):
    '''
    Objective:
        rename header original to new
        
    inverseDict = False
    dictHeader = {'header_original1':'header_new1',
                  'header_original2':'header_new2'}
    
    inverseDict = True
    dictHeader = {'header_new1':'header_original1',
                  'header_new2':'header_original2'}
    
    '''
    
    if inverseDict:
        dictHeader = swapKeyAndValueDict(dictHeader)
        
    
    df = df.rename(columns=dictHeader)
    
    return df

def DAC(arrayDigital, bitRes, analogFullScale):
    '''
    Objective: 
        Convert digital to analog value
    
    Input:
        arrayDigital: output data from sensor(support array)
        nBit: no. of bit resolution, digital data range in 0 to (2^bitRes) -1
        analogFullScale: maximum value of analog data, analog data above this value
                    will be clipped to (2^bitRes) -1
    
    Output:
        arrayAnalog: data in analog type    
        
        e.g. 12 bits ADC, analogFullScale = 3.3 (volt)

        digial   analog
        0        0
        4095     3.3      
        
        x        3.3(x) / 4095
        
    '''
    maxDigital = math.pow(2,bitRes) - 1
    arrayAnalog = ( arrayDigital * analogFullScale ) / maxDigital
    
    return arrayAnalog

def DACbyHeader(df, listHeaderToDAC, adcBitRes, fullScaleValue, findListHeader = False):

    if findListHeader:
        # listHeaderToDAC = word for search in list header
        listHeader = list(df.columns)
        listHeaderToDAC = filterList(listHeader, listHeaderToDAC)

    for iheader in listHeaderToDAC:
        # print(f'DAC column:{iheader}')
        df[iheader] = DAC(df[iheader].to_numpy(), adcBitRes, fullScaleValue)
        
    return df
        
def ADC(y_meas, bitRes, fullScaleValue):
    '''
    vref = 3.3
    bitRes = 19 bits >> 2^19 >> 524288
    analog      digital
     vref       524288
     x          524288(x)/vref
    '''
    # vRef = 3
    # bitRes = 19
    digitalMax = math.pow(2, bitRes) - 1

    y_digital = np.floor((digitalMax * y_meas) / fullScaleValue)
    y_digital = y_digital.astype(int)

    return y_digital

def uint2int(uintVal, nbits):
    """
    Convert unsigned decimal to signed 
    """
    # nbits = 4
    nUint = (2**nbits)
    uintValMax = nUint - 1
    
    uintValMin = 0
    if uintVal > uintValMax:
        raise ValueError(f'uintValMax for {nbits} bits = {uintValMax}')
    if uintVal < uintValMin:
        raise ValueError(f'uintValMin for {nbits} bits = {uintValMin}')

    valMax = 2**(nbits-1)
    valSplit = nUint / 2 

    if uintVal >= valSplit:
        intVal = uintVal - nUint
    else:
        intVal = uintVal

    return intVal
    
def arrayUint2Int(arrUint, nbits):
    valMax = 2**nbits
    valSplit = valMax / 2 

    # set positive value
    arrInt = arrUint.copy()

    # convert to negative
    indexNegative = (arrUint >= valSplit)
    arrInt[indexNegative] = arrUint[indexNegative] - valMax

    return arrInt

def dfUint2Int(df, listHeaderConvert, nbits, logUint = False):
    """
    Loop convert uint to signed int in list header
    """
    dfUint = df.copy()
    for headerConvert in listHeaderConvert:
        if logUint:
            headerUint = f'{headerConvert}_uint'
            dfUint[headerUint] = df[headerConvert]
        dfUint[headerConvert] = arrayUint2Int(df[headerConvert].to_numpy(), nbits)

    return dfUint
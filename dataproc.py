"""
    本文件目标为处理数据，对目标文件夹调用即可获得包含有效项且已去重的A2DF；
"""



import pandas as pd
import json
from os import listdir


# 处理单个文件的函数procpage, 把json页里的停电信息拿出来；
def procpage(filepath:'str') -> list:
    """
        返回该json页里面所包含的所有停电信息。形式为一个dict列表。
    """
    print( 'procing file:', filepath, '...')
    
    line = ""
    with open( filepath, "r+", encoding='utf8', errors='ignore') as page:
        line = page.readline() # 每个page只有一页
        page.close()
    
    try:
        page_jsn = json.loads( line)
    except:
        print( 'LOAD error at file:', filepath)
        return 
    
    if page_jsn['seleList']:
        return page_jsn['seleList'].copy()

    return


# 将一个路径中的所有json中的停电事件汇集为一个DF
def makedf(datapath:'str') -> pd.DataFrame:
    """
        参数给出json文件所在的folder路径即可
    """
    keys = ['poweroffId', 'sgpoweroffId', 'subsName', 'lineName', 'pubTranName', 'scope', 'startTime', 'stopDate', 'orgNo', 'typeCode', 'poweroffArea', 'poweroffReason', 'powerTime', 'powerComm', 'subsNo', 'lineNo', 'tgNo', 'tgName', 'infoStatus', 'orgName', 'typeName', 'infoStatusName', 'dateDay', 'orgNos', 'nowTime', 'countyName', 'streetName', 'villageName', 'roadName', 'communityName', 'tranName', 'sdLineName', 'cityCode', 'cityName', 'provinceCode', 'stopTime', 'powerType', 'powerOffArea', 'powerOffReason', 'powerOffId']
    res = { k: list() for k in keys}
    
    for eachf in listdir( datapath):
        if eachf[-4:] == 'json':
            tds = procpage( datapath+'\\'+eachf)
            for d in tds:
                for k,v in d.items():
                    res[k].append( v)
    
    df = pd.DataFrame(res)
    return df


# drop掉 以下的列，这些列中没有任何有意义的信息; 最后对id列去重
def dropitems( bodf: pd.DataFrame) -> None:
    
    drop_item1 = "sgpoweroffId tgName typeName infoStatusName dateDay orgNos nowTime countyName streetName villageName roadName communityName tranName sdLineName provinceCode".split()
    drop_item2 = 'subsName infoStatus orgName orgNo powerType powerOffArea tgNo powerOffId'.split()
    drop_item3 = "powerComm subsNo lineNo".split()
    drop_item4 = 'powerOffReason stopDate'.split()

    for itm in ( drop_item1, drop_item2, drop_item3, drop_item4):
        bodf.drop( itm, axis=1, inplace=True)
    
    bodf.drop_duplicates(['poweroffId'], inplace=True)
    print(" all item droped;")
    return


# 把以上工作合并为一个方法，直接对json路径调用即可获得数据集
def cityfolder_toDF( folderpath:'str') -> pd.DataFrame:
    df = makedf(folderpath)
    dropitems(bodf=df)
    
    return df

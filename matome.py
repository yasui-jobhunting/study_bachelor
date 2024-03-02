import pandas as pd
import glob
import os

def merge(folder_name):
    path = glob.glob(f'{folder_name}/*.csv')
    #空のExcelフォルダを作成
    base_df = pd.DataFrame()

    for path_obj in path:
        df = pd.read_csv(path_obj, header=None)
        df = df.iloc[:,1]
        base_df = pd.concat([base_df,df],axis=1)

    #base_listという空のファイルを作る
    base_list = []

    for file in path:
        file_name = os.path.basename(file)
        base_list.append(file_name)
    
    base_df.columns =base_list
    base_df.index = pd.read_csv(path_obj,header=None).iloc[:,0] 
    
    return base_df.T
    

# 3つのスペクトル平均化関数の定義
def mean(df):
    # 空のDataFrame準備
    base_X = pd.DataFrame()
    # 3列平均化後のスペクトル本数
    n = int(len(df)/3) #割り算をすると浮動小数点型（float）になるので整数型に直す
    for i in range(n):
        # 平均化する3つのスペクトル抽出
        df3 = df.iloc[i*3:3*i+3]
        # 平均化
        mean_i = df3.mean(axis=0) #axis=0だと縦
        # 空のDataFrameに結合
        base_X = pd.concat([base_X,mean_i],axis=1)
        
    # データの名前取得
    df_index = df.index
    base_X_name = [df_index[i*3] for i in range(n)]
    base_X.columns = base_X_name
    return base_X.T


import numpy as np
import math
#クベルカムンク変換関数km
def km(Xabs):
    ln10 = math.log(10)
    Xkm = np.cosh(Xabs*ln10)-1
    return Xkm


# snv関数の定義
def snv(X_NM):
    # 入力がNumpyのarray配列の場合はDataFrameに直す
    if type(X_NM) == np.ndarray:
        X_NM = pd.DataFrame(X_NM)
    # 各行ごとにsnv変換を用いる
    X_snv = X_NM.apply(lambda x:(x-x.mean())/x.std(),axis=1) #lambda x:(x-x.mean())/x.std()はsnv変換の式
    return X_snv

#中心化
def cent(X_NM):
    return X_NM.apply(lambda x:x-x.mean(),axis=0)
    
# coding=utf-8
from __future__ import division  # #保留两整数相除取浮点数
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
# #用于将日线数据转换为周线、月线，计算ma、macd、ene等指标
##根据日线、5分线、实时数据获取macd等参数

class stockindicatorutils(object):
    def __init__(self):
        print('***********调用股票技术指标工具***********')

    def MACD(df, n_fast=12, n_slow=26):
        EMAfast = df['close'].ewm(ignore_na=False, span=n_fast, min_periods=n_fast - 1, adjust=True).mean()
        EMAslow = df['close'].ewm(ignore_na=False, span=n_slow, min_periods=n_slow - 1, adjust=True).mean()
        df['diff'] = EMAfast - EMAslow
        df['dea'] = df['diff'].ewm(ignore_na=False, span=9, min_periods=8, adjust=True).mean()
        df['macd'] = 2 * (df['diff'] - df['dea'])
        return df

    def ENE(df):
        ma11 = df['close'].rolling(window=11, center=False).mean()
        df['upper'] = float(1 + 10.0 / 100) * ma11
        df['lower'] = float(1 - 9.0 / 100) * ma11
        df['ene'] = (df['upper'] + df['lower']) / 2
        return df

    def MA(df, ma_list=[5, 10, 20, 60]):
        for ma in ma_list:
            df['MA_' + str(ma)] = df['close'].rolling(window=ma, center=False).mean()
        return df

    def KDJ_OLD(df, fastk=9):
        low = df['low'].rolling(window=fastk, min_periods=1, center=False).min()
        high = df['high'].rolling(window=fastk, min_periods=1, center=False).max()
        rsv = (df['close'] - low) / (high - low) * 100
        df['KDJ_K'] = rsv.ewm(ignore_na=False, min_periods=0, adjust=True, com=2).mean()
        df['KDJ_D'] = df['KDJ_K'].ewm(ignore_na=False, min_periods=0, adjust=True, com=2).mean()
        df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
        return df


    #將日线转换为周线、月线
    #return: OHLC,volume,price_change,p_change
    def resample(df, _period_='W'):
        dat = df.resample(_period_).last()
        dat['open'] = df['open'].resample(_period_).first()
        dat['high'] = df['high'].resample(_period_).max()
        dat['low'] = df['low'].resample(_period_).min()
        dat['volume'] = df['volume'].resample(_period_).sum()
        dat['close'] = df['close'].resample(_period_).last()
        if 'amount' in dat.columns:
            dat['amount'] = df['amount'].resample(_period_).sum()
            dat.dropna(inplace=True)
            return dat[['open', 'high', 'low', 'close', 'volume', 'amount']]
            #dat['price_change'] = df['price_change'].resample(_period_).sum()
            #dat['p_change'] = df['p_change'].resample(_period_).apply(lambda x: (x + 1.0).prod() - 1.0)
        dat.dropna(inplace=True)
        return dat[['open', 'high', 'low', 'close', 'volume']]


    def EMA(DF, N):
        return pd.Series.ewm(DF, span=N, min_periods=N - 1, adjust=True).mean()


    def SMA(DF, N, M):
        DF = DF.fillna(0)
        z = len(DF)
        var = np.zeros(z)
        var[0] = DF[0]
        for i in range(1, z):
            var[i] = (DF[i] * M + var[i - 1] * (N - M)) / N
        for i in range(z):
            DF[i] = var[i]
        return DF

    def ATR(self,DF, N):
        C = DF['close']
        H = DF['high']
        L = DF['low']
        TR1 =self.MAX(self.MAX((H - L),self.ABS(self.REF(C, 1) - H)), self.ABS(self.REF(C, 1) - L))
        atr =self.MA(TR1, N)
        return atr

    def HHV(self,DF, N):
        return pd.Series.rolling(DF, N).max()

    def LLV(self,DF, N):
        return pd.Series.rolling(DF, N).min()

    def SUM(self,DF, N):
        return pd.Series.rolling(DF, N).sum()

    def ABS(self,DF):
        return abs(DF)

    def MAX(self,A, B):
        var = self.IF(A > B, A, B)
        return var


    def MIN(self,A, B):
        var = self.IF(A < B, A, B)
        return var


    def IF(self,COND, V1, V2):
        var = np.where(COND, V1, V2)
        for i in range(len(var)):
          V1[i] = var[i]
        return V1

    def REF(self,DF, N):
        var = DF.diff(N)
        var = DF - var
        return var


    def STD(self,DF, N):
        return pd.Series.rolling(DF, N).std()


    def MACD(self,DF, FAST, SLOW, MID):
        EMAFAST =self.EMA(DF, FAST)
        EMASLOW =self.EMA(DF, SLOW)
        DIFF = EMAFAST - EMASLOW
        DEA = self.EMA(DIFF, MID)
        MACD = (DIFF - DEA) * 2
        DICT = {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD}
        VAR = pd.DataFrame(DICT)
        return VAR


    def KDJ(self,DF, N, M1, M2):
        C = DF['close']
        H = DF['high']
        L = DF['low']
        RSV = (C - self.LLV(L, N)) / (self.HHV(H, N) - self.LLV(L, N)) * 100
        K = self.SMA(RSV, M1, 1)
        D = self.SMA(K, M2, 1)
        J = 3 * K - 2 * D
        DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}
        VAR = pd.DataFrame(DICT)
        return VAR


    def OSC(self,DF, N, M):  #变动速率线
        C = DF['close']
        OS = (C - self.MA(C, N)) * 100
        MAOSC = self.EMA(OS, M)
        DICT = {'OSC': OS, 'MAOSC': MAOSC}
        VAR = pd.DataFrame(DICT)
        return VAR


    def BBI(self,DF, N1, N2, N3, N4):  #多空指标
        C = DF['close']
        bbi = (self.MA(C, N1) + self.MA(C, N2) + self.MA(C, N3) + self.MA(C, N4)) / 4
        DICT = {'BBI': bbi}
        VAR = pd.DataFrame(DICT)
        return VAR


    def BBIBOLL(self,DF, N1, N2, N3, N4, N, M):  #多空布林线
        bbiboll = self.BBI(DF, N1, N2, N3, N4)
        UPER = bbiboll + M * self.STD(bbiboll, N)
        DOWN = bbiboll - M * self.STD(bbiboll, N)
        DICT = {'BBIBOLL': bbiboll, 'UPER': UPER, 'DOWN': DOWN}
        VAR = pd.DataFrame(DICT)
        return VAR


    def PBX(self,DF, N1, N2, N3, N4, N5, N6):  #瀑布线
        C = DF['close']
        PBX1 = (self.EMA(C, N1) + self.EMA(C, 2 * N1) + self.EMA(C, 4 * N1) ) / 3
        PBX2 = (self.EMA(C, N2) + self.EMA(C, 2 * N2) + self.EMA(C, 4 * N2) ) / 3
        PBX3 = (self.EMA(C, N3) + self.EMA(C, 2 * N3) + self.EMA(C, 4 * N3) ) / 3
        PBX4 = (self.EMA(C, N4) + self.EMA(C, 2 * N4) + self.EMA(C, 4 * N4) ) / 3
        PBX5 = (self.EMA(C, N5) + self.EMA(C, 2 * N5) + self.EMA(C, 4 * N5) ) / 3
        PBX6 = (self.EMA(C, N6) + self.EMA(C, 2 * N6) + self.EMA(C, 4 * N6) ) / 3
        DICT = {'PBX1': PBX1, 'PBX2': PBX2, 'PBX3': PBX3, 'PBX4': PBX4, 'PBX5': PBX5, 'PBX6': PBX6}
        VAR = pd.DataFrame(DICT)
        return VAR


    def BOLL(self,DF, N):  #布林线
        C = DF['close']
        boll = self.MA(C, N)
        UB = boll + 2 * self.STD(C, N)
        LB = boll - 2 * self.STD(C, N)
        DICT = {'BOLL': boll, 'UB': UB, 'LB': LB}
        VAR = pd.DataFrame(DICT)
        return VAR


    def ROC(self,DF, N, M):  #变动率指标
        C = DF['close']
        roc = 100 * (C - self.REF(C, N)) /self.REF(C, N)
        MAROC = self.MA(roc, M)
        DICT = {'ROC': roc, 'MAROC': MAROC}
        VAR = pd.DataFrame(DICT)
        return VAR


    def MTM(self,DF, N, M):  #动量线
       C = DF['close']
       mtm = C - self.REF(C, N)
       MTMMA = self.MA(mtm, M)
       DICT = {'MTM': mtm, 'MTMMA': MTMMA}
       VAR = pd.DataFrame(DICT)
       return VAR


    def MFI(self,DF, N):  #资金指标
       C = DF['close']
       H = DF['high']
       L = DF['low']
       VOL = DF['volume']
       INDEX=DF['date']
       TYP = (C + H + L) / 3
       V1 = self.SUM(self.IF(TYP > self.REF(TYP, 1), TYP * VOL, 0), N) / self.SUM(self.IF(TYP < self.REF(TYP, 1), TYP * VOL, 0), N)
       mfi = 100 - (100 / (1 + V1))
       DICT = {'MFI': mfi}
       return pd.DataFrame(DICT)


    def SKDJ(self,DF, N, M):
       CLOSE = DF['close']
       LOWV = self.LLV(DF['low'], N)
       HIGHV = self.HHV(DF['high'], N)
       RSV = self.EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
       K = self.EMA(RSV, M)
       D = self.MA(K, M)
       DICT = {'SKDJ_K': K, 'SKDJ_D': D}
       VAR = pd.DataFrame(DICT)
       return VAR


    def WR(self,DF, N, N1):  #威廉指标
       HIGH = DF['high']
       LOW = DF['low']
       CLOSE = DF['close']
       WR1 = 100 * (self.HHV(HIGH, N) - CLOSE) / (self.HHV(HIGH, N) - self.LLV(LOW, N))
       WR2 = 100 * (self.HHV(HIGH, N1) - CLOSE) / (self.HHV(HIGH, N1) - self.LLV(LOW, N1))
       DICT = {'WR1': WR1, 'WR2': WR2}
       VAR = pd.DataFrame(DICT)
       return VAR


    def BIAS(self,DF, N1, N2, N3):  #乖离率
       CLOSE = DF['close']
       BIAS1 = (CLOSE - self.MA(CLOSE, N1)) / self.MA(CLOSE, N1) * 100
       BIAS2 = (CLOSE - self.MA(CLOSE, N2)) / self.MA(CLOSE, N2) * 100
       BIAS3 = (CLOSE - self.MA(CLOSE, N3)) / self.MA(CLOSE, N3) * 100
       DICT = {'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3}
       VAR = pd.DataFrame(DICT)
       return VAR


    def RSI(self,DF, N1, N2, N3):  #相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;
       CLOSE = DF['close']
       LC = self.REF(CLOSE, 1)
       RSI1 = self.SMA(self.MAX(CLOSE - LC, 0), N1, 1) / self.SMA(self.ABS(CLOSE - LC), N1, 1) * 100
       RSI2 = self.SMA(self.MAX(CLOSE - LC, 0), N2, 1) / self.SMA(self.ABS(CLOSE - LC), N2, 1) * 100
       RSI3 = self.SMA(self.MAX(CLOSE - LC, 0), N3, 1) / self.SMA(self.ABS(CLOSE - LC), N3, 1) * 100
       DICT = {'RSI1': RSI1, 'RSI2': RSI2, 'RSI3': RSI3}
       VAR = pd.DataFrame(DICT)
       return VAR


    def ADTM(self,DF, N, M):  #动态买卖气指标
       HIGH = DF['high']
       LOW = DF['low']
       OPEN = DF['open']
       DTM = self.IF(OPEN <= self.REF(OPEN, 1), 0, self.MAX((HIGH - OPEN), (OPEN - self.REF(OPEN, 1))))
       DBM = self.IF(OPEN >= self.REF(OPEN, 1), 0, self.MAX((OPEN - LOW), (OPEN - self.REF(OPEN, 1))))
       STM = self.SUM(DTM, N)
       SBM = self.SUM(DBM, N)
       ADTM1 = self.IF(STM > SBM, (STM - SBM) / STM, self.IF(STM == SBM, 0, (STM - SBM) / SBM))
       MAADTM = self.MA(ADTM1, M)
       DICT = {'ADTM': ADTM1, 'MAADTM': MAADTM}
       VAR = pd.DataFrame(DICT)
       return VAR


    def DDI(self,DF, N, N1, M, M1):  #方向标准离差指数
       H = DF['high']
       L = DF['low']
       DMZ = self.IF((H + L) <= (self.REF(H, 1) + self.REF(L, 1)), 0, self.MAX(self.ABS(H-self.REF(H, 1)), self.ABS(L-self.REF(L, 1))))
       DMF = self.IF((H + L) >= (self.REF(H, 1) + self.REF(L, 1)), 0, self.MAX(self.ABS(H-self.REF(H, 1)), self.ABS(L -self.REF(L, 1))))
       DIZ = self.SUM(DMZ, N) / (self.SUM(DMZ, N) + self.SUM(DMF, N))
       DIF = self.SUM(DMF, N) / (self.SUM(DMF, N) + self.SUM(DMZ, N))
       ddi = DIZ - DIF
       ADDI = self.SMA(ddi, N1, M)
       AD = self.MA(ADDI, M1)
       DICT = {'DDI': ddi, 'ADDI': ADDI, 'AD': AD}
       VAR = pd.DataFrame(DICT)
       return VAR


   # def ADX(DF, N=14):
   #    H = DF['high']
   #    L = DF['low']
   #    C = DF['close']
   #    PDI = ta.PLUS_DI(H.values, L.values, C.values, N)
   #    MDI = ta.MINUS_DI(H.values, L.values, C.values, N)
   #    DX = ta.DX(H.values, L.values, C.values, N)
   #    ADX = ta.ADX(H.values, L.values, C.values, N)
   #    VAR = pd.DataFrame({'PDI': PDI, 'MDI': MDI, 'DX': DX, 'ADX': ADX}, index=H.index.values)
   #    return VAR


   # def AROON(DF, N=20):
   #    H = DF['high']
   #    L = DF['low']
   #    AD, AP = ta.AROON(H.values, L.values, N)
   #    AR = AP - AD
   #    VAR = pd.DataFrame({'AROON': AR, 'AROON_UP': AP, 'AROON_DOWN': AD}, index=H.index.values)
   #    return VAR


   # def CCI(DF, N=20):
   #    H = DF['high']
   #    L = DF['low']
   #    C = DF['close']
   #    CCI = ta.CCI(H.values, L.values, C.values, N)
   #    VAR = pd.DataFrame({'CCI': CCI}, index=H.index.values)
   #    return VAR


if __name__ == '__main__':
    code = '001696'
    data = ts.get_k_data(code)
    index = list(data['date'])
    newdata = stockindicatorutils().MFI(DF=data, N=5)
    MFI = list(newdata['MFI'])
    newshow = pd.DataFrame({'MFI':MFI},index=index)
    plt.plot(newshow.tail(20))
    plt.grid()##添加网格
    plt.show()
    #print CCI(a).tail()

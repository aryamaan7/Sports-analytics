import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

Eng18 = pd.read_excel("C:/Users/aryam/Downloads/Engsoccer2017-18.xlsx")
print(Eng18.columns.tolist())

Eng18['hwinvalue']=np.where(Eng18['FTR']=='H',1,np.where(Eng18['FTR']=='D',0.5,0))
Eng18['awinvalue']=np.where(Eng18['FTR']=='A',1,np.where(Eng18['FTR']=='D',0.5,0))
Eng18['count']=1

Enghome = Eng18.groupby(['HomeTeam', 'Div'])['count','hwinvalue','FTHG','FTAG'].sum().reset_index()
Enghome = Enghome.rename(columns={'HomeTeam':'team','count':'Ph','FTHG':'FTHGh', 'FTAG':'FTAGh'})
Enghome

Engaway = Eng18.groupby('AwayTeam')['count','awinvalue','FTHG','FTAG'].sum().reset_index()
Engaway = Engaway.rename(columns={'AwayTeam': 'team','count':'Pa','FTHG':'FTHGa','FTAG':'FTAGa'})
Engaway

Eng18 = pd.merge(Enghome, Engaway, on=['team'])
Eng18

Eng18['W'] = Eng18['hwinvalue']+Eng18['awinvalue']
Eng18['G'] = Eng18['Ph']+Eng18['Pa']
Eng18['GF'] = Eng18['FTHGh']+Eng18['FTAGa']
Eng18['GA'] = Eng18['FTAGh']+Eng18['FTHGa']
Eng18

Eng18['wpc']=Eng18['W']/Eng18['G']
Eng18['pyth']=Eng18['GF']**2/(Eng18['GF']**2+Eng18['GA']**2)
sns.relplot(x="pyth",y="wpc",data=Eng18, hue='Div')

pyth_lm = smf.ols(formula = 'wpc ~ pyth', data=Eng18).fit()
pyth_lm.summary()

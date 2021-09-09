# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 11:02:33 2021

@author: Fabio Diuana
"""


#%%
# =============================================================================
# Converting daily data to monthly data part1
# =============================================================================

filem = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado','Vazões_Diárias_1931_2019_tripa.csv')
df = pd.read_csv(filem, decimal =',', sep=';', encoding='latin1')

sd = int(df.Data.min().split('/')[-1])
fd = int(df.Data.max().split('/')[-1])
d1 = datetime.date(sd, 1, 1)
d2 = datetime.date(fd, 12, 31)
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]

df['Data2'] = dd      

df['Data2'] = pd.to_datetime(df['Data2'])
df.set_index('Data2', inplace=True)
dfw = df.copy()
#%%
# =============================================================================
# Converting daily data to monthly data part 2
# ============================================================================= 
months = df.index.month
df['months'] = months
dfm = df.resample('M').mean()

dfm['year'] = dfm.index.year
dfm.reset_index(inplace=True)

dfm = dfm[['year', 'months'] + dfm.columns[1:-2].values.tolist()]

filemout = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado','Vazões_Diárias_1931_2019_tripa_Mensal.csv')
dfm.to_csv(filemout, decimal =',', sep=';', encoding='latin1')

#%%


dfw['year'] = dfw.index.year
df82 = dfw[dfw['year'] >=1982]
NaN_Cols = df82.columns[df82.isna().any()].tolist()
for uhe in NaN_Cols:
    if uhe == 'RONDON II (145)':
        a = 0.0168
        b = 46.2362
        ref = 'TELES PIRES (229)'
    elif uhe == 'RETIRO BAIXO (155)':
        a = 0.1798
        b = 8.3059
        ref = 'TRES MARIAS (156)'        
    elif uhe == 'BALBINA (269)':
        a = 0.4201
        b = 231.5632
        ref =  'FERREIRA GOMES (297)'
    else:
        print('You need to set linear regression parameters for '+uhe+' in order to extend flow data series')
        break

    df82[uhe] = np.where(df82[uhe].isnull(), df82[ref]*a + b, df82[uhe]) #replacing NaN values based on linear regression


filemout = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado','Vazões_Diárias_1982_2019_tripa_Completo.csv')
df82.to_csv(filemout, decimal =',', sep=';', encoding='latin1')




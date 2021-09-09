# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 15:03:21 2021

@author: Fabio Diuana
"""

"""
THIS SCRIPT CONVERTS THE ORIGINAL FILES
TO A BETTER FORMAT TO WORK ON THEM
"""
# =============================================================================
# Converting monthly data from ONS format to dataframe with hidro stations as columns 
# =============================================================================

#add poath to your file
filem = os.path.join(MyPath, 'Dados', 'Hidro', 'Original', 'Vazões_Mensais_1931_2019.xlsx')

df = pd.read_excel(filem) 
#value inside parenthesis is the station code not the hpp code

header = ['Station', 'YEAR'] + [str(ll) for ll in range(1,13)]

df = df.iloc[:,:-2]
df.columns = header

df = df.iloc[1:]

inds = pd.isnull(df).all(1)

#rows_with_nan = [index for index, row in df.iterrows() if row.isnull().all()]

inds =  df.index[pd.isnull(df).all(1) == True].tolist()
inds = [0] + inds


for idx in range(len(inds)-1):
    idx_s = inds[idx]+1
    idx_f = inds[idx+1]-1
    
    dfaux = df.loc[idx_s:idx_f]
    dfaux = dfaux.iloc[0:-3]
    
    name = dfaux.iloc[0,0]
    print(name)
    print(idx)
    if str(name) == 'nan':
        name = 'STA BRANCA T (54)' #based on comparison between 2019 and 2018 file
    
    dfaux2 = dfaux.iloc[:,1:].set_index('YEAR').stack()
    dfaux2 = dfaux2.reset_index()
    dfaux2.columns = ['YEAR', 'MONTH', 'VALUE']

    if idx == 0:
        fdf = dfaux2.iloc[:,:-1].copy()  

    fdf[name] = dfaux2['VALUE']
    
print('finished')
#add poath to save csv file
filemout = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado', 'Vazões_Mensais_1931_2019_tripa.csv')
fdf.to_csv(filemout, decimal =',', sep=';', index = False, encoding='latin1')
#%%
# =============================================================================
# Converting monthly data from VAZOES.DAT format to dataframe with hidro stations as columns 
# =============================================================================

#add poath to your file
filem = os.path.join(MyPath,'Dados', 'Original', 'Vazoes.xlsx')

df = pd.read_excel(filem) 

df1 = df.set_index(['Posto', 'Ano'])
df2 = df1.stack()
df3 = df2.unstack('Posto')

df3.reset_index(inplace=True)
df3.columns = ['Ano', 'Mes'] + df3.columns[2:].values.tolist()

filemout = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado', 'Vazoes_PDE_tripa.csv')
df3.to_csv(filemout, decimal =',', sep=';', index = False, encoding='latin1')

#%%
# =============================================================================
# ADJUSTING DAILY FLOW DATA FILE
# =============================================================================
#add poath to your file
filem = os.path.join(MyPath,'Dados', 'Hidro', 'Original', 'Vazões_Diárias_1931_2019.xlsx')

df = pd.read_excel(filem, skiprows=5) 
df.drop(df.index[[0]], inplace=True)

df.columns = ['Data'] + df.columns[1:].values.tolist()

filemout = os.path.join(MyPath, 'Dados', 'Hidro', 'Modificado', 'Vazões_Diárias_1931_2019_tripa.csv')
df.to_csv(filemout, decimal =',', sep=';', index = False, encoding='latin1')



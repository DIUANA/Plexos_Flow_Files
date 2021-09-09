# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:33:16 2021

@author: Fabio Diuana
"""


# =============================================================================
# ADDING EXPANSION
# =============================================================================
Exp_nameo = ['JARDIM OURO', 'MIRADOR', "MARANHAO BAIXO", "ITAGUAÇU", "FOZ PIQUIRI", 
             "P. GALEANO", "SAUDADE", "FOZ DO XAXIM", "STOANTCHAP"]

Exp_codeo = []

if len(Exp_nameo) >0:
    Exp_name = Exp_nameo[:]
    
    #looking for power plant which the name starts with the first five letters of the pp that was set
    Exp_code = [caduhe[caduhe['Usina'].str.startswith(ll[:5])]['Posto'].values.tolist() for ll in Exp_nameo] 
    for nn in range(len(Exp_code)):
        if len(Exp_code[nn]) >1:
            print("\nCheck if there are more than one UHE with name starting with: " + Exp_name[nn] )
            break
        elif len(Exp_code[nn]) <1:
            print("\nCheck if the name: " + Exp_name[nn] + " is corrected" ) 
            break

    Exp_code = list(itertools.chain(*Exp_code))
            
elif len(Exp_codeo) >0:
    Exp_code = Exp_codeo[:]
    Exp_name = [caduhe[caduhe['Posto'] == ll]['Usina'].values.tolist() for ll in Exp_codeo]
else:
    print("there is no expansion defined")
    


#%%
# =================================================================================
# ADDING DATA RELATED TO UHES FROM PLANNING EXPANSION CAPACITY FROM PDE 29
# UHEs which daily flow data was generated
# =================================================================================

filepath = os.path.join(MyPath, 'Dados','Hidro', 'Modificado','Vazões_Diárias_1982_2019_tripa_Completo.csv')
df = pd.read_csv(filepath, decimal=',', sep=';', encoding='latin1')

df19 = df[df['year']==2019]
df18 = df[df['year']==2018]
df19.mean().mean()
df18.mean().mean()
fx = (df19.mean().mean() - df18.mean().mean())/df18.mean().mean()
#df18.mean().mean()*(1+fx)

#%%
# =============================================================================
# getting flow data from old expansion
# =============================================================================
filepath = os.path.join(MyPath, 'Dados', 'Hidro','Expansão','Uhes_Expansao_PDE29.csv')
dfe = pd.read_csv(filepath, decimal=',', sep=';', encoding='latin1')


sd = int(dfe.Data.min().split('/')[-1])
fd = int(dfe.Data.max().split('/')[-1])
d1 = datetime.date(sd, 1, 1)
d2 = datetime.date(fd, 12, 31)
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]

dfe['Data2'] = dd      

dfe['Data2'] = pd.to_datetime(dfe['Data2'])
dfe.set_index('Data2', inplace=True)

d1 = datetime.date(sd, 1, 1)
d2 = datetime.date(2019, 12, 31)
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
      
dfef = pd.DataFrame(columns=['Data'])
dfef['Data'] = dd      

dfef['Data'] = pd.to_datetime(dfef['Data'])
dfef.set_index('Data', inplace=True)

dfe2 = pd.merge(dfef, dfe.iloc[:,1:], how='left', right_index=True, left_index=True)

#%%
# =============================================================================
# PDE EXPANSAION for new UHEs --> taking flow data form monthly PDE data
# =============================================================================
filemout = os.path.join(MyPath, 'Dados','Hidro','Modificado', 'Vazoes_PDE_tripa.csv')
dfpde30 = pd.read_csv(filemout, decimal=',', sep=';', encoding='latin1')
dfpde30_s = dfpde30[['Ano', 'Mes'] + [str(ll) for ll in Exp_code]]
dfpde30_s = dfpde30_s[dfpde30_s['Ano']>=sd]
dfpde30_s.columns = ['Ano', 'Mes'] + [ll+' ('+str(nn)+')' for ll,nn in zip(Exp_name, Exp_code)]

d2 = datetime.date(int(dfpde30_s.Ano.max()), 12, 31)
dates = pd.date_range(d1, d2, freq='D')
mdates = pd.date_range(d1, d2, freq='M')
mdates = [m.replace(day=1) for m in mdates]
dfpde30_s['Data'] = mdates
dfpde30_s.set_index('Data', inplace=True)

dfpde30_s_dia = dfpde30_s.reindex(dates, method='ffill')
#%%
# =============================================================================
# merging old expansion with new expansion
# =============================================================================
dfet = pd.merge(dfe2, dfpde30_s_dia.iloc[:,2:], how='left', right_index=True, left_index=True)

dfet18 = dfet[dfet.index.year<=2018]
dfet19 = dfet[dfet.index.year==2019]

#adding data for 2019 based on 2018 using fx (mean variation of the flow in the system from 2019 to 2018)
for nn in dfet.columns:
    dfet19[nn] = dfet[dfet.index.year==2018][nn].values *(1+fx)
    
dfet = pd.concat([dfet18, dfet19])
dfet.index.names = ['Data2']
#%%
# =============================================================================
# adding expansion in the flow data series file
# =============================================================================
df['Data2'] = pd.to_datetime(df['Data2'])
df.set_index('Data2', inplace=True)
df = df.iloc[:,1:-1]#removing last column

for nn in dfet.columns:
    df[nn] = dfet[nn]

filemout = os.path.join(MyPath, 'Dados','Hidro', 'Modificado','Vazões_Diárias_1982_2019_tripa_Completo+Exp.csv')
df.to_csv(filemout, decimal =',', sep=';', encoding='latin1')

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 13:52:27 2021

@author: Fabio Diuana
"""
# =============================================================================
# ADJUSTING DAILY FLOW VALUES BASED ON MONTHLY FLOW DATA obtained from PDE 
# TO MAKE MONTHLY AVERAGE FROM DAILY DATA MATCH MONTHLY DATA 
# =============================================================================

"""
iT MEANS WE ARE ASSUMING THE MONTHLY DATA IS CORRECT, 
THEN WE ARE KEEPING THE DAILY PROFILE BUT ADJUSTING ITS INTENSITY TO MATCH WITH MONTHLY DATA
"""

filemout = os.path.join(MyPath, 'Dados','Hidro','Modificado', 'Vazoes_PDE_tripa.csv')
dfpde = pd.read_csv(filemout, decimal=',', sep=';', encoding='latin1')
dfpde = dfpde[dfpde['Ano'] >=1982]
#add datetime to PDE FILE
d1 = datetime.date(1982, 1, 1)
d2 = datetime.date(int(dfpde.Ano.max()), 12, 31)
dates = pd.date_range(d1, d2, freq='D')
mdates = pd.date_range(d1, d2, freq='M')
mdates = [m.replace(day=1) for m in mdates]
dfpde['Data2'] = mdates
dfpde['Data2'] = pd.to_datetime(dfpde['Data2'])
dfpde.set_index('Data2', inplace=True)
#%%
filemout = os.path.join(MyPath, 'Dados','Hidro','Modificado', 'Vazões_Mensais_1931_2019_tripa.csv')
dfonsM = pd.read_csv(filemout, decimal=',', sep=';', encoding='latin1')

filemout = os.path.join(MyPath, 'Dados','Hidro', 'Modificado','Vazões_Diárias_1982_2019_tripa_Completo+Exp.csv')
dfonsD = pd.read_csv(filemout, sep=';', decimal=',', encoding='latin1')

dfonsM2 = dfonsM.copy()
dfonsM2.columns = dfonsM2.columns[:2].tolist() + [ll.split('(')[-1].split(')')[0] for ll in dfonsM2.columns[2:]]


dfonsD2 = dfonsD.copy()
dfonsD2.columns = dfonsD2.columns[:1].tolist() + [ll.split('(')[-1].split(')')[0] for ll in dfonsD2.columns[1:]]
dfonsD2['Data2'] = pd.to_datetime(dfonsD2['Data2'])
dfonsD2.set_index('Data2', inplace=True)


#%%
dfonsD2_adj = dfonsD2.copy()
dfonsD2_adj.reset_index(inplace=True)


#%%
#ajustando todas as usinas para bater com o mensal do PDE

for cc in dfonsD2.columns[2:]:
    print(cc)
    print(caduhe[caduhe['Posto']==int(cc)]['Usina'].values)
    print('')
    
    if cc in dfpde.columns[2:-1]:

        uhe_adj = dfonsD2[[cc]].copy()
        uhe_adj['YEAR'] = uhe_adj.index.year.values.tolist()
        uhe_adj['MONTH'] = uhe_adj.index.month.values.tolist()
        uhe_adj_md = uhe_adj.resample('M').mean()
        uhe_adj_md.reset_index(drop=True, inplace=True)


        pde_cc = dfpde[[cc]].copy() #[pc for pc in df_pde29.columns if pc.endswith(posto[1:-1])][0]       
        uhe_pde_m = pde_cc.copy()
        uhe_pde_m['YEAR'] = uhe_pde_m.index.year.values.tolist()
        uhe_pde_m['MONTH'] = uhe_pde_m.index.month.values.tolist()
        uhe_pde_m.reset_index(drop=True,inplace=True)

        
        aux = uhe_adj_md[uhe_adj_md['YEAR']<=uhe_pde_m['YEAR'].max()].copy()
        C = uhe_pde_m[cc] / aux[cc]
        C = C.values.tolist()
        C = [1 if math.isnan(x) else x for x in C]
        
        aux['C'] = C
 
        #start here    
        for ya in list(range(1982,2019)):
            #print(ya)
            for m in range(1,13):
                #print(m)
                dfonsD2_adj[cc] = np.where( np.logical_and(dfonsD2_adj['Data2'].dt.year == ya, dfonsD2_adj['Data2'].dt.month == m), 
                                            dfonsD2_adj[cc] * aux[(aux['YEAR'] == ya) & (aux['MONTH'] == m)]['C'].values.tolist()[0],
                                                        dfonsD2_adj[cc])
                
                
#%%
#ajustando todas as usinas para bater com o mensal do ONS no último ano

for cc in dfonsD2.columns[2:]:
    print(cc)
    print(caduhe[caduhe['Posto']==int(cc)]['Usina'].values)
    print('')
    
    if cc in dfonsM2.columns[2:-1]:

        uhe_adj = dfonsD2[[cc]].copy()
        uhe_adj['YEAR'] = uhe_adj.index.year.values.tolist()
        uhe_adj['MONTH'] = uhe_adj.index.month.values.tolist()
        uhe_adj_md = uhe_adj.resample('M').mean()
        uhe_adj_md.reset_index(drop=True, inplace=True)


        ons_m_cc = dfonsM2[['YEAR', 'MONTH', cc]].copy() #[pc for pc in df_pde29.columns if pc.endswith(posto[1:-1])][0]       
        ons_m = ons_m_cc.copy()
        ons_m2 = ons_m[ons_m['YEAR'] > dfpde.index.year.max()]
        ons_m2.reset_index(drop=True, inplace=True)


        
        aux = uhe_adj_md[uhe_adj_md['YEAR'] > dfpde.index.year.max() ].copy()
        aux.reset_index(drop=True, inplace=True)
        C = ons_m2[cc] / aux[cc]
        C = C.values.tolist()
        C = [1 if math.isnan(x) else x for x in C]
        
        aux['C'] = C
 
        #start here    
        for ya in [2019]:
            #print(ya)
            for m in range(1,13):
                #print(m)
                dfonsD2_adj[cc] = np.where( np.logical_and(dfonsD2_adj['Data2'].dt.year == ya, dfonsD2_adj['Data2'].dt.month == m), 
                                            dfonsD2_adj[cc] * aux[(aux['YEAR'] == ya) & (aux['MONTH'] == m)]['C'].values.tolist()[0],
                                                        dfonsD2_adj[cc])
                
#%%
# =============================================================================
# exporting natural daily flow datafile            
# =============================================================================
              
dfonsD2_adj.columns = ['Data2'] + dfonsD.columns[1:].tolist()             

dfonsD2_adj.rename(columns={'Data2':'Data'}, inplace=True)
dfonsD2_adj['Data'] =  pd.to_datetime(dfonsD2_adj['Data'])
dfonsD2_adj['Data'] = dfonsD2_adj["Data"].dt.strftime("%m/%d/%Y")

dfonsD2_adj.iloc[:,1:] = dfonsD2_adj.iloc[:,1:].round(2)

files = os.listdir(os.path.join(MyPath, 'Dados', 'Modificado'))
if any([ll.startswith('Vazões_Diárias_1982_2019_tripa_Completo+Exp_ADJ') for ll in files]):
    rv = [ll.split('_r')[-1] for ll in files if ll.startswith('Vazões_Diárias_1982_2019_tripa_Completo+Exp_ADJ') ]
    rv = [ll.split('.')[0] for ll in rv]
    rv = [int(ll[1]) if ll[0] == '0' else int(ll) for ll in rv]
    mrv = max(rv)
    mrv = mrv + 1
    smrv = str(mrv)
    if len(smrv)==1:
        smrv = '0'+smrv
    filen = 'Vazões_Diárias_1982_2019_tripa_Completo+Exp_ADJ_r'+smrv+'.csv'
else:
    filen = 'Vazões_Diárias_1982_2019_tripa_Completo+Exp_ADJ_r00.csv'
    
fileout = os.path.join(MyPath, 'Dados','Hidro', 'Modificado',filen)

dfonsD2_adj.to_csv(fileout,  sep=';', decimal=',', encoding='latin1', index=False)#, date_format='%m%d%Y')  


#a=dfonsD2_adj.columns

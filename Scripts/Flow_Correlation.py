# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 09:19:15 2021

@author: Fabio Diuana
"""

"""
FLOW CORRELATION SCRIPT
"""
from datetime import datetime as dt
startTime = dt.now()
import itertools
import pandas as pd
import numpy as np
import scipy
from scipy import stats
import datetime
#from datetime import datetime
from datetime import timedelta
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import os
import time
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import matplotlib.dates as mdates
#import pingouin as pg
model = LinearRegression()
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def get_corrs(df):
    col_correlations = df.corr()
    col_correlations.loc[:, :] = np.tril(col_correlations, k=-1)
    cor_pairs = col_correlations.stack()
    return cor_pairs.to_dict()

def isnotnan(value):
    return np.invert(np.isnan(value))




CASC_UHE = {                
    'Amazonas': 
    ['CACHOEIRA CALDEIRAO (204)',	'CURUA-UNA (277)',	'DARDANELOS (291)',	'FERREIRA GOMES (297)',	'GUAPORE (296)',	'JIRAU (285)',	
     'PIMENTAL (288)',	'RONDON II (145)',	'SAMUEL (279)',	'SANTO ANTONIO (MADEIRA) (287)',	'STO ANT JARI (290)',	'TELES PIRES (229)',	
     'COARACY NUN. (280)', 'BALBINA (269)', 'COLIDER (228)', 'SAO MANOEL (230)', 'SINOP (227)'], #'PIMENTAL - BELO MONTE (288)'

    'Doce':
    ['AIMORES (148)',	'BAGUARI (141)',	'CANDONGA (149)',	'GUILMAN-AMOR (262)',	'MASCARENHAS (144)',	'P. ESTRELA (263)',	
     'ROSAL (196)',	'SALTO GRANDE (134)'],

    'Grande':
    ['A. VERMELHA (18)',	'A.S.OLIVEIRA (16)',	'CACONDE (14)',	'CAMARGOS (1)',	'E. DA CUNHA (15)',	'ESTREITO (8)',	'FUNIL-GRANDE (211)',	'FURNAS (6)',	
     'IGARAPAVA (10)', 'ITUTINGA (2)',	'JAGUARA (9)',	'M. DE MORAES (7)',	'MARIMBONDO (17)',	'P. COLOMBIA (12)',	'VOLTA GRANDE (11)'],

    'Iguaçu':
    ['FUNDAO (72)',	'JORDAO (73)',	'SALTO CAXIAS (222)',	'SALTO OSORIO (78)',	'SEGREDO (76)',	'SLT.SANTIAGO (77)',	
     'STA CLARA PR (71)',	'G.B. MUNHOZ (74)', 'BAIXO IGUACU (81)'], #'G.B. MUNHOZ -Foz do Areia (74)'

    'Atl. Sul':
    ['14 DE JULHO (284)',	'CASTRO ALVES (98)',	'D. FRANCISCA (114)',	'ERNESTINA (110)',	'ITAUBA (113)',	'JACUI (112)',	
     'MONTE CLARO (97)',	'PASSO REAL (111)', 'G.P. SOUZA (115)', 'SALTO PILAO (101)'],

    'Paraguai':
    ['ITIQUIRA I (259)',	'JAURU (295)',	'MANSO (278)',	'PONTE PEDRA (281)'],

    'Paraíba do Sul': #'Atl. Sudeste'
    ['FUNIL (123)',	'ILHA POMBOS (130)',	'PARAIBUNA (121)',	'PICADA (197)',	'SANTA BRANCA (122)',	'SOBRAGI (198)',	'STA CECILIA (125)',	
     'ANTA (129)',	'JAGUARI (120)',	'LAJES (202)',	'TOCOS (201)', 'SANTANA (203)'], #'ANTA - Simplicio (129)'

    'Paranapanema':
    ['CANOAS I (52)',	'CANOAS II (51)',	'CAPIVARA (61)',	'CHAVANTES (49)',	'L.N. GARCEZ (50)',	'MAUA (57)',	'OURINHOS (249)',	
     'PIRAJU (48)',	'ROSANA (63)',	'TAQUARUCU (62)',	'A.A. LAYDNER (47)'], #'A.A. LAYDNER (47) (JURUMURIM)

    'Paranaíba':
    ['B. COQUEIROS (248)',	'BATALHA (22)',	'CACH.DOURADA (32)',	'CACU (247)',	'CAPIM BRANC1 (207)',	'CAPIM BRANC2 (28)',	'CORUMBA I (209)',	
     'CORUMBA III (23)', 'CORUMBA IV (205)',	'EMBORCACAO (24)',	'ESPORA (99)',	'FOZ DO RIO CLARO (261)',	'ITUMBIARA (31)',	'MIRANDA (206)',	
     'NOVA PONTE (25)',	'SALTO (294)',	'SAO SIMAO (33)',	 'SERRA FACAO (251)',	'SLT VERDINHO (241)' ] ,   

    'PR+Verde':
    ['I. SOLTEIRA (34)', 'SAO DOMINGOS (154)',	'JUPIA (245)',	'P. PRIMAVERA (246)',	'ITAIPU (266)'],

    'S. Francisco':
    ['ITAPARICA (172)',	'MOXOTO (173)',	'P.AFONSO (175)',	'QUEIMADO (158)',	'RETIRO BAIXO (155)',	
     'SOBRADINHO (169)',	'SOBRADINHO INCREMENTAL (168)',	'TRES MARIAS (156)',	'XINGO (178)'],

    'Tiete':
    ['BARRA BONITA (237)',	'IBITINGA (239)',	'NAVANHANDAVA (242)',	'PROMISSAO (240)',	'TRES IRMAOS (243)',	
    'A.S. LIMA (238)',	'ALTO TIETÊ (160)',	'GUARAPIRANGA (117)',	'EDGARD DE SOUZA+TRIBUT (161)'], #'A.S. LIMA - Bariri (238)'
    
    'Tocantins':
    ['CANA BRAVA (191)',	'ESTREITO TOCANTINS (271)',	'LAJEADO (273)',	'PEIXE ANGIC (257)',	'SAO SALVADOR (253)',	 'SERRA MESA (270)', 'TUCURUI (275)'],
    
    'Uruguai':
    ['BARRA GRANDE (215)',	'CAMPOS NOVOS (216)',	'FOZ CHAPECO (94)',	'GARIBALDI (89)',	'ITA (92)',	'MACHADINHO (217)',	
     'MONJOLINHO (220)',	'PASSO FUNDO (93)',	'PASSO SAO JOAO (103)',	'QUEBRA QUEIX (286)',	'SAO JOSE (102)'],

    'Atl. Leste':    
    ['IRAPE (255)', 'ITAPEBI (188)', 'P. CAVALO (254)', 'STA CLARA MG (283)'],

    'Avulsas':    
    ['B. ESPERANCA (190)',	'BILLINGS (118)', 'BILLINGS+PEDRAS (119)', 'A.DIAS+S.CAR (183)', 'PEDRAS (116)']
}

cascatas = list( CASC_UHE.keys() )

#%%
filem = os.path.join(MyPath, 'Dados', 'Hidro','Modificado','Vazões_Diárias_1931_2019_tripa.csv')
dfo = pd.read_csv(filem, decimal =',', sep=';', encoding='latin1')
uhel = list(itertools.chain(*list(CASC_UHE.values())))
missing_uhe = [ll for ll in dfo.columns[1:].tolist() if ll not in uhel]
extra_uhe = [ll for ll in uhel if ll not in dfo.columns[1:].tolist()]

if len(missing_uhe) >0:
    print('Missing following UHEs:')
    print(missing_uhe)
    
if len(extra_uhe) >0:
    print('There are extra UHEs in the list:')
    print(extra_uhe)


    
try:
    os.makedirs(os.path.join(MyPath, 'Dados', 'Hidro', 'Cascatas'))
except:
    pass

a = dfo.columns
# =============================================================================
# b_to_r = {}
# os.chdir('D:/Fabio/COPPE-PPE/Gesel/Hidro')
# for casc in cascatas:
#     df = pd.read_excel(os.path.join(os.getcwd(), 'Vazões_Diárias_1931_2016_PY.xlsx'), sheet_name=casc)
#     b_to_r[casc] = df.columns.tolist()[1:]
# =============================================================================
#%%

for casc in cascatas:

    startTime2 = dt.now()
    print('')
    print(casc)
    if casc not in os.listdir(os.path.join(MyPath, 'Dados','Hidro', 'Cascatas')):
        os.makedirs(os.path.join(MyPath, 'Dados','Hidro', 'Cascatas', casc))
        
    #df = pd.read_excel(os.path.join(os.getcwd(), 'Vazões_Diárias_1931_2016_PY_new.xlsx'), sheet_name=casc)

    df = dfo[['Data']+ CASC_UHE[casc]].copy()
    
    sd = int(df.Data.min().split('/')[-1])
    fd = int(df.Data.max().split('/')[-1])
    d1 = datetime.date(sd, 1, 1)
    d2 = datetime.date(fd, 12, 31)
    dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
    df['Data'] = dd
    df2 = df.iloc[:,1:]
    
    _31 = [n for n in range(len(df2.columns)) if isnotnan(df2.iloc[0,n])]
    
    #my_corrs = get_corrs(df2)
    corr_ = df2.corr()
    r2_corr = corr_.copy()
    r2_corr = r2_corr*r2_corr
    r2_corr_r = r2_corr.round(2)
    
    mask = np.zeros_like(r2_corr_r)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        plt.figure(figsize=(16,12))
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
#        plt.gcf().text(0.64, 0.8, 'Usinas em vermelho \n apresentam dados \n a partir de 1931', 
#               fontsize=10, color='red', bbox=props)
        ax = sns.heatmap(r2_corr_r, mask=mask, square=True, annot=True, cmap='Oranges')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right')
        plt.title('Correlação R² da Cascata/Bacia do Rio '+casc, fontsize=16, fontweight='bold')
#        for c in _31:
#            ax.get_xticklabels()[c].set_color("red")
#            ax.get_yticklabels()[c].set_color("red")
    
        #plt.tight_layout()
        plt.savefig(os.path.join(MyPath, 'Dados','Hidro', 'Cascatas', casc, casc+'_correlation_matrix.png'), dpi = 300)
    
# =============================================================================
#     import statsmodels.regression.linear_model as sm
#     model = sm.OLS(y, x, missing='drop')
#     results = model.fit()
# =============================================================================
    #results.summary()
    #new_x = df[x_c][(df[x_c].notna()) & (df[y_c].isna())]
    #ynewpred =  results.predict(new_x)
    ##nc = ynewpred.rename(y_c) 
    #df2.update(nc)
    
    # =============================================================================
    # xx = np.array(x).reshape((-1,1))
    # yy = np.array(y)
    # ols_sk = LinearRegression()
    # model_sk = ols_sk.fit(xx, yy)
    # coefofdet = model_sk.score(xx, yy)
    # y_predit = model.predict(xx)
    # =============================================================================

    if len(df.columns) >12:
        ncol1 = 3
    elif len(df.columns) < 12 and len(df.columns) >6:
        ncol1 = 2
    else:
        ncol1 = 1
    ax1 = df.plot(x='Data', figsize=(16,9))
    ax1.set_ylabel('Vazão (m³/s)')
    ax1.xaxis.set_minor_locator(mdates.YearLocator(1))
    #aax.grid(axis='x')
    plt.legend(ncol = ncol1)
    plt.grid(which='minor', linestyle='dotted')
    plt.title("Série de Vazões Históricas da Cascata/Bacia do Rio "+casc, fontsize=16, fontweight='bold')
    plt.savefig(os.path.join(MyPath, 'Dados','Hidro', 'Cascatas', casc, '01_'+casc+'_flow_series.png'), dpi = 300)
    
    for y_c in df.columns.tolist()[1:]:
        print(y_c)
        dfp = df[['Data', y_c]][~df[y_c].isnull()]
        aax = dfp.plot(x='Data', figsize=(16,9))
        aax.set_ylabel('Vazão (m³/s)')
        #aax.xaxis.set_minor_locator(MultipleLocator(1))
        aax.xaxis.set_minor_locator(mdates.YearLocator(1))
        #aax.grid(axis='x')
        plt.grid(which='minor', linestyle='dotted')
        #aax.tick_params(axis='x',which='minor',bottom=True)
        plt.title('Série de Vazões Históricas UHE '+y_c, fontsize=16, fontweight='bold')
        plt.savefig(os.path.join(MyPath, 'Dados','Hidro', 'Cascatas', casc, '0_'+y_c+'_flow_series.png'), dpi = 300)
        
        for x_c in df.columns.tolist()[1:]:
            x = df[x_c][(df[x_c]>0) & (~df[x_c].isnull())]
            #x = x[~((x-x.mean()).abs() > 5*x.std())] #removing outliers
            y = df[y_c][(df[y_c]>0) & (~df[y_c].isnull())] 
            #y = y[~((y-y.mean()).abs() > 5*y.std())] #removing outliers
            if len(x) > len(y):
                x = x.where(y>=0)
                x = x.dropna()
                y = y.where(x>=0)
                y = y.dropna()
                #linetrend
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                #regression
                slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
                r2 = r2_score(y, p(x))
                if r2>0.59 or r2 >= r2_corr_r[y_c].nlargest(2).min():
                    #print(x_c)
                    #plot
                    textstr = '\n'.join(('y = ax + b',
                        'a: '+str(np.round(slope,4)),
                        'b: '+str(np.round(intercept,4)),
                        'R²: '+str(np.round(r2,5))))
                    fig, ax = plt.subplots(figsize=(12,9))
                    plt.scatter(x, y)
                    plt.plot(x,p(x),"r--")
                    plt.xlabel('Vazão (m³/s) - '+x_c, fontsize=12)
                    plt.ylabel('Vazão (m³/s) - '+y_c, fontsize=12)
                    title = x_c+' _x_ '+y_c
                    if len(title) >40:
                        plt.title(x_c+' _x_ '+y_c, fontsize=16, fontweight='bold', wrap=True)
                    else:
                        plt.title(x_c+' _x_ '+y_c, fontsize=16, fontweight='bold')
                    # these are matplotlib.patch.Patch properties
                    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
                    # place a text box in upper left in axes coords
                    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                            verticalalignment='top', bbox=props)
                    fname = os.path.join(MyPath,'Dados','Hidro', 'Cascatas', casc,'correlation_'+x_c+'_'+y_c+'.png')
                    if os.path.isfile(fname):
                        os.remove(fname)   # Opt.: os.system("rm "+strFile)
                    plt.tight_layout()
                    plt.savefig(fname, dpi = 300)
                    plt.show(block=False)
                    time.sleep(2)
                    plt.close('all')

    Runtime = dt.now() - startTime2
    print('\n'+casc+' file completed in:')
    print(Runtime)
    
Runtime = dt.now() - startTime
print('\n file completed in:')
print(Runtime)

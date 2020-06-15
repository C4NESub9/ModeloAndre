import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%matplotlib inline 
# !pip install mpld3 - DONE !
#import mpld3
#mpld3.enable_notebook()

from scipy.integrate import odeint
# !pip install lmfit - DONE !
#import lmfit
#from lmfit.lineshapes import gaussian, lorentzian # do códi go original, mantida mas não usados

import datetime

import warnings
warnings.filterwarnings('ignore')
from pyswarm import pso
from numpy import linalg as LA

#import numdifftools # permite que lmfit calcule a matriz de correlações

#from lmfit import Model # classe lmfit para a criação do modelo de fitting

path = "D:/Projetos/googleData/data/"

pref = "ON"
suf  = "_An.csv"
Data_files_names = {
    "Alagoas"    : pref+"AiL"+suf ,
    "Bahia"      : pref+"BiA"+suf ,
    "Ceará"      : pref+"CiE"+suf ,
    "Maranhão"   : pref+"MiA"+suf ,
    "Paraíba"    : pref+"PiB"+suf ,
    "Pernambuco" : pref+"PiE"+suf ,
    "Piauí"      : pref+"PiI"+suf ,
    "RioGrdoN"   : pref+"RiN"+suf ,
    "Sergipe"    : pref+"SiE"+suf
}

data_ON_AL = pd.read_csv(path+Data_files_names["Alagoas"], sep =",")
data_ON_BA = pd.read_csv(path+Data_files_names["Bahia"], sep =",")
data_ON_CE = pd.read_csv(path+Data_files_names["Ceará"], sep =",")
data_ON_MA = pd.read_csv(path+Data_files_names["Maranhão"], sep =",")
data_ON_PB = pd.read_csv(path+Data_files_names["Paraíba"], sep =",")
data_ON_PE = pd.read_csv(path+Data_files_names["Pernambuco"], sep =",")
data_ON_PI = pd.read_csv(path+Data_files_names["Piauí"], sep =",")
data_ON_RN = pd.read_csv(path+Data_files_names["RioGrdoN"], sep =",")
data_ON_SE = pd.read_csv(path+Data_files_names["Sergipe"], sep =",")

format_str = "%Y-%m-%d"
data_ON_AL['Data'] = data_ON_AL['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_BA['Data'] = data_ON_BA['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_CE['Data'] = data_ON_CE['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_MA['Data'] = data_ON_MA['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_PB['Data'] = data_ON_PB['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_PE['Data'] = data_ON_PE['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_PI['Data'] = data_ON_PI['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_RN['Data'] = data_ON_RN['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))
data_ON_SE['Data'] = data_ON_SE['Data'].apply(lambda x:datetime.datetime.strptime(x,format_str))

data_ON_AL.set_index('Data')
data_ON_BA.set_index('Data')
data_ON_CE.set_index('Data')
data_ON_MA.set_index('Data')
data_ON_PB.set_index('Data')
data_ON_PE.set_index('Data')
data_ON_PI.set_index('Data')
data_ON_RN.set_index('Data')
data_ON_SE.set_index('Data')
data_ON_CE.info()

N_BR ={"Brasil": 210147125, 
    "Nordeste": 
        {'MA':7075181, 
        'PI':3273227, 
        'CE':9132078, 
        'RN':3506853, 
        'PB':4018127, 
        'PE':9557071, 
        'AL':3337357, 
        'SE':2298696, 
        'BA':14873064}, 
    "Norte": 
        {'RO':1777225, 
        'AC':881935, 
        'AM':4144597, 
        'RR': 605761, 
        'PA':8602865, 
        'AP':845731, 
        'TO':1572866}, 
    "Sudeste": 
        {'MG':21168791,
        'ES':4018650, 
        'RJ':17264943, 
        'SP':45919049}, 
    "Sul": 
        {'PR':11433957, 
        'SC':7164788, 
        'RS':11377239}, 
    "Centro-Oeste": 
        {'MS':2778986, 
        'MT':3484466, 
        'GO':7018354, 
        'DF':3015268} }

#
# VALORES MÉDIOS ASSUMIDOS:
#
num_of_incubation     = 9      # número de dias de incubação da doença (1/delta). 
num_of_infecting_days = 5      # número de dias que um infectado (ativo) infecta outros (= D = 1/gama)
num_to_dead           = 15     # número de dias para evoluir de infectado para óbito (1/rho) 
alpha                 = 5/1000 # taxa de letalidade (% dos infectados que vão a óbito)
Epi_days              = 600    # duração arbitrada da pandemia
#
# FREQUÊNCIAS CORRESPONDENTES
#
delta = 1/num_of_incubation
gamma = 1/num_of_infecting_days  
rho   = 1/num_to_dead
print('delta = ',delta,'gamma = ',gamma,'rho = ',rho)

def deriv(y, t, N, beta, gamma, delta, alpha, rho):
    #
    S, E, I, R, D = y
    #
    dSdt = -beta[int(t)] * S * I / N
    dEdt = beta[int(t)] * S * I / N - delta * E
    dIdt = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
    dRdt = (1 - alpha) * gamma * I
    dDdt = alpha * rho * I
    #
    return dSdt, dEdt, dIdt, dRdt, dDdt


N = N_BR['Nordeste']['CE']                 # <-- população do estado
y_data = data_ON_CE['ONCiE_An'].to_numpy() # <-- de pandas series para numpy array - ndarray 
x_data = np.arange(len(y_data))            # <-- do dia 1 ao final da série (Python inicia em 'zero', daí o +1)
days   = len(x_data)                       # <-- duração, até "hoje", da pandemia no estado, para o fitting dos parâmetros
t = np.arange(days)
y0 = N-1.0, 1.0, 0.0, 0.0, 0.0
h = 0.05
y = np.zeros(days)
for i in range(len(y_data)-1):
    y[i+1] = y[i]+h*(y_data[i]-y[i]) 

def seirdFunc(beta):
    ret = odeint(deriv, y0, t, args=(N, beta, gamma, delta, alpha, rho))
    S, E, I, R, D = ret.T
    
    value = LA.norm(D - y,2)
    return  value

#ret = seirdFunc(t)
xopt, fopt = pso(seirdFunc, 0.01*np.ones(len(t)), 3*np.ones(len(t)),swarmsize=200, omega=0.1, phip=0.7, phig=3.3, maxiter=1000, minstep=1e-4,
    minfunc=1e-8)

ret = odeint(deriv, y0, t, args=(N, xopt, gamma, delta, alpha, rho))
S, E, I, R, D = ret.T

R_0_over_time = [xopt[i]/gamma for i in range(len(t))]

plt.figure(figsize = [12, 5])
plt.xlim(10,102)
plt.ylim(0 ,200)
plt.plot(t, D,      label = 'Mortos', color='m')
plt.plot(t, y,      label = 'Mortos', color='black')
plt.bar (t, y_data, label = 'Dados de Óbitos')
plt.show()
'''
def logistic_R_0(t, R_0_start, k, x0, R_0_end):
    return (R_0_start-R_0_end) / (1 + np.exp(-k*(-t+x0))) + R_0_end

params_init_min_max = {"R_0_start": (3.0, 2.0, 6.0),
                       "k": (0.5, 0.01, 9.0), 
                       "x0": (30, 0, 250), 
                       "R_0_end": (0.9, 0.3, 3.5)}


def SolverEDOs(days, N, R_0_start, k, x0, R_0_end):
    #
    # definição da função beta(t) = R_0(t)*gama
    #
    def beta(t):
        return logistic_R_0(t, R_0_start, k, x0, R_0_end) * gamma
    #
    # Valores iniciais das variáveid do SEIRD: N-1 (população), 1 exposto, 0 infectado, recuperados ou mortos
    #
    y0 = N-1.0, 1.0, 0.0, 0.0, 0.0
    #
    # geração da grid temporal a partir da quantidade de dias informados
    #
    t = np.arange(days)
    #print(t)
    #
    # Integração do sistema de EDOs - o sistema é passado pela função 'deriv' na chamada do solver
    #
    ret = odeint(deriv, y0, t, args=(N, beta, gamma, delta, alpha, rho))
    #
    # Salvando os resultados nas variáveis do sistema
    #
    S, E, I, R, D = ret.T
    #
    # Cálculo de R_0(t)
    #
    R_0_over_time = [beta(i)/gamma for i in range(len(t))]
    #
    return t, S, E, I, R, D, R_0_over_time

N = N_BR['Nordeste']['CE']                 # <-- população do estado
y_data = data_ON_CE['ONCiE_An'].to_numpy() # <-- de pandas series para numpy array - ndarray 
x_data = np.arange(len(y_data))            # <-- do dia 1 ao final da série (Python inicia em 'zero', daí o +1)
days   = len(x_data)                       # <-- duração, até "hoje", da pandemia no estado, para o fitting dos parâmetros

def fitter(x, R_0_start, k, x0, R_0_end):
    ret = SolverEDOs(days, N, R_0_start, k, x0, R_0_end) # <-- chama a função solver das EDOs (que chama odeint para integrar)
    deaths_fitted = ret[5]                            # <-- óbitos: 6o elem. da tupla (t, S, E, I, R, D, R_0)
    return deaths_fitted[x]                           # <-- retorna vetor com as fatalidades no tempo 

# Cria o modelo de fitting passando a função fitter como parâmetro para lmfit 
#
mod = lmfit.Model(fitter)
#
# Criação do vetor de parâmetros para o fitting, incluindo 3 estimativas iniciais (inicial, min, max) p/cada parâmetro
#
for kwarg, (init, mini, maxi) in params_init_min_max.items(): # <-- usa as estimativas fornecidas acima
    mod.set_param_hint(str(kwarg), value=init, min=mini, max=maxi, vary=True)
#
# Criação do vetor de parâmetros para o otimizador
#
params = mod.make_params()

result = mod.fit(y_data, params, method="least_squares", x=x_data)

result.plot_fit(datafmt="-")

parametros = []
paramsfit = result.best_values
parametros.append(paramsfit['R_0_start'])
parametros.append(paramsfit['k'])
parametros.append(paramsfit['x0'])
parametros.append(paramsfit['R_0_end'])

#
print('\n','*** PARÂMETROS OTIMIZADOS DA CURVA LOGÍSTICA DE R_0 PELO FITTING COM OS DADOS DE ÓBITOS:','\n')
print('    R_0_start = {:.3f}'.format(paramsfit['R_0_start']))
print('    k         = {:.3f}'.format(paramsfit['k']))
print('    x_0       = {:.0f}'.format(paramsfit['x0']))
print('    R_0_end   = {:.3f}'.format(paramsfit['R_0_end']))

#
# Chamada do SOLVER com os parâmetros otimizados da curva logística para R_0(t)
#
Epi_days = 600
dados = SolverEDOs(Epi_days, N,*parametros)

plt.figure(figsize = [14, 6])
plt.title('Curvas SEIRD')
plt.xlim(20,120)
#plt.plot(dados[0],dados[1], label = 'Suscetíveis')
plt.plot(dados[0],dados[2], label = 'Infectados')
plt.plot(dados[0],dados[3], label = 'Expostos')
#plt.plot(dados[0],dados[4], label = 'Recuperados')
plt.plot(dados[0],dados[5], label = 'Óbitos')
plt.legend()
plt.show()

plt.figure(figsize = [10, 4])
plt.xlim(20,120)
plt.plot(dados[0],dados[5], label = 'Óbitos')
plt.title('Óbitos')

plt.figure(figsize = [12, 5])
plt.xlim(10,102)
plt. ylim(0,200)
plt.plot(dados[0],dados[5], label = 'Mortos', color='m')
plt.bar(x_data, y_data,     label = 'Dados de Óbitos')

plt.figure(figsize = [10, 4])
plt.xlim(30,60)
plt.title('R_0')
plt.plot(dados[0],dados[6], label = 'R_0')
'''
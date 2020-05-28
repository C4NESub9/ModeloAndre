import numpy as np
import pandas as pd
import csv

from bokeh.layouts import column, grid, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker
from bokeh.palettes import Spectral6

#pegar os ultimos valores de cada planilha e montar um painel com as informação
#poderia incluir também no painel a projeção de casos e óbitos para o dia seguinte

output_file('dashboard.html')
tools = 'pan'

def data2Num(shortMonth):
    return{
        'Data' : 0,
        'Saida_Estimada' : 1,
        'Saida': 2,
        'Erro' : 3
    }[shortMonth]

def readCSV(filename_src,column=data2Num('Saida_Estimada')):
    x = []
    importantDates = []
    y = []
  
    with open(filename_src, "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=";")
        axisName = []
        flag = True
        counter = 0
        for row in reader: 
            if flag:
                flag = False
                axisName = row[0].split(',')
                continue
            row = row[0].split(',')
            x.append(row[0])
            y.append(float(row[column])) 

            if counter%7 == 0:
                counter = 0
                importantDates.append(row[0])
            counter = counter + 1
    return [x,y,importantDates,axisName]

def plotConfiguration(x,y,title,ylabel):
    plot = figure(plot_height=320, x_axis_type='datetime', title=title)
    plot.line(x=x,y=y, line_width=3, line_alpha=0.6,line_color=Spectral6[0])
    plot.xaxis.major_label_orientation = 1.2
    plot.xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
    plot.yaxis.axis_label = yLabel
    plot.legend.location = "top_left"

    tick_vals = pd.to_datetime(CA[2]).astype(int) / 10**6
    #plot.xaxis.ticker = FixedTicker(ticks=list(tick_vals))
    temp = list(tick_vals)
    plot.xaxis.ticker = FixedTicker(ticks=temp)
    return plot

def Letalidade(filename_src,file,title,yLabel):
    
    OA = readCSV(filename_src+'OA'+file+'PNP.csv', data2Num('Saida'))
    CA = readCSV(filename_src+'CA'+file+'PNP.csv', data2Num('Saida'))

    x = pd.to_datetime(OA[0])
    y = [(i / j) *100 for i, j in zip(OA[1], CA[1])] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot
    
def Incidencia(filename_src,file, population, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+ file +'.csv', data2Num('Saida')) #Casos Novos tem q pegar da planilha

    x = pd.to_datetime(CN[0])
    y = [(i / population) *100.000 for i in CN[1]] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot

def PercentPopulContaminada(filename_src,file, population, title,yLabel):
    
    CA = readCSV(filename_src+'CA'+file+'PNP.csv', data2Num('Saida'))

    x = pd.to_datetime(CA[0])
    y = [(i / population) *100 for i in CA[1]] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot

def mortalidade(filename_src,file, population, title,yLabel):
    
    M = readCSV(filename_src+'M'+file+'.csv', data2Num('Saida')) #Mortalidade tem q pegar da planilha

    x = pd.to_datetime(M[0])
    y = [(i / population) *100.000 for i in M[1]] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot

 def CasosNovos(filename_src,file, population, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+file+'.csv', data2Num('Saida')) #Casos Novos tem q pegar da planilha

    x = pd.to_datetime(CN[0])
    y = [(i / population) *100.000 for i in CN[1]] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot

 def ObtosNovos(filename_src,file, population, title,yLabel):
    
    ON = readCSV(filename_src+'ON'+file+'.csv', data2Num('Saida')) #Óbitos Novos tem q pegar da planilha

    x = pd.to_datetime(ON[0])
    y = [(i / population) *100.000 for i in ON[1]] 
    plot = plotConfiguration(x,y,title,ylabel)
    return plot

def comparacoCenarios(filename_src,title,yLabel):
    
    A = readCSV(filename_src+'P.csv')
    B = readCSV(filename_src+'50P.csv')
    C = readCSV(filename_src+'75P.csv')
    D = readCSV(filename_src+'PNP.csv')

    x = pd.to_datetime(A[0])
    plot = figure(plot_height=320, x_axis_type='datetime', title=title)
    plot.line(x=x,y=A[1], line_width=3, line_alpha=0.6,legend_label='Projeção com Taxa de Isolamento Mantida no Último Valor',line_color=Spectral6[0])
    plot.line(x=x,y=B[1], line_width=3, line_alpha=0.6,legend_label='Projeção com Taxa de Isolamento em 50 por cento do valor Normal',line_color=Spectral6[1])
    plot.line(x=x,y=C[1], line_width=3, line_alpha=0.6,legend_label='Projeção com Taxa de Isolamento em 70 por cento do valor Normal',line_color=Spectral6[2])
    plot.line(x=x[0:len(D[1])],y=D[1], line_width=3, line_alpha=0.6,legend_label='Dados de Validação de 15 dias anteriores',line_color=Spectral6[3])
    plot.xaxis.major_label_orientation = 1.2
    plot.xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
    plot.yaxis.axis_label = yLabel
    plot.legend.location = "top_left"

    tick_vals = pd.to_datetime(A[2]).astype(int) / 10**6
    #plot.xaxis.ticker = FixedTicker(ticks=list(tick_vals))
    temp = list(tick_vals)
    plot.xaxis.ticker = FixedTicker(ticks=temp)
    return plot

stateListFileNordeste = ["AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"]
stateListNordeste = ['do Alagoas', 'da Bahia', 'do Ceará', 'do Maranhão', 'da Paraíba', 'de Pernambuco', 'do Piauí', 'do Rio Grande do Norte', 'de Sergipe']

stateListFileNorte = ["RiO_An","AiC_An","AiM_An","RiR_An","PiA_An","AiP_An","TiO_An"]
stateListNorte = ['de Rondônia', 'do Acre' , 'do Amazonas' , 'de Roraima', 'do Pará', 'do Amapá', 'do Tocantins']

stateListFileSuldeste = ["MiG_An","EiS_An","RiJ_An","SiP_An"]
stateListSuldeste = ['de Minas Gerais', 'do Espírito Santo', 'do Rio de Janeiro', 'de São Paulo' ]

stateListFileSul = ["PiR_An","SiC_An","RiS_An"]
stateListSul = ['do Paraná' , 'de Santa Catarina' , 'do Rio Grande do Sul' ]

stateListFileCentro = ["MiS_An","MiT_An","GiO_An"]
stateListCentro = ['do Mato Grosso do Sul' , 'do Mato Grosso' , 'de Goiás']

stateListFile = stateListFileNordeste + stateListFileNorte + stateListFileSuldeste + stateListFileSul + stateListFileCentro
stateList = stateListNordeste + stateListNorte + stateListSuldeste + stateListSul + stateListCentro

conjuntodePlots = list()

for i in zip(stateListFile,stateList): 
    CasosAcumulados  = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'CA'+i[0],"Casos Acumulados no estado " + i[1],"Casos Acumulados")
    ObitosAcumulados = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'OA'+i[0],"Óbitos Acumulados no estado " + i[1],"Óbitos Acumulados")
    letalidade = Letalidade('D:/Projetos/googleData/dataAn/',i[0],"Evolução da Letalidade no estado " + i[1],"Letalidade em porcentagens")
    conjuntodePlots.append(CasosAcumulados)
    conjuntodePlots.append(ObitosAcumulados)
    conjuntodePlots.append(letalidade)
    break

l = gridplot(conjuntodePlots, ncols=2, plot_width=650, plot_height=350)
show(l)



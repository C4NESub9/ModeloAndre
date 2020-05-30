import numpy as np
import pandas as pd
import csv
from unicodedata import normalize

from bokeh.layouts import column, grid, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select, Div, Paragraph, Span
from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker, HoverTool
from bokeh.palettes import Spectral6, Paired10
import webbrowser
# Variáveis Globais

Estado = 'Estado '

regioes = ['Norte','Nordeste','Sul','Suldeste','Centro-Oeste']

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


listOfRegions = [stateListNorte, stateListNordeste, stateListSul,stateListSuldeste,stateListCentro]
listOfRegionsFiles = [stateListFileNorte, stateListFileNordeste, stateListFileSul,stateListFileSuldeste,stateListFileCentro]

stateListFile = stateListFileNordeste + stateListFileNorte + stateListFileSuldeste + stateListFileSul + stateListFileCentro
stateList = stateListNordeste + stateListNorte + stateListSuldeste + stateListSul + stateListCentro

path2stateListFile = list()
for i in stateListFile:
    path2stateListFile.append(i+'.html') 

selecaoHTML = '<select id="16131" onchange="location = this.value;"><option value="">Selecione uma das Opções a Seguir</option><option value="'+ regioes[0]+'.html'+'">Estados do '+ regioes[0] +'</option><option value="'+ regioes[1]+'.html'+'">Estados do '+ regioes[1] +'</option><option value="'+ regioes[2]+'.html'+'">Estados do '+ regioes[2] +'</option><option value="'+ regioes[3]+'.html'+'">Estados do '+ regioes[3] +'</option><option value="'+ regioes[4]+'.html'+'">Estados do '+ regioes[4] +'</option><option value="'+ path2stateListFile[0]+'">Estado do Alagoas</option><option   value="'+ path2stateListFile[1]+'">Estado da Bahia</option><option   value="'+ path2stateListFile[2]+'">Estado do Ceará</option><option   value="'+ path2stateListFile[3]+'">Estado do Maranhão</option><option   value="'+ path2stateListFile[4]+'">Estado da Paraíba</option><option   value="'+ path2stateListFile[5]+'">Estado de Pernambuco</option><option   value="'+ path2stateListFile[6]+'">Estado do Piauí</option><option   value="'+ path2stateListFile[7]+'">Estado do Rio Grande do Norte</option><option   value="'+ path2stateListFile[8]+'">Estado de Sergipe</option><option   value="'+ path2stateListFile[9]+'">Estado de Rondônia</option><option   value="'+ path2stateListFile[10]+'">Estado do Acre</option><option   value="'+ path2stateListFile[11]+'">Estado do Amazonas</option><option   value="'+ path2stateListFile[12]+'">Estado de Roraima</option><option   value="'+ path2stateListFile[13]+'">Estado do Pará</option><option   value="'+ path2stateListFile[14]+'">Estado do Amapá</option><option   value="'+ path2stateListFile[15]+'">Estado do Tocantins</option><option   value="'+ path2stateListFile[16]+'">Estado de Minas Gerais</option><option   value="'+ path2stateListFile[17]+'">Estado do Espírito Santo</option><option   value="'+ path2stateListFile[18]+'">Estado do Rio de Janeiro</option><option   value="'+ path2stateListFile[19]+'">Estado de São Paulo</option><option   value="'+ path2stateListFile[20]+'">Estado do Paraná</option><option   value="'+ path2stateListFile[21]+'">Estado de Santa Catarina</option><option   value="'+ path2stateListFile[22]+'">Estado do Rio Grande do Sul</option><option   value="'+ path2stateListFile[23]+'">Estado do Mato Grosso do Sul</option><option   value="'+ path2stateListFile[24]+'">Estado do Mato Grosso</option><option   value="'+ path2stateListFile[25]+'">Estado de Goiás</option></select>'


municipioListBA = ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Itabuna', 'Juazeiro']
municipioListSE = ['Aracaju', 'Itabaiana', 'Estância', 'Lagarto']
municipioListAL = ['Maceió', 'Arapiraca','Murici', 'Coruripe', 'Palmeira dos Índios']
municipioListPE = ['Recife', 'Petrolina', 'Caruaru']
municipioListPB = ['João Pessoa', 'Campina Grande', 'Sousa', 'Patos']
municipioListRN = ['Natal', 'Mossoró']
municipioListCE = ['Fortaleza','Juazeiro do Norte', 'Sobral']
municipioListPI = ['Teresina','Picos','São Raimundo Nonato']
municipioListMA = ['São Luís', 'Imperatriz', 'Caxias']
municipiosFileList = ["BiASiliaioi","BiAFiiiaidiaitini","BiAVitiriaidioiqiiiti","BiAIiaiuiai","BiAJiaieiri","SiEAiaiaiui","SiEIiaiaiaiai","SiEEitiniii","SiELigirioi","AiLMiciii","AiLAiaiiiaiai","AiLMirici","AiLCiriripi","AiLPilieirioiniiisi","PiERicifi","PiEPitioiiiai","PiECiriaiui","PiBJiaieisiai","PiBCimiiiaiGiaidi","PiBSiuiai","PiBPitisi","RiNNitili","RiNMisioioi","CiEFiriaieiai","CiEJiaieirioiNiriei","CiESibiai","PiITirisini","MiASioiLiii","MiAIipiritiii","MiACixiai"]
municipiosList = [municipioListBA+municipioListSE+municipioListAL+municipioListPE+municipioListPB+municipioListRN+municipioListCE+['Teresina']+municipioListMA]
municipiosList = municipiosList[0]

selecaoMunicipiosHTML = '<select id="16131" onchange="location = this.value;"><option>Selecione uma das Opções a Seguir</option>'

for municipio in zip(municipiosList,municipiosFileList):
    selecaoMunicipiosHTML = selecaoMunicipiosHTML+'<option value="'+ municipio[1]+'.html'+'">Municipio: '+ municipio[0] +'</option>'

selecaoMunicipiosHTML = selecaoMunicipiosHTML+'</select>'

toPainel = dict()
predictionObservations = "As predições apresentadas são realizadas com base em um modelo ARX (Auto-Regressivo com entradas eXógenas) em que as entradas são os dados do google mobility (percentagem de pessoas nas residências) atrasados em 10 dias. É importante lembrar que os modelos ARX são mais adequados para predições de curta duração, e, quanto maior for o horizonte de predição, maior será o erro associado. Outro fator importante a ser considerado aqui é que todos os modelos apresentados foram obtidos automaticamente. Isto é, existe um algoritmo que captura os dados do ministério da saúde e de mobilidade, e realiza as predições de forma automática, sem a intervenção humana. Isto significa que, devido a particularidades dos estados quanto a coleta de informações e outros fatores, as predições podem não representar corretamente a evolução das variáveis. Por isso, essas informações devem ser analisadas com cuidado e de forma crítica."
####

#pegar os ultimos valores de cada planilha e montar um painel com as informação
#poderia incluir também no painel a projeção de casos e óbitos para o dia seguinte

tools = 'pan'

population ={
  "Brasil": 210147125,
  "Nordeste": {'MA':7075181, 'PI':3273227, 'CE':9132078, 'RN':3506853, 'PB':4018127, 'PE':9557071, 'AL':3337357, 'SE':2298696, 'BA':14873064}, 
  "Norte": {'RO':1777225, 'AC':881935, 'AM':4144597, 'RR': 605761, 'PA':8602865, 'AP':845731, 'TO':1572866}, 
  "Suldeste": {'MG':21168791,'ES':4018650, 'RJ':17264943, 'SP':45919049}, 
  "Sul": {'PR':11433957, 'SC':7164788, 'RS':11377239},
  "Centro-Oeste": {'MS':2778986, 'MT':3484466, 'GO':7018354, 'DF':3015268}
}

def statelist2Population(shortMonth):
    return{
#"AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"
        'AiL_An' : population['Nordeste']['AL'],
        'BiA_An' : population['Nordeste']['BA'],
        'CiE_An' : population['Nordeste']['CE'],
        'MiA_An' : population['Nordeste']['MA'],
        'PiB_An' : population['Nordeste']['PB'],
        'PiE_An' : population['Nordeste']['PE'],
        'PiI_An' : population['Nordeste']['PI'],
        'RiN_An' : population['Nordeste']['RN'],
        'SiE_An' : population['Nordeste']['SE'],
#"RiO_An","AiC_An","AiM_An","RiR_An","PiA_An","AiP_An","TiO_An"
        'RiO_An' : population['Norte']['RO'],
        'AiC_An' : population['Norte']['AC'],
        'AiM_An' : population['Norte']['AM'],
        'RiR_An' : population['Norte']['RR'],
        'PiA_An' : population['Norte']['PA'],
        'AiP_An' : population['Norte']['AP'],
        'TiO_An' : population['Norte']['TO'],
#"MiG_An","EiS_An","RiJ_An","SiP_An"       
        'MiG_An' : population['Suldeste']['MG'],
        'EiS_An' : population['Suldeste']['ES'],
        'RiJ_An' : population['Suldeste']['RJ'],
        'SiP_An' : population['Suldeste']['SP'],
#"PiR_An","SiC_An","RiS_An"
        'PiR_An' : population['Sul']['PR'],
        'SiC_An' : population['Sul']['SC'],
        'RiS_An' : population['Sul']['RS'],
#"MiS_An","MiT_An","GiO_An"
        'MiS_An' : population['Centro-Oeste']['MS'],
        'MiT_An' : population['Centro-Oeste']['MT'],
        'GiO_An' : population['Centro-Oeste']['GO']
    }[shortMonth]

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
        for row in reader: 
            #a = row[0].split(",")
            if len(row) < 2:
                reader = csv.reader(f,delimiter=",")
                break
        #if reader.line_num < 3: reader = csv.reader(f,delimiter=",")
        axisName = []
        flag = True
        counter = 0
        for row in reader: 
            if flag:
                flag = False
                axisName = row[0].split(',')
                continue
            if(row[column] == '+'):
                break
            #row = row[0].split(',')
            x.append(row[0])
            y.append(float(row[column])) 

            if counter%7 == 0:
                counter = 0
                importantDates.append(row[0])
            counter = counter + 1
    return [x,y,importantDates,axisName]

def plotConfiguration(x1,x,y,title,ylabel):
    plot = figure(plot_height=320, x_axis_type='datetime', title=title)
    plot.line(x=x,y=y, line_width=3, line_alpha=0.6,line_color=Spectral6[0])
    plot.xaxis.major_label_orientation = 1.2
    plot.xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
    plot.yaxis.axis_label = ylabel
    plot.legend.location = "top_left"

    tick_vals = pd.to_datetime(x1).astype(int) / 10**6
    #plot.xaxis.ticker = FixedTicker(ticks=list(tick_vals))
    temp = list(tick_vals)
    plot.xaxis.ticker = FixedTicker(ticks=temp)
    return plot

def getAllData(filename_src,file,population,filename_srcPredictions):
    #x = readCSV(filename_src+'OA'+file+'.csv')[0]
    GDM = readCSV(filename_src+'GDM'+file+'.csv')
    CAP = readCSV(filename_srcPredictions+'CA'+file+'P.csv')
    CAP50 = readCSV(filename_srcPredictions+'CA'+file+'50P.csv')
    CAP75 = readCSV(filename_srcPredictions+'CA'+file+'75P.csv')

    OAP = readCSV(filename_srcPredictions+'OA'+file+'P.csv')
    OAP50 = readCSV(filename_srcPredictions+'OA'+file+'50P.csv')
    OAP75 = readCSV(filename_srcPredictions+'OA'+file+'75P.csv')

    OA = readCSV(filename_src+'OA'+file+'.csv')
    CA = readCSV(filename_src+'CA'+file+'.csv')
    CN = readCSV(filename_src+'CN'+ file +'.csv')
    ON = readCSV(filename_src+'ON'+file+'.csv') 
    letalidade = [OA[0],[(i / j) *100 for i, j in zip(OA[1], CA[1])]] 
    incidencia = [CN[0],[(i / population) *100000 for i in CN[1] ]]
    popContaminada = [CA[0],[(i / population) *100 for i in CA[1]]]
    mortalidade = [ON[0],[(i / population) *100000 for i in ON[1] ]]
    taxaCrescimento = [CN[0],[(i /(1+j)) *100 for i, j in zip(CN[1], CA[1])] ]
    fatorCrescimento = [CN[0][0:len(CN)-1],[(i / (1+j)) *100 for i, j in zip(CN[1][1:len(CN[1])], CN[1][0:len(CN[1])-1])]]
    acumulatedData.setdefault(file,[]).append ([OA,CA,CN,ON,GDM,letalidade,incidencia,popContaminada,mortalidade,taxaCrescimento,fatorCrescimento,CAP,OAP,CAP50,OAP50,CAP75,OAP75]) 
    return acumulatedData

def Letalidade(filename_src,file,title,yLabel):
    
    OA = readCSV(filename_src+'OA'+file+'.csv')
    CA = readCSV(filename_src+'CA'+file+'.csv')

    toPainel.clear()
    toPainel.setdefault('ObitosAcumulados',[]).append (OA[1][-1]) 
    toPainel.setdefault('CasosAcumulados',[]).append (CA[1][-1]) 

    x = pd.to_datetime(OA[0])
    y = [(i / j) *100 for i, j in zip(OA[1], CA[1])] 

    toPainel.setdefault('Letalidade',[]).append (y[-1]) 

    x1 = OA[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot
    
def Incidencia(filename_src,file, population, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+ file +'.csv') #Casos Novos tem q pegar da planilha
    toPainel.setdefault('CasosNovos',[]).append (CN[1][-1]) 

    x = pd.to_datetime(CN[0])
    y = [(i / population) *100000 for i in CN[1]] 

    toPainel.setdefault('Incidencia',[]).append (y[-1]) 

    x1 = CN[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def PercentPopulContaminada(filename_src,file, population, title,yLabel):
    
    CA = readCSV(filename_src+'CA'+file+'.csv')

    x = pd.to_datetime(CA[0])
    y = [(i / population) *100 for i in CA[1]] 

    toPainel.setdefault('PercentualContaminado',[]).append (y[-1]) 

    x1 = CA[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def Mortalidade(filename_src,file, population, title,yLabel):
    
    ON = readCSV(filename_src+'ON'+file+'.csv') #Mortalidade tem q pegar da planilha
    toPainel.setdefault('ObitosNovos',[]).append (ON[1][-1]) 

    x = pd.to_datetime(ON[0])
    y = [(i / population) *100000 for i in ON[1]] 

    toPainel.setdefault('Mortalidade',[]).append (y[-1]) 

    x1 = ON[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def CasosNovos(filename_src,file, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+file+'.csv') #Casos Novos tem q pegar da planilha

    x = pd.to_datetime(CN[0])
    y = CN[1]
    x1 = CN[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def ObtosNovos(filename_src,file, title,yLabel):
    
    ON = readCSV(filename_src+'ON'+file+'.csv') #Óbitos Novos tem q pegar da planilha

    x = pd.to_datetime(ON[0])
    y = ON[1]
    x1 = ON[2]  
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def Mobilidade(filename_src,file, title,yLabel):
    
    GDM = readCSV(filename_src+'GDM'+file+'.csv') #Casos Novos tem q pegar da planilha

    x = pd.to_datetime(GDM[0])
    y = GDM[1] 
    x1 = GDM[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def CasosAcumulados(filename_src,file, title,yLabel):
    
    CA = readCSV(filename_src+'CA'+file+'.csv') #Casos Novos tem q pegar da planilha

    x = pd.to_datetime(CA[0])
    y = CA[1] 
    x1 = CA[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def ObitosAcumulados(filename_src,file, title,yLabel):
    
    OA = readCSV(filename_src+'OA'+file+'.csv') #Óbitos Novos tem q pegar da planilha

    x = pd.to_datetime(OA[0])
    y = OA[1]
    x1 = OA[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def TaxadeCrescimento(filename_src,file, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+file+'.csv')
    CA = readCSV(filename_src+'CA'+file+'.csv')

    x = pd.to_datetime(CA[0])
    y = [(i /(1+j)) *100 for i, j in zip(CN[1], CA[1])] 

    toPainel.setdefault('TaxadeCrescimento',[]).append (y[-1]) 

    x1 = CA[2]
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def FatordeCrescimento(filename_src,file, title,yLabel):
    
    CN = readCSV(filename_src+'CN'+file+'.csv') #Óbitos Novos tem q pegar da planilha

    x = pd.to_datetime(CN[0][0:len(CN[1])-1])
    y = [(i / (1+j)) *100 for i, j in zip(CN[1][1:len(CN[1])], CN[1][0:len(CN[1])-1])] 
    x1 = CN[2]

    toPainel.setdefault('FatordeCrescimento',[]).append (y[-1]) 
    
    plot = plotConfiguration(x1,x,y,title,yLabel)
    plot.circle(x, y, fill_color="white", size=2)
    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)
    return plot

def comparacoCenarios(filename_src,title,yLabel):
    
    
    A = readCSV(filename_src+'P.csv')
    B = readCSV(filename_src+'50P.csv')
    C = readCSV(filename_src+'75P.csv')
    D = readCSV(filename_src+'60P.csv')
    #D = readCSV(filename_src+'PNP.csv')

    x = pd.to_datetime(A[0])
    plot = figure(plot_height=320, x_axis_type='datetime', title=title)
    plot.line(x=x,y=A[1], line_width=2, line_alpha=0.6,legend_label='Mantida no Último Valor',line_color=Spectral6[0])
    plot.circle(x, A[1], fill_color = Spectral6[0], size=2)
    plot.line(x=x,y=B[1], line_width=2, line_alpha=0.6,legend_label='50% do valor Normal',line_color=Spectral6[0],line_dash="4 4")
    #plot.circle(x, B[1], fill_color=Spectral6[1], size=2)
    plot.line(x=x,y=C[1], line_width=1.5, line_alpha=0.6,legend_label='70% do valor Normal',line_color=Spectral6[0],line_dash="4 4")

    plot.line(x=x,y=D[1], line_width=1.5, line_alpha=0.6,legend_label='60% do valor Normal',line_color=Paired10[4])
    #plot.circle(x, C[1], fill_color=Spectral6[2], size=2)
    #plot.line(x=x[0:len(D[1])],y=D[1], line_width=3, line_alpha=0.6,legend_label='Dados de Validação de 15 dias anteriores',line_color=Spectral6[3])
    Prediction = Span(location=x[-16],dimension='height', line_color='black',line_dash='dashed', line_width=0.5)
    plot.add_layout(Prediction)
    #Prediction = Span(location=x[-21],dimension='height', line_color='black',line_dash='dashed', line_width=0.5)
    #plot.add_layout(Prediction)
    
    plot.xaxis.major_label_orientation = 1.2
    plot.xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
    plot.yaxis.axis_label = yLabel
    plot.legend.location = "top_left"

    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)

    tick_vals = pd.to_datetime(A[2]).astype(int) / 10**6
    #plot.xaxis.ticker = FixedTicker(ticks=list(tick_vals))
    temp = list(tick_vals)
    plot.xaxis.ticker = FixedTicker(ticks=temp)
    return plot 

def geracaoPorEstado(region,stateListFile,stateList,data,Titulos,yLabel):
    output_file('./dashboard/'+ region + '.html')
    plot = list()

    for i in range(len(Titulos)):
        plot.append(figure(plot_height=320, x_axis_type='datetime', title=Titulos[i]+region))
        plot[i].xaxis.major_label_orientation = 1.2
        plot[i].xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
        plot[i].yaxis.axis_label = yLabel[i]
        hovertool = HoverTool(tooltips=[("Serie","$name"),("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
        plot[i].add_tools(hovertool)
            
    countState = 0
    for i in zip(stateListFile,stateList):
        stateTemp = i[1].split(' ')[1:]
        state = ''
        for j in stateTemp:
            state = state + ' ' + j

        dataTemp = data[i[0]][0]
        #flag = True
        counter = 0
        for j in dataTemp:
            #if flag: flag = False; continue
            y = j[1]
            x = pd.to_datetime(j[0])
            plot[counter].circle(x, y, fill_color="white", size=0.5)
            plot[counter].line(x,y, line_width=1+counter/10, line_alpha=0.6, line_color = Paired10[countState], legend_label=state,name=state)
            #função inacabada
            plot[counter].legend.location = "top_left"
            counter = counter + 1
        countState = countState + 1

    select = Div(text=selecaoHTML)
    selectmunicipio = Div(text=selecaoMunicipiosHTML)
    l=grid([[select, selectmunicipio],[plot[0], plot[1]],[plot[2], plot[3]],[plot[4], plot[5]],[plot[6], plot[7]],[plot[8], plot[9]],[Paragraph(text= predictionObservations)],[plot[10], plot[11]],[plot[12], plot[13]],[plot[14], plot[15]]])
    show(l)



acumulatedData = dict()
conjuntodePlots = list()
for i in zip(stateListFile,stateList): 
    
    output_file('./dashboard/'+ i[0] + '.html')
    
    select = Div(text=selecaoHTML)
    selectmunicipio = Div(text=selecaoMunicipiosHTML)

    casosAcumuladosComp     = comparacoCenarios('D:/Projetos/ModeloAndre/dataAn/'+'CA'+i[0],"Casos Acumulados no Estado " + i[1] + '(Projeção com Taxa de Isolamento)',"Casos Acumulados")
    obitosAcumuladosComp    = comparacoCenarios('D:/Projetos/ModeloAndre/dataAn/'+'OA'+i[0],"Óbitos Acumulados no Estado " + i[1] + '(Projeção com Taxa de Isolamento)',"Óbitos Acumulados")
    letalidade              = Letalidade('D:/Projetos/ModeloAndre/data/',i[0],"Evolução da Letalidade no estado " + i[1],"Letalidade em porcentagens")
    incidencia              = Incidencia('D:/Projetos/ModeloAndre/data/',i[0], statelist2Population(i[0]), 'Evolução da Incidência no Estado ' + i[1], 'Incidência')
    percentPopulContaminada = PercentPopulContaminada('D:/Projetos/ModeloAndre/data/',i[0], statelist2Population(i[0]), 'Evolução da Percentual da População Contaminada no Estado ' + i[1], 'População Contaminada')
    mortalidade             = Mortalidade('D:/Projetos/ModeloAndre/data/',i[0], statelist2Population(i[0]), 'Evolução da Mortalidade no Estado ' + i[1],'Mortalidade')
    casosNovos              = CasosNovos('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Casos Novos no Estado ' + i[1], 'Casos Novos')
    obtosNovos              = ObtosNovos('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Óbitos Novos no Estado ' + i[1], 'Óbitos Novos')
    casosAcumulados         = CasosAcumulados('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Casos Acumulados no Estado ' + i[1], 'Casos Acumulados')
    obtosAcumulados         = ObitosAcumulados('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Óbitos Acumulados no Estado ' + i[1], 'Óbitos Acumulados')
    taxadeCrescimento       = TaxadeCrescimento('D:/Projetos/ModeloAndre/data/',i[0],"Evolução da Taxa de Crescimento no estado " + i[1], 'Taxa de Crescimento')
    fatordeCrescimento      = FatordeCrescimento('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução do Fator de Crescimento no Estado ' + i[1], 'Fator de Crescimetno')
    mobilidade              = Mobilidade('D:/Projetos/ModeloAndre/data/',i[0], "Tendência de mobilidade para Espaços Residenciais (0 Representa a Média) no Estado ",'Mobilidade Residencial')
    acumulatedData[i[0]]    = getAllData('D:/Projetos/ModeloAndre/data/',i[0],statelist2Population(i[0]),'D:/Projetos/ModeloAndre/dataAn/')[i[0]]
    
    paragraph1 = Paragraph(text="Casos Acumulados = " + "{:.{}f}".format(toPainel['CasosAcumulados'][0],4))
    paragraph2 = Paragraph(text="Casos Novos = " +"{:.{}f}".format(toPainel['CasosNovos'][0],4))
    paragraph3 = Paragraph(text="Incidência = " + "{:.{}f}".format(toPainel['Incidencia'][0],4))
    paragraph4 = Paragraph(text="Letalidade = " + "{:.{}f}".format(toPainel['Letalidade'][0],4) + '%')
    paragraph5 = Paragraph(text="Mortalidade = " + "{:.{}f}".format(toPainel['Mortalidade'][0],4))
    paragraph6 = Paragraph(text="Óbitos Acumulados = " + "{:.{}f}".format(toPainel['ObitosAcumulados'][0],4))
    paragraph7 = Paragraph(text="Óbitos Novos = " + "{:.{}f}".format(toPainel['ObitosNovos'][0],4))
    paragraph8 = Paragraph(text="Pessoas Contaminadas = " + "{:.{}f}".format(toPainel['PercentualContaminado'][0],4) + '%')
    paragraph9 = Paragraph(text="Taxa de Crescimento = " + "{:.{}f}".format(toPainel['TaxadeCrescimento'][0],4))
    paragraph10 = Paragraph(text="Fator de Crescimetno = " + "{:.{}f}".format(toPainel['FatordeCrescimento'][0],4))
    paragraphOBS = Paragraph(text= predictionObservations)
    l=grid([
    [select,selectmunicipio],
    [paragraph1,paragraph2,paragraph3,paragraph4,paragraph5],
    [paragraph6,paragraph7,paragraph8,paragraph9,paragraph10],
    [casosAcumuladosComp, obitosAcumuladosComp],
    [paragraphOBS],
    [casosAcumulados, obtosAcumulados],
    [casosNovos, obtosNovos],
    [letalidade, incidencia],
    [percentPopulContaminada,mortalidade],
    [taxadeCrescimento,fatordeCrescimento]
    ])
    #break
    show(l) 

Titulos = [ #OA,CA,CN,ON,letalidade,incidencia,popContaminada,mortalidade,taxaCrescimento,fatorCrescimento,CAP,OAP
    "Evolução de Óbitos Acumulados nos Estados do ",
    "Evolução de Casos Acumulados nos Estados do ",
    'Evolução de Casos Novos nos Estados do ',
    'Evolução de Óbitos Novos nos Estados do ',
    "Tendência de mobilidade para Espaços Residenciais (0 Representa a Média) nos Estados",
    "Evolução da Letalidade nos Estados do ",
    'Evolução da Incidência nos Estados do ',
    'Evolução da Percentual da População Contaminada nos Estados do ',
    'Evolução da Mortalidade nos Estados do ',
    "Evolução da Taxa de Crescimento nos Estados do",
    'Evolução do Fator de Crescimento nos Estados do',
    "Predição de Casos Acumulados nos Estados do ",
    "Predição de Óbitos Acumulados nos Estados do ",
    "Predição com 50% de intervenção de Casos Acumulados nos Estados do ",
    "Predição com 50% de intervenção de Óbitos Acumulados nos Estados do ",
    "Predição com 75% de intervenção de Casos Acumulados nos Estados do ",
    "Predição com 75% de intervenção de Óbitos Acumulados nos Estados do ",
]

yLabel = [
    "Óbitos Acumulados",
    "Casos Acumulados",
    'Casos Novos',
    'Óbitos Novos',
    'Mobilidade Residencial',
    "Letalidade",
    'Incidência',
    'População Contaminada',
    'Mortalidade',
    "Taxa de Crescimento",
    'Fator de Crescimento',
    "Óbitos Acumulados",
    "Casos Acumulados",
    "Óbitos Acumulados",
    "Casos Acumulados",
    "Óbitos Acumulados",
    "Casos Acumulados"
]

for i in zip(regioes,listOfRegionsFiles,listOfRegions):
    geracaoPorEstado(i[0],i[1],i[2],acumulatedData,Titulos,yLabel)


#municipios
acumulatedData = dict()
conjuntodePlots = list()
for i in zip(municipiosFileList,municipiosList): 
    
    output_file('./dashboard/'+ i[0] + '.html')
    
    select = Div(text=selecaoHTML)
    selectmunicipio = Div(text=selecaoMunicipiosHTML)

    casosAcumuladosComp     = comparacoCenarios('D:/Projetos/ModeloAndre/dataAn/'+'CA'+i[0],"Casos Acumulados no Municipio: " + i[1] + '(Projeção com Taxa de Isolamento)',"Casos Acumulados")
    obitosAcumuladosComp    = comparacoCenarios('D:/Projetos/ModeloAndre/dataAn/'+'OA'+i[0],"Óbitos Acumulados no Municipio: " + i[1] + '(Projeção com Taxa de Isolamento)',"Óbitos Acumulados")
    #casosNovos              = CasosNovos('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Casos Novos no Municipio:  ' + i[1], 'Casos Novos')
    #obtosNovos              = ObtosNovos('D:/Projetos/ModeloAndre/data/',i[0], 'Evolução de Óbitos Novos no Municipio:  ' + i[1], 'Óbitos Novos')
    #casosAcumulados         = CasosAcumulados('D:/Projetos/googleData/data/',i[0], 'Evolução de Casos Acumulados no Municipio:  ' + i[1], 'Casos Acumulados')
    #obtosAcumulados         = ObitosAcumulados('D:/Projetos/googleData/data/',i[0], 'Evolução de Óbitos Acumulados no Municipio:  ' + i[1], 'Óbitos Acumulados')
    
    #paragraph1 = Paragraph(text="Casos Acumulados = " + "{:.{}f}".format(toPainel['CasosAcumulados'][0],4))
    #paragraph2 = Paragraph(text="Casos Novos = " +"{:.{}f}".format(toPainel['CasosNovos'][0],4))
    #paragraph6 = Paragraph(text="Óbitos Acumulados = " + "{:.{}f}".format(toPainel['ObitosAcumulados'][0],4))
   # paragraph7 = Paragraph(text="Óbitos Novos = " + "{:.{}f}".format(toPainel['ObitosNovos'][0],4))
    paragraphOBS = Paragraph(text= predictionObservations)
    l=grid([
    [select,selectmunicipio],
    #[paragraph1,paragraph2,paragraph6,paragraph7],
    [casosAcumuladosComp, obitosAcumuladosComp],
    [paragraphOBS],
    #[casosNovos, obtosNovos]
    ])
    #break
    show(l)
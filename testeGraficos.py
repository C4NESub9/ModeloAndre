import numpy as np
import pandas as pd
import csv
from unicodedata import normalize
from unidecode import unidecode
import datetime
from datetime import timedelta 
import time 

from bokeh.layouts import column, grid, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select, Div, Paragraph, Span
from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker, HoverTool
from bokeh.palettes import Spectral6, Paired10
import webbrowser
# Variáveis Globais
RegioesSaude = ["NERNRSCA24004", "NERNRSCA24008", "NERNRSCA24003", "NERNRSCA24006", "NERNRSCA24002", "NERNRSCA24001", "NERNRSCA24005", "NERNRSCA24007","NERNRSOA24004", "NERNRSOA24008", "NERNRSOA24003", "NERNRSOA24006", "NERNRSOA24002", "NERNRSOA24001", "NERNRSOA24005", "NERNRSOA24007","NEPBRSCA25011", "NEPBRSCA25007", "NEPBRSCA25003", "NEPBRSCA25002", "NEPBRSCA25015", "NEPBRSCA25001", "NEPBRSCA25009", "NEPBRSCA25005", "NEPBRSCA25010", "NEPBRSCA25006", "NEPBRSCA25016", "NEPBRSCA25014", "NEPBRSCA25004", "NEPBRSCA25008", "NEPBRSCA25013", "NEPBRSCA25012", "NEPBRSOA25007", "NEPBRSOA25003", "NEPBRSOA25002", "NEPBRSOA25015", "NEPBRSOA25001", "NEPBRSOA25009", "NEPBRSOA25005", "NEPBRSOA25010", "NEPBRSOA25006", "NEPBRSOA25016", "NEPBRSOA25014", "NEPBRSOA25008", "NEPBRSOA25012","NEBARSCA29023", "NEBARSCA29017", "NEBARSCA29001", "NEBARSCA29019", "NEBARSCA29025", "NEBARSCA29015", "NEBARSCA29026", "NEBARSCA29012", "NEBARSCA29022", "NEBARSCA29006", "NEBARSCA29010", "NEBARSCA29028", "NEBARSCA29011", "NEBARSCA29003", "NEBARSCA29009", "NEBARSCA29002", "NEBARSCA29008", "NEBARSCA29018", "NEBARSCA29021", "NEBARSCA29005", "NEBARSCA29007", "NEBARSCA29014", "NEBARSCA29027", "NEBARSCA29004", "NEBARSCA29016", "NEBARSCA29024", "NEBARSCA29020", "NEBARSCA29013","NEBARSOA29023",  "NEBARSOA29001", "NEBARSOA29019", "NEBARSOA29025", "NEBARSOA29015", "NEBARSOA29026", "NEBARSOA29012", "NEBARSOA29022", "NEBARSOA29006", "NEBARSOA29010", "NEBARSOA29028", "NEBARSOA29011", "NEBARSOA29003", "NEBARSOA29009", "NEBARSOA29002",  "NEBARSOA29018", "NEBARSOA29005", "NEBARSOA29014", "NEBARSOA29027", "NEBARSOA29004", "NEBARSOA29016", "NEBARSOA29024", "NEBARSOA29020", "NEBARSOA29013","NESERSCA28007", "NESERSCA28001", "NESERSCA28002", "NESERSCA28003", "NESERSCA28005", "NESERSCA28006", "NESERSCA28004","NESERSOA28007", "NESERSOA28001", "NESERSOA28002", "NESERSOA28003", "NESERSOA28005", "NESERSOA28006", "NESERSOA28004","NEALRSCA27010", "NEALRSCA27005", "NEALRSCA27007", "NEALRSCA27004", "NEALRSCA27001", "NEALRSCA27008", "NEALRSCA27003", "NEALRSCA27009", "NEALRSCA27006", "NEALRSCA27002","NEALRSOA27010", "NEALRSOA27005", "NEALRSOA27007", "NEALRSOA27004", "NEALRSOA27001", "NEALRSOA27008", "NEALRSOA27003", "NEALRSOA27009", "NEALRSOA27006", "NEALRSOA27002","NEMARSCA21001", "NEMARSCA21005", "NEMARSCA21006", "NEMARSCA21016", "NEMARSCA21002", "NEMARSCA21007", "NEMARSCA21014", "NEMARSCA21003", "NEMARSCA21019", "NEMARSCA21008", "NEMARSCA21009", "NEMARSCA21011", "NEMARSCA21004", "NEMARSCA21013", "NEMARSCA21018", "NEMARSCA21015", "NEMARSCA21010", "NEMARSCA21012", "NEMARSCA21017","NEMARSOA21001", "NEMARSOA21005", "NEMARSOA21006", "NEMARSOA21016", "NEMARSOA21002", "NEMARSOA21007", "NEMARSOA21014", "NEMARSOA21003", "NEMARSOA21019", "NEMARSOA21008", "NEMARSOA21009", "NEMARSOA21011", "NEMARSOA21004", "NEMARSOA21013", "NEMARSOA21018", "NEMARSOA21015", "NEMARSOA21010", "NEMARSOA21012", "NEMARSOA21017","NEPERSCA26010", "NEPERSCA26001", "NEPERSCA26009", "NEPERSCA26003", "NEPERSCA26008", "NEPERSCA26004", "NEPERSCA26005", "NEPERSCA26007", "NEPERSCA26002", "NEPERSCA26011", "NEPERSCA26012", "NEPERSCA26006","NEPERSOA26010", "NEPERSOA26001", "NEPERSOA26009", "NEPERSOA26003", "NEPERSOA26008", "NEPERSOA26004", "NEPERSOA26005", "NEPERSOA26007", "NEPERSOA26002", "NEPERSOA26011", "NEPERSOA26012", "NEPERSOA26006","NECERSCA23019", "NECERSCA23003", "NECERSCA23012", "NECERSCA23018", "NECERSCA23014", "NECERSCA23011", "NECERSCA23020", "NECERSCA23010", "NECERSCA23006", "NECERSCA23002", "NECERSCA23001", "NECERSCA23007", "NECERSCA23004", "NECERSCA23015", "NECERSCA23017", "NECERSCA23008", "NECERSCA23021", "NECERSCA23016", "NECERSCA23022", "NECERSCA23005", "NECERSCA23013", "NECERSCA23009","NECERSOA23019", "NECERSOA23003", "NECERSOA23012", "NECERSOA23018", "NECERSOA23014", "NECERSOA23011", "NECERSOA23020", "NECERSOA23010", "NECERSOA23006", "NECERSOA23002", "NECERSOA23001", "NECERSOA23007", "NECERSOA23004", "NECERSOA23015", "NECERSOA23017", "NECERSOA23008", "NECERSOA23021", "NECERSOA23016", "NECERSOA23022", "NECERSOA23005", "NECERSOA23013", "NECERSOA23009","NEPIRSCA22004", "NEPIRSCA22009", "NEPIRSCA22002", "NEPIRSCA22006", "NEPIRSCA22010", "NEPIRSCA22007", "NEPIRSCA22003", "NEPIRSCA22008", "NEPIRSCA22011", "NEPIRSCA22001", "NEPIRSCA22005","NEPIRSOA22004", "NEPIRSOA22009", "NEPIRSOA22002", "NEPIRSOA22006", "NEPIRSOA22010", "NEPIRSOA22007", "NEPIRSOA22003",  "NEPIRSOA22011", "NEPIRSOA22001", "NEPIRSOA22005"]
selecaoRegiaoHTML = '<select onchange="location = this.value;"><option>Selecione uma das Opções a Seguir</option>'

for regiao in RegioesSaude:
        selecaoRegiaoHTML = selecaoRegiaoHTML+'<option value="'+ regiao + '.html'+'">Regiao de Saúde: '+ regiao +'</option>'

selecaoRegiaoHTML = selecaoRegiaoHTML+'</select>'

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

stateListNordesteAbrev = ['BA','SE','AL','PE','PB','RN','CE','PI','MA']
municipioListBA = ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Itabuna', 'Juazeiro']
municipioListSE = ['Aracaju', 'Itabaiana', 'Estância', 'Lagarto']
municipioListAL = ['Maceió', 'Arapiraca','Murici', 'Coruripe', 'Palmeira dos Índios']
municipioListPE = ['Recife', 'Petrolina', 'Caruaru']
municipioListPB = ['João Pessoa', 'Campina Grande', 'Sousa', 'Patos']
municipioListRN = ['Natal', 'Mossoró']
municipioListCE = ['Fortaleza','Juazeiro do Norte', 'Sobral']
municipioListPI = ['Teresina','Picos','São Raimundo Nonato']
municipioListMA = ['São Luís', 'Imperatriz', 'Caxias']
municipiosFileList = [["BiASiliaioi","BiAFiiiaidiaitini","BiAVitiriaidioiqiiiti","BiAIiaiuiai","BiAJiaieiri"],["SiEAiaiaiui","SiEIiaiaiaiai","SiEEitiniii","SiELigirioi"],["AiLMiciii","AiLAiaiiiaiai","AiLMirici","AiLCiriripi","AiLPilieirioiniiisi"],["PiERicifi","PiEPitioiiiai","PiECiriaiui"],["PiBJiaieisiai","PiBCimiiiaiGiaidi","PiBSiuiai","PiBPitisi"],["RiNNitili","RiNMisioioi"],["CiEFiriaieiai","CiEJiaieirioiNiriei","CiESibiai"],["PiITirisini"],["MiASioiLiii","MiAIipiritiii","MiACixiai"]]
municipiosList = [municipioListBA,municipioListSE,municipioListAL,municipioListPE,municipioListPB,municipioListRN,municipioListCE,['Teresina'],municipioListMA]
#municipiosList = municipiosList[0]

selecaoMunicipiosHTML = '<select onchange="location = this.value;"><option>Selecione uma das Opções a Seguir</option>'

for estado in zip(municipiosList,municipiosFileList):
    for municipio in zip(estado[0],estado[1]):
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

def getAlbertoData(filename_src):
    Dict_data = dict()
    with open(filename_src, "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")

        flag = True
        for row in reader: 
            if flag:
                flag = False
                continue
            Dict_data.setdefault(unidecode(row[0]),[]).append ([ row[1],row[2],row[3] ]) 
    return Dict_data

def plotAlberto(plot,data,local):
    data = data.get(unidecode(local), "empty")
    if data == 'empty':
        return
    time = list()
    y = list()
    value = 0
    counter = 0
    importantDates = list()
    timeTemp = ''
    for row in data:
        timeTemp = datetime.datetime.strptime(row[0], '%d/%m/%Y').strftime('20%y-%m-%d')
        time.append(timeTemp)
        if row[2] == '':
            value = 0
        else:
            value = float(row[2])
        y.append(value)
        if counter%7 == 0:
            counter = 0
            importantDates.append(row[0])
        counter = counter + 1
    x = pd.to_datetime(time)
    plot.line(x,y, line_width=1.5, line_alpha=0.6,legend_label='Projeções Modelo 2',line_color=Spectral6[1],line_dash="4 4")
    tick_vals = pd.to_datetime(importantDates).astype(int) / 10**6
    #plot.xaxis.ticker = FixedTicker(ticks=list(tick_vals))
    temp = list(tick_vals)
    plot.xaxis.ticker = FixedTicker(ticks=temp)
    return plot

def plotMarcus(plot,data,local,delay=0):
    data = data.get(unidecode(local), "empty")
    if data == 'empty':
        return
    timeList = list()
    y = list()
    importantDates = list()
    timeTemp = ''
    acumulated = 0
    for row in zip(data,range(len(data)-1)):
        format = '%Y-%m-%d'
        timeTemp = datetime.datetime.strptime(row[0][0],format)+ timedelta(days=delay)
        timeTemp = timeTemp.strftime(format)
        timeTemp = timeList.append(timeTemp)
        if row[0][1] == '':
            value = 0
        else:
            acumulated = acumulated+float(row[0][1])
        y.append(acumulated)
        if row[1]%7 == 0:
            importantDates.append(row[0][0])
                
    x = pd.to_datetime(timeList)
    plot.line(x,y, line_width=2.5, line_alpha=0.6,legend_label='Projeções Modelo 3',line_color=Spectral6[2],line_dash="4 4")
    tick_vals = pd.to_datetime(importantDates).astype(int) / 10**6
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
    CAP60 = readCSV(filename_srcPredictions+'CA'+file+'60P.csv')

    OAP = readCSV(filename_srcPredictions+'OA'+file+'P.csv')
    OAP50 = readCSV(filename_srcPredictions+'OA'+file+'50P.csv')
    OAP75 = readCSV(filename_srcPredictions+'OA'+file+'75P.csv')
    OAP60 = readCSV(filename_srcPredictions+'OA'+file+'60P.csv')

    OA = readCSV(filename_src+'OA'+file+'.csv')
    CA = readCSV(filename_src+'CA'+file+'.csv')
    CN = readCSV(filename_src+'CN'+ file +'.csv')
    ON = readCSV(filename_src+'ON'+file+'.csv') 
    letalidade = [OA[0],[(i / (1+j)) *100 for i, j in zip(OA[1], CA[1])]] 
    incidencia = [CN[0],[(i / population) *100000 for i in CN[1] ]]
    popContaminada = [CA[0],[(i / population) *100 for i in CA[1]]]
    mortalidade = [ON[0],[(i / population) *100000 for i in ON[1] ]]
    taxaCrescimento = [CN[0],[(i /(1+j)) *100 for i, j in zip(CN[1], CA[1])] ]
    fatorCrescimento = [CN[0][0:len(CN)-1],[(i / (1+j)) *100 for i, j in zip(CN[1][1:len(CN[1])], CN[1][0:len(CN[1])-1])]]
    acumulatedData.setdefault(file,[]).append ([OA,CA,CN,ON,GDM,letalidade,incidencia,popContaminada,mortalidade,taxaCrescimento,fatorCrescimento,CAP,OAP,CAP50,OAP50,CAP60,OAP60,CAP75,OAP75]) 
    return acumulatedData

def Letalidade(filename_src,file,title,yLabel):
    
    OA = readCSV(filename_src+'OA'+file+'.csv') 
    CA = readCSV(filename_src+'CA'+file+'.csv')

    toPainel.clear()
    toPainel.setdefault('ObitosAcumulados',[]).append (OA[1][-1]) 
    toPainel.setdefault('CasosAcumulados',[]).append (CA[1][-1]) 

    x = pd.to_datetime(OA[0])
    y = [(i / (1+j)) *100 for i, j in zip(OA[1], CA[1])] 

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

def comparacoCenarios(filename_src,title,yLabel,removelastData = 0):
    
    
    A = readCSV(filename_src+'P.csv')
    B = readCSV(filename_src+'50P.csv')
    C = readCSV(filename_src+'75P.csv')
    D = readCSV(filename_src+'60P.csv')
    
    #D = readCSV(filename_src+'PNP.csv')

    x = pd.to_datetime(B[0])
    plot = figure(plot_height=320, x_axis_type='datetime', title=title)
    plot.line(x=x,y=A[1][0:len(A[1])-removelastData], line_width=2, line_alpha=0.6,legend_label='Mantida no Último Valor',line_color=Spectral6[0])
    plot.circle(x, A[1][0:len(A[1])-removelastData], fill_color = Spectral6[0], size=2)
    plot.line(x=x,y=B[1][0:len(B[1])-removelastData], line_width=2, line_alpha=0.6,legend_label='50% do valor Normal',line_color=Spectral6[0],line_dash="4 4")
    #plot.circle(x, B[1], fill_color=Spectral6[1], size=2)
    plot.line(x=x,y=C[1][0:len(C[1])-removelastData], line_width=1.5, line_alpha=0.6,legend_label='70% do valor Normal',line_color=Spectral6[0],line_dash="4 4")

    plot.line(x=x,y=D[1][0:len(D[1])-removelastData], line_width=1.5, line_alpha=0.6,legend_label='60% do valor Normal',line_color=Paired10[4])
    #plot.circle(x, C[1], fill_color=Spectral6[2], size=2)
    #plot.line(x=x[0:len(D[1])],y=D[1], line_width=3, line_alpha=0.6,legend_label='Dados de Validação de 15 dias anteriores',line_color=Spectral6[3])
    Prediction = Span(location=x[-16-removelastData],dimension='height', line_color='black',line_dash='dashed', line_width=0.5)
    plot.add_layout(Prediction)
    #Prediction = Span(location=x[-21],dimension='height', line_color='black',line_dash='dashed', line_width=0.5)
    #plot.add_layout(Prediction)
    
    plot.xaxis.major_label_orientation = 1.2
    plot.xaxis.axis_label = 'Data de Notificação (Ano de 2020)'
    plot.yaxis.axis_label = yLabel
    plot.legend.location = "top_left"

    hovertool = HoverTool(tooltips=[("x", "$x{%F}"),("y", "@y"),],formatters={'$x': 'datetime',})
    plot.add_tools(hovertool)

    tick_vals = pd.to_datetime(B[2]).astype(int) / 10**6
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
    selectRegiao = Div(text=selecaoRegiaoHTML)
    l=grid([[select, selectmunicipio,selectRegiao],[plot[0], plot[1]],[plot[2], plot[3]],[plot[4], plot[5]],[plot[6], plot[7]],[plot[8], plot[9]],[Paragraph(text= predictionObservations)],[plot[10], plot[11]],[plot[12], plot[13]],[plot[14], plot[15]],[plot[16], plot[17]], [plot[18]]])
    show(l)


acumulatedData = dict()
conjuntodePlots = list()
for i in zip(stateListFile,stateList): 
    
    output_file('./dashboard/'+ i[0] + '.html')
    
    select = Div(text=selecaoHTML)
    selectmunicipio = Div(text=selecaoMunicipiosHTML)

    casosAcumuladosComp     = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'CA'+i[0],"Casos Acumulados no Estado " + i[1] + '(Projeção com Taxa de Isolamento)',"Casos Acumulados")
    obitosAcumuladosComp    = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'OA'+i[0],"Óbitos Acumulados no Estado " + i[1] + '(Projeção com Taxa de Isolamento)',"Óbitos Acumulados")
    letalidade              = Letalidade('D:/Projetos/googleData/data/',i[0],"Evolução da Letalidade no estado " + i[1],"Letalidade em porcentagens")
    incidencia              = Incidencia('D:/Projetos/googleData/data/',i[0], statelist2Population(i[0]), 'Evolução da Incidência no Estado ' + i[1], 'Incidência')
    percentPopulContaminada = PercentPopulContaminada('D:/Projetos/googleData/data/',i[0], statelist2Population(i[0]), 'Evolução da Percentual da População Contaminada no Estado ' + i[1], 'População Contaminada')
    mortalidade             = Mortalidade('D:/Projetos/googleData/data/',i[0], statelist2Population(i[0]), 'Evolução da Mortalidade no Estado ' + i[1],'Mortalidade')
    casosNovos              = CasosNovos('D:/Projetos/googleData/data/',i[0], 'Evolução de Casos Novos no Estado ' + i[1], 'Casos Novos')
    obtosNovos              = ObtosNovos('D:/Projetos/googleData/data/',i[0], 'Evolução de Óbitos Novos no Estado ' + i[1], 'Óbitos Novos')
    casosAcumulados         = CasosAcumulados('D:/Projetos/googleData/data/',i[0], 'Evolução de Casos Acumulados no Estado ' + i[1], 'Casos Acumulados')
    obtosAcumulados         = ObitosAcumulados('D:/Projetos/googleData/data/',i[0], 'Evolução de Óbitos Acumulados no Estado ' + i[1], 'Óbitos Acumulados')
    taxadeCrescimento       = TaxadeCrescimento('D:/Projetos/googleData/data/',i[0],"Evolução da Taxa de Crescimento no estado " + i[1], 'Taxa de Crescimento')
    fatordeCrescimento      = FatordeCrescimento('D:/Projetos/googleData/data/',i[0], 'Evolução do Fator de Crescimento no Estado ' + i[1], 'Fator de Crescimetno')
    mobilidade              = Mobilidade('D:/Projetos/googleData/data/',i[0], "Tendência de mobilidade para Espaços Residenciais (0 Representa a Média) no Estado ",'Mobilidade Residencial')
    acumulatedData[i[0]]    = getAllData('D:/Projetos/googleData/data/',i[0],statelist2Population(i[0]),'D:/Projetos/googleData/dataAn/')[i[0]]
    
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
    selectRegiao = Div(text=selecaoRegiaoHTML)
    l=grid([
    [select,selectmunicipio,selectRegiao],
    [paragraph1,paragraph2,paragraph3,paragraph4,paragraph5],
    [paragraph6,paragraph7,paragraph8,paragraph9,paragraph10],
    [casosAcumuladosComp, obitosAcumuladosComp],
    [mobilidade,mobilidade],
    [paragraphOBS],
    [casosAcumulados, obtosAcumulados],
    [casosNovos, obtosNovos],
    [letalidade, incidencia],
    [percentPopulContaminada,mortalidade],
    [taxadeCrescimento,fatordeCrescimento]
    ])
    show(l) 

Titulos = [ #OA,CA,CN,ON,GDM,letalidade,incidencia,popContaminada,mortalidade,taxaCrescimento,fatorCrescimento,CAP,OAP,CAP50,OAP50,CAP75,OAP75]
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
    "Predição com 60% de intervenção de Casos Acumulados nos Estados do ",
    "Predição com 60% de intervenção de Óbitos Acumulados nos Estados do ",
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
    "Casos Acumulados",
    "Óbitos Acumulados",
    "Casos Acumulados"
]

for i in zip(regioes,listOfRegionsFiles,listOfRegions):
    geracaoPorEstado(i[0],i[1],i[2],acumulatedData,Titulos,yLabel)


#municipios
acumulatedData = dict()
conjuntodePlots = list()
OA_Alberto = getAlbertoData("D:/Projetos/ModeloAlberto/Dados/OA_AL.csv")
CA_Alberto = getAlbertoData("D:/Projetos/ModeloAlberto/Dados/CA_AL.csv")
#CN_Marcus = getAlbertoData('D:/Projetos/covid-br-model-epiforecasts/_nowcasts/covid-regional/brazil/cities-summary/cases.csv')

for j in zip(municipiosFileList,municipiosList, range(len(municipiosList)-1)): 
    for i in zip(j[0],j[1]):
        output_file('./dashboard/'+ i[0] + '.html')
        
        select = Div(text=selecaoHTML)
        selectmunicipio = Div(text=selecaoMunicipiosHTML)

        casosAcumuladosComp     = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'CA'+i[0],"Casos Acumulados no Municipio: " + i[1] + '(Projeção com Taxa de Isolamento)',"Casos Acumulados")
        plotAlberto(casosAcumuladosComp,CA_Alberto,i[1])
        #plotMarcus(casosAcumuladosComp,CN_Marcus,stateListNordesteAbrev[j[2]]+'-'+i[1],9)

        obitosAcumuladosComp    = comparacoCenarios('D:/Projetos/googleData/dataAn/'+'OA'+i[0],"Óbitos Acumulados no Municipio: " + i[1] + '(Projeção com Taxa de Isolamento)',"Óbitos Acumulados")
        plotAlberto(obitosAcumuladosComp,OA_Alberto,i[1])

        paragraphOBS = Paragraph(text= predictionObservations)
        selectRegiao = Div(text=selecaoRegiaoHTML)

        l=grid([
        [select,selectmunicipio,selectRegiao],
        [casosAcumuladosComp, obitosAcumuladosComp],
        [paragraphOBS],
        ])
        #break
        show(l)



#Regioes de Saude
# datas estão começando erradas das predições
acumulatedData = dict()
conjuntodePlots = list()

for j in RegioesSaude: 
    output_file('./dashboard/'+ j + '.html')
    
    select = Div(text=selecaoHTML)
    selectmunicipio = Div(text=selecaoMunicipiosHTML)
    selectRegiao = Div(text=selecaoRegiaoHTML)

    casosAcumuladosComp     = comparacoCenarios('D:/Projetos/googleData/dataAn/'+ j,"Casos: " + j,"Casos")
    if j[6] == 'C':
        casosAcumuladosComp     = comparacoCenarios('D:/Projetos/googleData/dataAn/'+ j,"Casos Acumulados: " + j,"Casos Acumulados")
    else:
        casosAcumuladosComp     = comparacoCenarios('D:/Projetos/googleData/dataAn/'+ j,"Óbitos Acumulados: " + j,"Óbitos Acumulados")
    paragraphOBS = Paragraph(text= predictionObservations)
    l=grid([
    [select,selectmunicipio,selectRegiao],
    [casosAcumuladosComp],
    [paragraphOBS]
    ])
    #break
    show(l)
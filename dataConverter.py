import csv, os
import shutil
import xlrd
from unidecode import unidecode
import pandas as pd
from datetime import datetime, timedelta

#xlxsDir = 'C:/Users/andre/Downloads/'
xlxsDir = '/home/travis/Downloads/'
filename_src = './dataRaw/'
filename_dest = './data/'

def csv_from_excel(xlsxFile):
    #wb = xlrd.open_workbook(xlsxFile)
    splitedFinenameFromExtension = xlsxFile.split('.')
    splitedFinename = splitedFinenameFromExtension[0].split('/')
    splitedFinename = splitedFinename[-1]
    '''
    sh = wb.sheet_by_name('Sheet 1')
    splitedFinename = xlsxFile.split('.')
    your_csv_file = open(splitedFinenameFromExtension[0] + '.csv', 'w', encoding="utf8", newline="")
    wr = csv.writer(your_csv_file,delimiter=";")
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()'''
    df = pd.read_excel(xlsxFile)
    df.to_csv(splitedFinenameFromExtension[0] + '.csv')
    return splitedFinenameFromExtension[0] + '.csv'

def copiarPastas(src,dest):
    src_files = os.listdir(src)
    if os.path.isfile(src  + src_files[0]):
        print(src + src_files[0])
        newsrc = csv_from_excel(src + src_files[0])
        shutil.copy(newsrc, dest)
        splitedFinename = newsrc.split('/')
        src_files[0] = splitedFinename[-1]

    return dest + src_files[0]

def getFilename(src):
    src_files = os.listdir(src)
    filename_src = ''
    for file_name in src_files:
        file_name = csv_from_excel(src + file_name)
        filename_src = src + file_name
    return filename_src

def CasosToNum(shortMonth):
    return{
            'CasosAcumulados' : 10,
            'CasosNovos'      : 11,
            'obitosAcumulado' : 12,
            'obitosNovos'     : 13,
            'Recuperadosnovos': 14,
            'emAcompanhamentoNovos': 15
    }[shortMonth]

def writeDataCsV(filename_dest,data,tipo,state,complement):
    tipo = tipo + complement
    with open(filename_dest+tipo+'.csv', "w", encoding="utf8", newline="") as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
        stateDataRaw = data[state]
        #stateData = sumStateData(stateDataRaw)

        #valorAnterior = 0
        writer.writerow(['Data', tipo])
        for i in stateDataRaw:
            if i[1] == '':
                value = 0
            else:
                value = float(i[1])
            #if valorAnterior > value:
            #    break
            #valorAnterior = value
            writer.writerow([i[0], value])
        
        #for i in sorted(stateData):
                #writer.writerow([i, stateData[i]])

def splitData(filename_src,data):
    Dict_data = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")

        lastRow = ''
        for row in reader: 
            #row = row[1:]
            if lastRow == 'Centro-Oeste' and row[0] == 'Norte':
                break
            lastRow = row[0] 
            Dict_data.setdefault(row[1],[]).append ([ row[7],row[CasosToNum(data)] ]) 
    return Dict_data

def sumStateData(dataState):
    Dict_day = dict()
    for date in dataState:
        for row in dataState[date]:
            if not Dict_day.get(date):
                newstr = row[3]
                if newstr == '':
                    newstr = '0'
                Dict_day[date] = float(newstr)
            else:
                newstr = row[3]
                if newstr == '':
                    newstr = '0'
                Dict_day[date] = Dict_day[date] + float(newstr)
    return Dict_day

def splitDataPorRegiaoDeSaude(filename_src,data,region,state):
    Dict_Regiao = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            #row = row[1:]
            if row[0] == region and row[1] == state:
                if Dict_Regiao.get(row[5]):
                    Dict_Regiao[row[5]].setdefault(row[7],[]).append([row[0],row[1],row[2],row[CasosToNum(data)] ])
                else:
                    date = dict()
                    date.setdefault(row[7],[]).append([row[0],row[1],row[2],row[CasosToNum(data)]])
                    Dict_Regiao.setdefault(row[5],dict()).update(date)
    return Dict_Regiao

def writeDataCsVPorRegiaoDeSaude(filename_dest,data,tipo,region,state):
    flag = False
    nameRegSaude = list()
    for regioesDeSaude in data:
        
        if not flag or regioesDeSaude == '':
            flag = True
            continue

        tipoN = region + state + tipo + regioesDeSaude
        stateDataRaw = data[regioesDeSaude]
        stateData = sumStateData(stateDataRaw)
        tipoN = tipoN.split('.')[0]
        with open(filename_dest+tipoN+'.csv', "w", encoding="utf8", newline="") as edge_file:
            writer = csv.writer(edge_file, delimiter=",")
            nameRegSaude.append(tipoN)
            writer.writerow(['Data', tipoN])
            for i in sorted(stateData):
                    writer.writerow([i, stateData[i]])
    print(nameRegSaude)

def splitDataPorMunicipio(filename_src,data,state,municipio):
    Dict_data = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            #row = row[1:]
            if(row[1] == state and municipio == row[2]):
                Dict_data.setdefault(row[2],[]).append ([ row[7],row[CasosToNum(data)] ]) 
    return Dict_data

def writeDataCsVPorMunicipio(filename_dest,data,tipo,municipio,state):
    municipioCode = ''
    for i in range(len(municipio)):
        if i%2 == 0 and municipio[i] != ' ':
            municipioCode = municipioCode + municipio[i]+'i'
    tipoN = tipo + state[0] + 'i' + state[1] + unidecode(municipioCode)
    #print(tipoN)
    stateDataRaw = data[municipio]

    with open(filename_dest+tipoN+'.csv', "w", encoding="utf8", newline="") as edge_file:
        writer = csv.writer(edge_file, delimiter=",")

        writer.writerow(['Data', tipoN])
        for i in stateDataRaw:
                writer.writerow([i[0], i[1]])

def runMunicipios(municipio,state):
    Dict_data_casosAcumulados = splitDataPorMunicipio(filename_src,'CasosAcumulados',state,municipio)
    writeDataCsVPorMunicipio(filename_dest, Dict_data_casosAcumulados, 'CA',municipio,state)
    Dict_data_casosAcumulados = splitDataPorMunicipio(filename_src,'obitosAcumulado',state,municipio)
    writeDataCsVPorMunicipio(filename_dest, Dict_data_casosAcumulados, 'OA',municipio,state)
    Dict_data_casosAcumulados = splitDataPorMunicipio(filename_src,'Recuperadosnovos',state,municipio)
    writeDataCsVPorMunicipio(filename_dest, Dict_data_casosAcumulados, 'RN',municipio,state)
    Dict_data_casosAcumulados = splitDataPorMunicipio(filename_src,'emAcompanhamentoNovos',state,municipio)
    writeDataCsVPorMunicipio(filename_dest, Dict_data_casosAcumulados, 'EAN',municipio,state)
    
    municipioCode = ''
    for i in range(len(municipio)):
        if i%2 == 0 and municipio[i] != ' ':
            municipioCode = municipioCode + municipio[i]+'i'
    print('"'+ state[0] + 'i' + state[1]+unidecode(municipioCode)+'"')

def runAll(state,legend):
    
    Dict_data_casosAcumulados = splitData(filename_src,'CasosAcumulados')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'obitosAcumulado')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'OA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'Recuperadosnovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'RN',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'CasosNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CN',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'obitosNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'ON',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'emAcompanhamentoNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'EAN',state,legend)

def splitDataBrasil(filename_src,data):
    Dict_data = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")

        lastRow = ''
        for row in reader: 
            #row = row[1:]
            if lastRow == 'Brasil' and row[0] == 'Norte':
                break
            lastRow = row[0] 
            Dict_data.setdefault(row[0],[]).append ([ row[7],row[CasosToNum(data)] ]) 
    return Dict_data

def runBrasil(state,legend):
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'CasosAcumulados')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CA',state,legend)
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'obitosAcumulado')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'OA',state,legend)
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'CasosNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CN',state,legend)
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'obitosNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'ON',state,legend)
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'Recuperadosnovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'RN',state,legend)
    Dict_data_casosAcumulados = splitDataBrasil(filename_src,'emAcompanhamentoNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'EAN',state,legend)

def runRegioesSaude(region,regionAbrev,state):
    Dict_data_casosAcumulados = splitDataPorRegiaoDeSaude(filename_src,'CasosAcumulados',region,state)
    writeDataCsVPorRegiaoDeSaude(filename_dest, Dict_data_casosAcumulados, 'RSCA',regionAbrev,state)

    Dict_data_casosAcumulados = splitDataPorRegiaoDeSaude(filename_src,'obitosAcumulado',region,state)
    writeDataCsVPorRegiaoDeSaude(filename_dest, Dict_data_casosAcumulados, 'RSOA',regionAbrev,state)


#filename_src = copiarPastas(xlxsDir,filename_src)
#os.system('cd /home/travis/Downloads \n ls')
#os.system('cd ' + './dataRaw/' + ' \n ls')
today_date_str = "".join(str(datetime.now().date()).split("-"))
filename_src = './dataRaw/'+"Brasil_COVID19-" + today_date_str + ".csv"
#filename_src = './dataRaw/HIST_PAINEL_COVIDBR_04jun2020.csv'
# Norte

runBrasil('Brasil','BiR_An')

runAll('RO','RiO_An')
runAll('AC','AiC_An')
runAll('AM','AiM_An')
runAll('RR','RiR_An')
runAll('PA','PiA_An')
runAll('AP','AiP_An')
runAll('TO','TiO_An')

# nordeste
runAll('RN','RiN_An')
runAll('PB','PiB_An')
runAll('BA','BiA_An')
runAll('SE','SiE_An')
runAll('AL','AiL_An')
runAll('MA','MiA_An')
runAll('PE','PiE_An')
runAll('CE','CiE_An')
runAll('PI','PiI_An')

# Suldeste
runAll('MG','MiG_An')
runAll('ES','EiS_An')
runAll('RJ','RiJ_An')
runAll('SP','SiP_An')

# Sul
runAll('PR','PiR_An')
runAll('SC','SiC_An')
runAll('RS','RiS_An')

# Centro-Oeste
runAll('MS','MiS_An')
runAll('MT','MiT_An')
runAll('GO','GiO_An')
runAll('DF','DiF_An')

municipioListBA = ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Itabuna', 'Juazeiro']
municipioListSE = ['Aracaju', 'Itabaiana', 'Estância', 'Lagarto']
municipioListAL = ['Maceió', 'Arapiraca','Murici', 'Coruripe', 'Palmeira dos Índios']
municipioListPE = ['Recife', 'Petrolina', 'Caruaru']
municipioListPB = ['João Pessoa', 'Campina Grande', 'Sousa', 'Patos']
municipioListRN = ['Natal', 'Mossoró']
municipioListCE = ['Fortaleza','Juazeiro do Norte', 'Sobral']
municipioListPI = ['Teresina'] #'Picos','São Raimundo Nonato'
municipioListMA = ['São Luís', 'Imperatriz', 'Caxias']


for i in municipioListBA:
    runMunicipios(i, 'BA')

for i in municipioListSE:
    runMunicipios(i, 'SE')

for i in municipioListAL:
    runMunicipios(i, 'AL')

for i in municipioListPE:
    runMunicipios(i, 'PE')

for i in municipioListPB:
    runMunicipios(i, 'PB')

for i in municipioListRN:
    runMunicipios(i, 'RN')

for i in municipioListCE:
    runMunicipios(i, 'CE')

for i in municipioListPI:
    runMunicipios(i, 'PI')
    
for i in municipioListMA:
    runMunicipios(i, 'MA')


NElist = ['RN','PB','BA','SE','AL','MA','PE','CE','PI']
SElist = ['MG','ES','RJ','SP']
Nlist = ['RO','AC','AM','RR','PA','AP','TO']
Slist = ['PR','SC','RS']
COlist = ['MS','GO','MT']
for i in NElist:
    runRegioesSaude('Nordeste','NE',i)

for i in Nlist:
    runRegioesSaude('Norte','NO',i)

for i in Slist:
    runRegioesSaude('Sul','SU',i)

for i in SElist:
    runRegioesSaude('Sudeste','SE',i)

for i in COlist:
    runRegioesSaude('Centro-Oeste','CO',i)
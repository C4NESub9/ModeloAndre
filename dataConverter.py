import csv, os
import shutil
import xlrd

#xlxsDir = 'C:/Users/andre/Downloads/'
xlxsDir = '/home/travis/Downloads/'
filename_src = './dataRaw/'
filename_dest = './data/'

def csv_from_excel(xlsxFile):
    wb = xlrd.open_workbook(xlsxFile)
    splitedFinenameFromExtension = xlsxFile.split('.')
    splitedFinename = splitedFinenameFromExtension[0].split('/')
    splitedFinename = splitedFinename[-1]

    sh = wb.sheet_by_name('Sheet 1')
    splitedFinename = xlsxFile.split('.')
    your_csv_file = open(splitedFinenameFromExtension[0] + '.csv', 'w', encoding="utf8", newline="")
    wr = csv.writer(your_csv_file,delimiter=";")
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
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
            'obitosAcumulado' : 11,
            'Recuperadosnovos': 12,
            'emAcompanhamentoNovos': 13
    }[shortMonth]

def writeDataCsV(filename_dest,data,tipo,state,complement):
    tipo = tipo + complement
    with open(filename_dest+tipo+'.csv', "w", encoding="utf8", newline="") as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
        stateDataRaw = data[state]
        #stateData = sumStateData(stateDataRaw)

        valorAnterior = 0
        writer.writerow(['Data', tipo])
        for i in stateDataRaw:
            if i[1] == '':
                value = 0
            else:
                value = int(i[1])
            if valorAnterior > value:
                break
            valorAnterior = value
            writer.writerow([i[0], value])
        
        #for i in sorted(stateData):
                #writer.writerow([i, stateData[i]])

def splitData(filename_src,data):
    Dict_data = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=";")

        for row in reader:
            Dict_data.setdefault(row[1],[]).append ([ row[7],row[CasosToNum(data)] ]) 
    return Dict_data

def sumStateData(dataState):
    Dict_day = dict()
    for row in dataState:
        if Dict_day.get(row[0], []) == []:
            newstr = row[1].replace("'", "")
            if newstr == '':
                newstr = '0'
            Dict_day[row[0]] = float(newstr)
        else:
            newstr = row[1].replace("'", "")
            if newstr == '':
                newstr = '0'
            Dict_day[row[0]] = Dict_day[row[0]] + float(newstr)
    return Dict_day

def splitDataPorRegiaoDeSaude(filename_src,data):
    Dict_data = dict()
    filename_src = filename_src.split('.')
    with open('.' + filename_src[1] + '.csv', "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=";")
        for row in reader:
            Dict_data.setdefault(row[5],[]).append ([ row[7],row[CasosToNum(data)] ]) 
    return Dict_data

def writeDataCsVPorRegiaoDeSaude(filename_dest,data,tipo):
    flag = False
    for regioesDeSaude in data:
        
        if not flag or regioesDeSaude == '':
            flag = True
            continue

        tipoN = tipo + regioesDeSaude
        stateDataRaw = data[regioesDeSaude]
        stateData = sumStateData(stateDataRaw)

        with open(filename_dest+tipoN+'.csv', "w", encoding="utf8", newline="") as edge_file:
            writer = csv.writer(edge_file, delimiter=",")

            writer.writerow(['Data', tipoN])
            for i in sorted(stateData):
                    writer.writerow([i, stateData[i]])

def runAll(state,legend):
    Dict_data_casosAcumulados = splitData(filename_src,'CasosAcumulados')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'obitosAcumulado')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'OA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'Recuperadosnovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'RN',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'emAcompanhamentoNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'EAN',state,legend)


filename_src = copiarPastas(xlxsDir,filename_src)
#os.system('cd /home/travis/Downloads \n ls')
#os.system('cd ' + './dataRaw/' + ' \n ls')
#filename_src = './dataRaw/HIST_PAINEL_COVIDBR_24mai2020.csv'
runAll('RN','RiN_An')
runAll('PB','PiB_An')
runAll('BA','BiA_An')
runAll('SE','SiE_An')
runAll('AL','AiL_An')
runAll('MA','MiA_An')
runAll('PE','PiE_An')
runAll('CE','CiE_An')
runAll('PI','PiI_An')

#Dict_data_casosAcumulados = splitDataPorRegiaoDeSaude(filename_src,'CasosAcumulados')
#writeDataCsVPorRegiaoDeSaude(filename_dest, Dict_data_casosAcumulados, 'RSCA')

#Dict_data_casosAcumulados = splitDataPorRegiaoDeSaude(filename_src,'obitosAcumulado')
#writeDataCsVPorRegiaoDeSaude(filename_dest, Dict_data_casosAcumulados, 'RSOA')
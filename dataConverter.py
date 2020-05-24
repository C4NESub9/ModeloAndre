import csv, os
import shutil
import xlrd

filename_src = './dataRaw/'
filename_dest = './data/'

def csv_from_excel(xlsxFile):
    wb = xlrd.open_workbook(xlsxFile)
    splitedFinename = xlsxFile.split('.')
    splitedFinename = splitedFinename.split('/')[-1]

    sh = wb.sheet_by_name(splitedFinename)
    your_csv_file = open(splitedFinename + '.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
    return splitedFinename + '.csv'

def copiarPastas(src,dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        if os.path.isfile(src  + file_name):
            shutil.copy(src + file_name, dest)

def getFilename(src):
    src_files = os.listdir(src)
    filename_src = './dataRaw/'
    for file_name in src_files:
        file_name = csv_from_excel(filename_src + file_name)
        filename_src = filename_src + file_name
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
        stateData = sumStateData(stateDataRaw)

        writer.writerow(['Data', tipo])
        for i in sorted(stateData):
                writer.writerow([i, stateData[i]])

def splitData(filename_src,data):
    Dict_data = dict()
    with open(filename_src, "r", encoding="utf8", newline="") as f:
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

def runAll(state,legend):
    Dict_data_casosAcumulados = splitData(filename_src,'CasosAcumulados')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'CA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'obitosAcumulado')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'OA',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'Recuperadosnovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'RN',state,legend)

    Dict_data_casosAcumulados = splitData(filename_src,'emAcompanhamentoNovos')
    writeDataCsV(filename_dest, Dict_data_casosAcumulados, 'EAN',state,legend)


copiarPastas('/home/travis/Downloads','./dataRaw/')
filename_src = getFilename('/home/travis/Downloads')

runAll('RN','RiN_An')
runAll('PB','PiB_An')
runAll('BA','BiA_An')
runAll('SE','SiE_An')
runAll('AL','AiL_An')
runAll('MA','MiA_An')
runAll('PE','PiE_An')
runAll('CE','CiE_An')
runAll('PI','PiI_An')

import csv

filename_src = '/home/travis/build/C4NESub9/ModeloAndre/HIST_PAINEL_COVIDBR_20mai2020.csv'
filename_dest = '/home/travis/build/C4NESub9/ModeloAndre/data/'

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



runAll('RN','RiN_An')
runAll('PB','PiB_An')
runAll('BA','BiA_An')
runAll('SE','SiE_An')
runAll('AL','AiL_An')
runAll('MA','MiA_An')
runAll('PE','PiE_An')
runAll('CE','CiE_An')
runAll('PI','PiI_An')

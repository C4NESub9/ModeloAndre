import csv
from datetime import datetime
from datetime import timedelta 
import time 

a = datetime.today()
print(a)
'''
stateListFileNordeste = ["AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"]

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


filename_src = 'D:/Projetos/googleData/data/'
filename_srcPredictions = 'D:/Projetos/googleData/dataAn/'

for file in stateListFileNordeste:

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
    ON = readCSV(filename_src+'ON'+file+'.csv') '''
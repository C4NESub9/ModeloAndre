from selenium import webdriver
import time, os
import csv
import shutil

#https://transparencia.registrocivil.org.br/registros fazer comparação de mortes

#   src = 'C:/Users/andre/Downloads/Global_Mobility_Report.csv'
src = '/home/travis/Downloads/Global_Mobility_Report.csv'
dest = './dataRaw/'
filename_dest = './data/'

def CasosToNum(shortMonth):
    return{
        'date' : 4,
        'retail_and_recreation_percent_change_from_baseline' : 5,
        'grocery_and_pharmacy_percent_change_from_baseline': 6,
        'parks_percent_change_from_baseline' : 7,
        'transit_stations_percent_change_from_baseline' : 8,
        'workplaces_percent_change_from_baseline': 9,
        'residential_percent_change_from_baseline': 10
    }[shortMonth]

def splitData(filename_src,columnData):
    Dict_data = dict()
    with open(filename_src, "r", encoding="utf8", newline="") as f:
        reader = csv.reader(f,delimiter=",")

        for row in reader:
            if row[0] == 'BR':
                #print(row)
                Dict_data.setdefault(row[2],[]).append ([ row[CasosToNum('date')],row[CasosToNum(columnData)] ]) 
    return Dict_data

def getData(src,dest):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com/covid19/mobility/')

    python_button = driver.find_elements_by_class_name("icon-link")
    #python_button[3].ATTR = 'TXT:Fazer<SP>o<SP>download<SP>do<SP>CSV<SP>global'
    time.sleep(10)
    fi = python_button[0].click()
    time.sleep(20)
    driver.quit()

    shutil.copy(src, dest)

def writeDataCsV(filename_dest,state, stateName):
    with open(filename_dest, "w", encoding="utf8", newline="") as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
        stateDataRaw = state[stateName]
        #GDM = Google data Mobility
        writer.writerow(['Data', 'GDM'])
        for i in stateDataRaw:
            if i[1] == '':
                value = 0
            else:
                value = int(i[1])

            writer.writerow([i[0], value])

getData(src,dest)
BrazilMobility = splitData(dest+'Global_Mobility_Report.csv','residential_percent_change_from_baseline')
#print(BrazilMobility)

SO = 'State of '
stateListFileNordeste = ["AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"]
stateListNordeste = ['State of Alagoas', 'State of Bahia', 'State of Ceará', 'State of Maranhão', 'State of Paraíba', 'State of Pernambuco', 'State of Piauí', 'State of Rio Grande do Norte', 'State of Sergipe']

stateListFileNorte = ["RiO_An","AiC_An","AiM_An","RiR_An","PiA_An","AiP_An","TiO_An"]
stateListNorte = [SO+ 'Rondônia', SO+'Acre' , SO+'Amazonas' , SO+ 'Roraima', SO+'Pará', SO+'Amapá', SO+'Tocantins']

stateListFileSuldeste = ["MiG_An","EiS_An","RiJ_An","SiP_An"]
stateListSuldeste = [SO+ 'Minas Gerais', SO+ 'Espírito Santo', SO+ 'Rio de Janeiro', SO+'São Paulo' ]

stateListFileSul = ["PiR_An","SiC_An","RiS_An"]
stateListSul = [SO+'Paraná' , SO+ 'Santa Catarina' , SO+'Rio Grande do Sul' ]

stateListFileCentro = ["MiS_An","MiT_An","GiO_An","DiF_An"]
stateListCentro = [SO+'Mato Grosso do Sul' , SO+'Mato Grosso' , SO+'Goiás' , 'Federal District']

stateListFile = ["BiR_An"] + stateListFileNordeste + stateListFileNorte + stateListFileSuldeste + stateListFileSul + stateListFileCentro
stateList = [""] + stateListNordeste + stateListNorte + stateListSuldeste + stateListSul + stateListCentro

for i in zip(stateListFile,stateList):
    writeDataCsV(filename_dest+'GDM' + i[0] + '.csv',BrazilMobility, i[1])


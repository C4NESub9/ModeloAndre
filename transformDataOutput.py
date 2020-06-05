from csv import DictReader
import datetime
from datetime import datetime, timedelta
import csv
import os

filename_src = './data/'
filename_srcDate = './dataAn/'

def ReadAllCsvFromFolder(src,dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        listasrc = []
        lista    = []
        if os.path.isfile(src  + file_name):
            splitedFinename = file_name.split('.')
            if "CA" in file_name or "OA" in file_name and os.path.isfile(dest + splitedFinename[0] +'P.'+ splitedFinename[1]):
                with open(src + file_name, "r", encoding="utf8", newline="") as f:
                    with open(dest + splitedFinename[0] +'P.'+ splitedFinename[1], "r", encoding="utf8", newline="") as f2:
                        reader_dest= csv.reader(f2, delimiter=",")
                        reader_src = csv.reader(f,delimiter=",")

                        for row in reader_src:
                            listasrc.append(row[0])
                        i = 0
                        daysFuture = 1
                        for row in reader_dest:
                            if i < len(listasrc):
                                lista.append([listasrc[i], row[1], row[0]])
                                i = i+1
                            else:
                                date = datetime.strptime(listasrc[i-1], '%Y-%m-%d').date() + timedelta(days=daysFuture)
                                lista.append(["'"+date.strftime('%Y-%m-%d')+"'", row[1], '+'])
                                daysFuture = daysFuture + 1
                with open(dest + splitedFinename[0] +'P.'+ splitedFinename[1], "w", encoding="utf8", newline="") as edge_file:
                    writer = csv.writer(edge_file, delimiter=",")
                    for row in lista:
                        writer.writerow([row[0],row[1],row[2]])
                #print(lista)
                            
    return lista

#with open(filename_dest+tipo+'.csv', "w", encoding="utf8", newline="") as edge_file:
#writer = csv.writer(edge_file, delimiter=",")
            
List = ReadAllCsvFromFolder(filename_src,filename_srcDate)
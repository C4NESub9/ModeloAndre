import yagmail
import os
import shutil

def copiarPastas(src,dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        if os.path.isfile(src  + file_name):
            shutil.copy(src + file_name, dest)


#yag = yagmail.SMTP('lordcobisco@gmail.com', 'ttahdkvnxxqbiytx')
#contents = [
#    'O relatorio de atualizacao segue em anexo. Para maiores informacoes acesse https://sites.google.com/d/1dRa745GQAOJHlC4mE_q89EHhKSw1FFW7/p/1bYgijzz9UOfCVjX9qpU0xFt3hs8AvAuP agradecemos desde ja a atencao.',
#]

#yag.send('andre.dantas@isd.org.br', 'Dados Coronavirus', contents, attachments=['/home/travis/build/C4NESub9/ModeloAlberto/data/results.csv'])

os.system('cd /home/travis/build/C4NESub9/ \n  git clone https://neurodeveloperISD:,Lc258147@github.com/C4NESub9/googleData.git')
copiarPastas('/home/travis/build/C4NESub9/ModeloAlberto/data/','/home/travis/build/C4NESub9/googleData/dataAn/')
os.system('cd /home/travis/build/C4NESub9/googleData/ \n git remote set-url origin https://neurodeveloperISD:,Lc258147@github.com/C4NESub9/googleData.git \n git add . \n git commit -m "Atualizacao dos dados" \n git push')






filename = "D:/Projetos/ModeloAndre/dataAn/"

Selection = ' <select onchange="location.href=this.value">'
Selection = Selection + '<option value="#">Selecione o Estado para visualização Gráfica</option>'
#iterar com os ters itens abaixo
ItemSelecaoInicio = '    <option value="./dashboard/"' #somarvalores aqui do arquivo html
ItemSelecaoMeio = '>' # COlocar o nome do estado a ser selecionado
ItemSelecaoFim = '</option>\n'
FimSelecion = '</select>'

dataType = ["CA","OA"]
states = ["AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"]
statesNames = ["Alagoas","Bahia","Ceará","Maranhão","Paraíba","Pernambuco","Piaui","RN","Sergipe"]

for i in dataType:
    counter = 0
    for j in states:
        Selection = Selection + ItemSelecaoInicio + i + j + '.csv' + ItemSelecaoMeio + statesNames[counter] + ItemSelecaoFim 
        counter = counter +1

print(Selection+FimSelecion)
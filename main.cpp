//#include <QCoreApplication>
#include "SistemasdeControle/headers/optimizationLibs/leastsquare.h"
#include <QFile>
#include <QStringList>
#include <QTextStream>

ModelHandler::ARX<double> *arx;
OptimizationHandler::LeastSquare<double> *LS;
LinAlg::Matrix<double> data;

void pegarDados(QString nome)
{
    //QFile file(ui->lineEdit->text().toStdString().c_str());
    //QString filename = "D:\\Projetos\\ModeloAndre\\data\\";
    QString filename = "/home/travis/build/C4NESub9/ModeloAndre/data/";
    QFile file(filename+nome+".csv");
    file.open(QIODevice::ReadOnly);

    //ui->textEdit->append("\n\n Dados Importados do CSV\n");
    std::string matrix;
    uint16_t counter = 0;
    while (!file.atEnd()) {
        QByteArray line = file.readLine();
        QString str = line.split(',')[1];

         //ui->textEdit->append(str);
         if(counter > 0)
         {
             QString temp = str;//.split(',')[1];
             if(temp == "+")
                 break;
             matrix += temp.toStdString()+",";
         }
        counter++;
    }
    file.close();

    matrix.erase(matrix.size()-1);

    LinAlg::Matrix<double> Input = LinAlg::Zeros<double>(1,counter-1);
    LinAlg::Matrix<double> Output = matrix;
//    for(int i = 0; i < Output.getNumberOfRows(); ++i)
//        for(int j = 0; j < Output.getNumberOfColumns(); ++j)
//                Output(i,j) = log10(Output(i,j));

    //arx = new ModelHandler::ARX<double>(0,ui->lineEdit_3->text().toInt());
    arx = new ModelHandler::ARX<double>(0,4);
    LS = new OptimizationHandler::LeastSquare<double>(arx);
    //ui->textEdit->append("\n\n Equação com os parâmetros ajustados por Mínimos Quadrados\n");
    LS->Optimize(Input,Output);
    //std::string str; str += arx->print();
    //ui->textEdit->append(str.c_str());

    //Input = LinAlg::Zeros<double>(1,counter);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    //for(unsigned i = 1; i < ui->lineEdit_4->text().toInt(); ++i)
    for(unsigned i = 1; i < counter; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-1)));
    //for(unsigned i = ui->lineEdit_4->text().toInt(); i < counter; ++i)
    //    estOutput(0,i) = arx->sim(0,estOutput(0,i-1));

    //ui->textEdit->append("\n\n Resposta do modelo (predição de 1 passo até da quantidade de dados para validação)\n amostra_n Saida Saida Estimada Erro\n");
    //data = (~LinAlg::LineVector<double>(1,counter-1)|(~(Output(0,from(0)-->counter-2)||estOutput(0,from(1)-->counter-1)))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //str.clear(); str << this->data;
    //ui->textEdit->append(str.c_str());
    //ui->textEdit->append("\n\n Erro médio Quadrático\n");
    //double MSE = 0;
    //for(int i = 0; i < Output.getNumberOfRows(); ++i)
    //    for(int j = 1; j < counter-1; ++j)
     //           MSE += pow(Output(i,j-1)-estOutput(i,j),2);
    //ui->textEdit->append(QString::number(MSE));

    double temp = estOutput(0,counter-1);
    //ui->textEdit->append("\n\n Valores preditos\n");
    //for(unsigned i = 0; i< ui->lineEdit_2->text().toInt(); ++i)
    LinAlg::Matrix<double> predictOutput(1,7);
    for(unsigned i = 0; i < 7; ++i)
    {
        temp = arx->sim(0,temp);
        predictOutput(0,i) = temp;
        //ui->textEdit->append(QString::number(temp));
    }
    data = ((~(Output(0,from(0)-->counter-2)))|(~(estOutput(0,from(1)-->counter-1)|predictOutput))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data;
}

void salvarDados(QString nome)
{
    //QString filename = "D:\\Projetos\\ModeloAndre\\dataAn\\";
    QString filename = "/home/travis/build/C4NESub9/ModeloAndre/dataAn/";
    QFile file(filename+nome+"P.csv");
    //QFile file(ui->lineEdit_5->text().toStdString().c_str());
    file.open(QIODevice::WriteOnly | QIODevice::Truncate );
    //ui->textEdit->append("\n\nDados Salvos!!!\n\n");

    QTextStream stream(&file);
    stream << "Saida,Saida_Estimada,Erro\n";
    for(int i = 0; i < data.getNumberOfRows(); ++i){
        for(int j = 0; j < data.getNumberOfColumns();++j)
            stream << QString::number(data(i,j)) << ',';
        stream << '\n';
    }

    file.close();
}

int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);
    QString estados[9] = {"AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"};
    QString tipoDados[2] = {"CA","OA"};

    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < 9; ++j){
            pegarDados (tipoDados[i] + estados[j]);
            salvarDados(tipoDados[i] + estados[j]);
        }

    return 0;
}

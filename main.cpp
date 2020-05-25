//#include <QCoreApplication>
#include "SistemasdeControle/headers/optimizationLibs/leastsquare.h"
#include "extendedleastsquare.h"
#include <QFile>
#include <QStringList>
#include <QTextStream>

ModelHandler::ARX<double> *arx;
OptimizationHandler::LeastSquare<double> *LS;
OptimizationHandler::ExtendedLeastSquare<double> *ELS;
LinAlg::Matrix<double> data;

LinAlg::Matrix<double> findBestModel(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4;
    for(uint8_t k = 1; k < 6; ++k){
        arx = new ModelHandler::ARX<double>(0,k);
        ELS = new OptimizationHandler::ExtendedLeastSquare<double>(arx);
        ELS->Optimize(Input,Output);
        error = ELS->getFinalError();
        uint16_t N = error.getNumberOfRows();
        double C = (((~error)*error)(0,0))/N;
        double AIC4_temp = N*log(C)+4*(k+1);
        double BIC_temp = N*log(C)+(k+1)*log(N);

        if(AIC4_temp < AIC4  && BIC_temp < BIC)
        {
            AIC4 = AIC4_temp; BIC = BIC_temp;
            ModelCoef = arx->getModelCoef();
        }

    }

    return ModelCoef;
}

void pegarDados(QString nome)
{
    QString filename = "D:\\Projetos\\ModeloAndre\\data\\";
    //QString filename = "/home/travis/build/C4NESub9/ModeloAndre/data/";
    QFile file(filename+nome+".csv");
    file.open(QIODevice::ReadOnly);

    std::string matrix;
    uint16_t counter = 0;
    while (!file.atEnd()) {
        QByteArray line = file.readLine();
        QString str = line.split(',')[1];

         if(counter > 0){
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

    //arx = new ModelHandler::ARX<double>(0,3);
    ////LS = new OptimizationHandler::LeastSquare<double>(arx);
    ////LS->Optimize(Input,Output);
    ////std::cout << arx->getModelCoef();
    //ELS = new OptimizationHandler::ExtendedLeastSquare<double>(arx);
    //ELS->Optimize(Input,Output);

    LinAlg::Matrix<double> ModelCoef = findBestModel(Input, Output);
    arx = new ModelHandler::ARX<double>(0,ModelCoef.getNumberOfRows());
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 2; i < counter; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));

    double temp = estOutput(0,counter-1);
    LinAlg::Matrix<double> predictOutput(1,7);
    for(unsigned i = 0; i < 7; ++i){
        temp = arx->sim(0,temp);
        predictOutput(0,i) = (int)temp;
    }
    data = ((~(Output(0,from(0)-->counter-2)))|(~(estOutput(0,from(1)-->counter-1)|predictOutput))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data << std::endl;
    std::cout << arx->print() << std::endl;
}

void salvarDados(QString nome)
{
    QString filename = "D:\\Projetos\\ModeloAndre\\dataAn\\";
    //QString filename = "/home/travis/build/C4NESub9/ModeloAndre/dataAn/";
    QFile file(filename+nome+"P.csv");
    file.open(QIODevice::WriteOnly | QIODevice::Truncate );

    QTextStream stream(&file);
    stream << "Saida,Saida_Estimada,Erro\n";
    for(int i = 0; i < data.getNumberOfRows(); ++i){
        for(int j = 0; j < data.getNumberOfColumns();++j)
            stream << QString::number(data(i,j)) << ',';
        stream << '\n';
    }

    file.close();
}

int main()
{
   QString estados[9] = {"AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An"};
    QString tipoDados[2] = {"CA","OA"};

    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < 9; ++j){
            pegarDados (tipoDados[i] + estados[j]);
            salvarDados(tipoDados[i] + estados[j]);
        }

    return 0;
}

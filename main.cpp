//#include <QCoreApplication>
#include "SistemasdeControle/headers/optimizationLibs/leastsquare.h"
#include "extendedleastsquare.h"
#include <QFile>
#include <QStringList>
#include <QTextStream>
#include <QDate>

//ModelHandler::ARX<double> *arx;
//OptimizationHandler::LeastSquare<double> *LS;
//OptimizationHandler::ExtendedLeastSquare<double> *ELS;
//LinAlg::Matrix<double> data;

LinAlg::Matrix<double> findBestARModelMQ(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::LeastSquare<double> *LS;

    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 1; k < 3; ++k){
        arx = new ModelHandler::ARX<double>(0,k);
        LS = new OptimizationHandler::LeastSquare<double>(arx);
        LS->Optimize(Input,Output);

        //arx->setModelCoef(ModelCoef);
        arx->setInitialOutputValue(Output(0,0));
        LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
        for(unsigned i = 2; i < counter; ++i)
            estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));

        error = Output - estOutput;
        uint16_t N = error.getNumberOfColumns();
        //std::cout << (error*(~error)) << "\n";
        double Ctemp = ((error*(~error))(0,0))/N;
        double AIC4_temp = N*log(Ctemp)+4*(k+1);
        double BIC_temp = N*log(Ctemp)+(k+1)*log(N);

        if((AIC4_temp < AIC4  && BIC_temp < BIC) && Ctemp < C){
            AIC4 = AIC4_temp; BIC = BIC_temp; C = Ctemp;
            ModelCoef = arx->getModelCoef();
        }
    }

    return ModelCoef;
}

LinAlg::Matrix<double> findBestARModelMQE(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::ExtendedLeastSquare<double> *ELS;

    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 1; k < 3; ++k){
        arx = new ModelHandler::ARX<double>(0,k);
        ELS = new OptimizationHandler::ExtendedLeastSquare<double>(arx);
        ELS->Optimize(Input,Output);

        //arx->setModelCoef(~ModelCoef);
        arx->setInitialOutputValue(Output(0,0));
        LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
        for(unsigned i = 2; i < counter; ++i)
            estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));

        error = Output - estOutput;
        uint16_t N = error.getNumberOfColumns();
        //std::cout << (error*(~error)) << "\n";
        double Ctemp = ((error*(~error))(0,0))/N;
        double AIC4_temp = N*log(Ctemp)+4*(k+1);
        double BIC_temp = N*log(Ctemp)+(k+1)*log(N);

        if((AIC4_temp < AIC4  && BIC_temp < BIC) && Ctemp < C){
            AIC4 = AIC4_temp; BIC = BIC_temp; C = Ctemp;
            ModelCoef = arx->getModelCoef();
        }
    }

    return ModelCoef;
}

LinAlg::Matrix<double> findBestARXModelMQ(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::LeastSquare<double> *LS;

    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 1; k < 3; ++k){
        arx = new ModelHandler::ARX<double>(k,k);
        LS = new OptimizationHandler::LeastSquare<double>(arx);
        LS->Optimize(Input,Output);

        //arx->setModelCoef(ModelCoef);
        arx->setInitialOutputValue(Output(0,0));
        LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
        for(unsigned i = 2; i < counter; ++i)
            estOutput(0,i) = int(arx->sim(Input(0,i-1),Output(0,i-2)));

        error = Output - estOutput;
        uint16_t N = error.getNumberOfColumns();
        //std::cout << (error*(~error)) << "\n";
        double Ctemp = ((error*(~error))(0,0))/N;
        double AIC4_temp = N*log(Ctemp)+4*(k+1);
        double BIC_temp = N*log(Ctemp)+(k+1)*log(N);

        if((AIC4_temp < AIC4  && BIC_temp < BIC) && Ctemp < C){
            AIC4 = AIC4_temp; BIC = BIC_temp; C = Ctemp;
            ModelCoef = arx->getModelCoef();
        }
    }

    return ModelCoef;
}

LinAlg::Matrix<double> calculaModeloARMQ(std::string matrix){
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrix;
    LinAlg::Matrix<double> data;

    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = LinAlg::Zeros<double>(1,counter-1);

    LinAlg::Matrix<double> ModelCoef = findBestARModelMQ(Input, Output);
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
    return data;
}

LinAlg::Matrix<double> calculaModeloARMQE(std::string matrix){
    LinAlg::Matrix<double> data;
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrix;
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = LinAlg::Zeros<double>(1,counter-1);

    LinAlg::Matrix<double> ModelCoef = findBestARModelMQE(Input, Output);
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
    return data;
}

LinAlg::Matrix<double> calculaModeloARXMQ(std::string matrixIn, std::string matrixOut, double Isolamento, uint8_t atrasoEnvolvido){
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrixOut;
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = matrixIn;
    Input = Input(0,from(0)-->counter-2);

    LinAlg::Matrix<double> ModelCoef = findBestARXModelMQ(Input, Output);
    arx = new ModelHandler::ARX<double>(ModelCoef.getNumberOfRows()/2,ModelCoef.getNumberOfRows()/2);
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 2; i < counter; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));

    double temp = estOutput(0,counter-1), inputTemp = 0;
    LinAlg::Matrix<double> predictOutput(1,7+atrasoEnvolvido);
    for(unsigned i = 0; i < atrasoEnvolvido; ++i){
        inputTemp = Input(0,counter-2);
        temp = arx->sim(inputTemp,temp);
        predictOutput(0,i) = (int)temp;
    }

    for(unsigned i = 0; i < 10; ++i){
        temp = arx->sim(Isolamento,temp);
        predictOutput(0,i+atrasoEnvolvido) = (int)temp;
    }
    LinAlg::Matrix<double> data = (~(estOutput(0,from(1)-->counter-1)|predictOutput))|((~(Output(0,from(0)-->counter-2)))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data << std::endl;
    std::cout << arx->print() << std::endl;
    return data;
}

std::string* pegarDados(QString nome)
{
    //QString filename = "D:\\Projetos\\ModeloAndre\\data\\";
    QString filename = "/home/travis/build/C4NESub9/ModeloAndre/data/";
    QFile file(filename+nome+".csv");
    file.open(QIODevice::ReadOnly);

    std::string *matrix = new std::string[2];
    QString date;
    uint16_t counter = 0;
    while (!file.atEnd()) {
        QByteArray line = file.readLine();
        date += line.split(',')[0] + "\n";
        matrix[0] = date.toStdString();

        QString str = line.split(',')[1];

         if(counter > 0){
             QString temp = str;//.split(',')[1];
             if(temp == "+")
                 break;
             matrix[1] += temp.toStdString()+",";
         }
        counter++;
    }
    file.close();

    matrix[1].erase(matrix[1].size()-1);

    return matrix;
}

void salvarDados(QString nome, QString diasParaGrafico, LinAlg::Matrix<double> data)
{
    QDate Date = QDate::fromString(diasParaGrafico.split('\n')[1],"yyyy-MM-dd");


    //QString filename = "D:\\Projetos\\ModeloAndre\\dataAn\\";
    QString filename = "/home/travis/build/C4NESub9/ModeloAndre/dataAn/";
    QFile file(filename+nome+"P.csv");
    file.open(QIODevice::WriteOnly | QIODevice::Truncate );

    QTextStream stream(&file);
    stream << "Data,Saida_Estimada,Saida,Erro\n";
    for(int i = 0; i < data.getNumberOfRows(); ++i){
        stream << Date.toString("yyyy-MM-dd") << ',';
        for(int j = 0; j < data.getNumberOfColumns();++j){
            QString temp;
            if(i > 30 && data(i,j) == 0)
                temp = "+";
            else
                temp = QString::number(data(i,j));

            if(j < data.getNumberOfColumns()-1)
                stream << temp << ',';
            else
                stream << temp;
        }

        stream << '\n';
        Date = Date.addDays(1);
    }

    file.close();
}

int main()
{
    QString estados[27] = {"AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An",      "RiO_An","AiC_An","AiM_An","RiR_An","PiA_An","AiP_An","TiO_An",    "MiG_An","EiS_An","RiJ_An","SiP_An",     "PiR_An","SiC_An","RiS_An",        "MiS_An","MiT_An","GiO_An","DiF_An"};
    QString tipoDados[2] = {"CA","OA"};
    QString isolamentoEstados = "GDM";

    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < 27; ++j){
            std::string *Input = pegarDados(isolamentoEstados + estados[j]);
            std::string *Output = pegarDados(tipoDados[i] + estados[j]);
            //calculaModeloARMQ(matrix);
            //calculaModeloARMQE(matrix);
            LinAlg::Matrix<double> data = calculaModeloARXMQ(Input[1], Output[1], 0, 10);
            salvarDados(tipoDados[i] + estados[j], Output[0].c_str(), data);
            LinAlg::Matrix<double> data2 = calculaModeloARXMQ(Input[1], Output[1], -50, 10);
            salvarDados(tipoDados[i] + estados[j] + "50", Output[0].c_str(), data2);
            LinAlg::Matrix<double> data3 = calculaModeloARXMQ(Input[1], Output[1], -75, 10);
            salvarDados(tipoDados[i] + estados[j] + "75", Output[0].c_str(), data3);
        }

    return 0;
}

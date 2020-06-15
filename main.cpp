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

    for(uint8_t k = 2; k < 3; ++k){
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

LinAlg::Matrix<double> findBestARModelMQE(LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::ExtendedLeastSquare<double> *ELS;
    LinAlg::Matrix<double> Input = LinAlg::Zeros<double>(Output.getNumberOfRows(),Output.getNumberOfRows());
    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 2; k < 3; ++k){
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

    for(uint8_t k = 2; k < 3; ++k){
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

LinAlg::Matrix<double> findBestARXModelMQE(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::ExtendedLeastSquare<double> *ELS;

    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 2; k < 3; ++k){
        arx = new ModelHandler::ARX<double>(k,k);
        ELS = new OptimizationHandler::ExtendedLeastSquare<double>(arx);
        ELS->Optimize(Input,Output);

        //arx->setModelCoef(ModelCoef);
        arx->setInitialOutputValue(Output(0,0));
        LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
        for(unsigned i = 1+k; i < counter; ++i)
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
        estOutput(0,i) = int(arx->sim(Input(0,i-1),Output(0,i-2)));

    double temp = estOutput(0,counter-1);
    LinAlg::Matrix<double> predictOutput(1,7);
    for(unsigned i = 0; i < 7; ++i){
        temp = arx->sim(0,temp);
        predictOutput(0,i) = (int)temp;
    }
    data = ((~(Output(0,from(0)-->counter-2)))|(~(estOutput(0,from(1)-->counter-1)|predictOutput))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data << std::endl;
    //std::cout << arx->print() << std::endl;
    return data;
}

LinAlg::Matrix<double> calculaModeloARMQE(std::string matrix, double Isolamento, double fator=0.2){
    LinAlg::Matrix<double> data;
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrix;
    LinAlg::Matrix<double> complementar = Output(0,from(0)-->(Output.getNumberOfColumns()/12-1));
    Output = Output(0,from(Output.getNumberOfColumns()/12)-->Output.getNumberOfColumns());
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = LinAlg::Zeros<double>(1,counter-1);

    LinAlg::Matrix<double> ModelCoef = findBestARModelMQE(Output);
    arx = new ModelHandler::ARX<double>(0,ModelCoef.getNumberOfRows());
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 2; i < counter; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));

    double temp = estOutput(0,counter-1);
    double OutputFactor = estOutput(0,counter-1)-estOutput(0,counter-2);
    LinAlg::Matrix<double> predictOutput(1,15);
    for(unsigned i = 0; i < 15; ++i){
        temp = arx->sim(0,temp - OutputFactor*Isolamento*fator);
        predictOutput(0,i) = (int)temp;
    }
    //LinAlg::Matrix<double> tempMatrix = (complementar|estOutput(0,from(1)-->counter-1));
    //tempMatrix = (complementar|Output(0,from(0)-->counter-2));
    data = /*((~(Output(0,from(0)-->counter-2)))|*/((~(complementar|estOutput(0,from(1)-->counter-1)|predictOutput))|(~((complementar|Output(0,from(0)-->counter-2))-(complementar|estOutput(0,from(1)-->counter-1)))));
    //std::cout << data << std::endl;
    //std::cout << arx->print() << std::endl;
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
        estOutput(0,i) = int(arx->sim(Input(0,i-1),Output(0,i-2)));

    double temp = estOutput(0,counter-1), inputTemp = 0;
    LinAlg::Matrix<double> predictOutput(1,15+atrasoEnvolvido);
    for(unsigned i = 0; i < atrasoEnvolvido; ++i){
        inputTemp = Input(0,counter-2);
        temp = arx->sim(inputTemp,temp);
        predictOutput(0,i) = (int)temp;
    }

    if(ModelCoef(ModelCoef.getNumberOfRows()/2,0) < 0)
        Isolamento = -Isolamento;
    for(unsigned i = 0; i < 15; ++i){
        temp = arx->sim(Isolamento,temp);
        predictOutput(0,i+atrasoEnvolvido) = (int)temp;
    }
    LinAlg::Matrix<double> data = (~(estOutput(0,from(1)-->counter-1)|predictOutput))|((~(Output(0,from(0)-->counter-2)))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data << std::endl;
    //std::cout << arx->print() << std::endl;
    return data;
}

LinAlg::Matrix<double> calculaModeloARXMQE(std::string matrixIn, std::string matrixOut, double Isolamento, uint8_t atrasoEnvolvido){
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrixOut;
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = matrixIn;
    Input = Input(0,from(0)-->counter-2);

    LinAlg::Matrix<double> ModelCoef = findBestARXModelMQE(Input, Output);
    arx = new ModelHandler::ARX<double>(ModelCoef.getNumberOfRows()/2,ModelCoef.getNumberOfRows()/2);
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 1+ModelCoef.getNumberOfRows()/2; i < counter; ++i)
        estOutput(0,i) = int(arx->sim(Input(0,i-1),Output(0,i-2)));

    double temp = estOutput(0,counter-1), inputTemp = 0;
    LinAlg::Matrix<double> predictOutput(1,15+atrasoEnvolvido);
    for(unsigned i = 0; i < atrasoEnvolvido; ++i){
        inputTemp = Input(0,counter-2);
        temp = arx->sim(inputTemp,temp);
        predictOutput(0,i) = (int)temp;
    }

    for(unsigned i = 0; i < 15; ++i){
        temp = arx->sim(Isolamento,temp);
        predictOutput(0,i+atrasoEnvolvido) = (int)temp;
    }
    //std::cout << ((~(Output(0,from(0)-->counter-2)))|(~estOutput(0,from(1)-->counter-1)));
    LinAlg::Matrix<double> data = (~(estOutput(0,from(1)-->counter-1)|predictOutput))|((~(Output(0,from(0)-->counter-2)))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
    //std::cout << data << std::endl;
    //std::cout << arx->print() << std::endl;
    return data;
}

LinAlg::Matrix<double> predicao(std::string matrixIn, std::string matrixOut, double endMinusDays){
    ModelHandler::ARX<double> *arx;
    LinAlg::Matrix<double> Output = matrixOut;
    LinAlg::Matrix<double> complementar = Output(0,from(0)-->(Output.getNumberOfColumns()/12-1));
    Output = Output(0,from(Output.getNumberOfColumns()/12)-->Output.getNumberOfColumns());
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = matrixIn;
    Input = Input(0,from(0)-->counter-2);

    double N = counter - endMinusDays - 1;

//    LinAlg::Matrix<double> ModelCoef = findBestARXModelMQ(Input, Output);
    LinAlg::Matrix<double> ModelCoef = findBestARModelMQE(Output);
    //arx = new ModelHandler::ARX<double>(ModelCoef.getNumberOfRows()/2,ModelCoef.getNumberOfRows()/2);
    arx = new ModelHandler::ARX<double>(0,ModelCoef.getNumberOfRows());
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 2; i < N; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));
    for(unsigned i = N; i < counter; ++i){
//        estOutput(0,i) = arx->sim(Input(0,counter-2),estOutput(0,i-1));
        estOutput(0,i) = arx->sim(0,estOutput(0,i-1));
    }

    LinAlg::Matrix<double> data = (~(complementar|estOutput(0,from(1)-->counter-1)))|((~(complementar|Output(0,from(0)-->counter-2)))|(~((complementar|Output(0,from(0)-->counter-2))-(complementar|estOutput(0,from(1)-->counter-1)))));
    //std::cout << data << std::endl;

    double delta = pow(ModelCoef(0,0),2)-4*ModelCoef(1,0),r0,i0 = 0,r1,i1 = 0;
    if(delta<0){
        r0 = -ModelCoef(0,0)/2; i0 = sqrt(-delta)/2;
        r1 = -ModelCoef(0,0)/2; i1 = -sqrt(-delta)/2;
    }
    else{
        r0 = -ModelCoef(0,0)/2 +sqrt(delta)/2;
        r1 = -ModelCoef(0,0)/2 -sqrt(delta)/2;
    }

    std::cout << arx->print() << std::endl << "Raiz1: " << r0 << "  " << i0 << std::endl<< "Raiz2: " << r1 << "  " << i1 << std::endl;
    return data;
}

std::string* pegarDados(QString nome)
{
//    QString filename = "D:\\Projetos\\ModeloAndre\\data\\";
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


//    QString filename = "D:\\Projetos\\ModeloAndre\\dataAn\\";
    QString filename = "/home/travis/build/C4NESub9/ModeloAndre/dataAn/";
    QFile file(filename+nome+"P.csv");
    file.open(QIODevice::WriteOnly | QIODevice::Truncate );

    QTextStream stream(&file);
    stream << "Data,Saida_Estimada,Saida,Erro\n";
    for(int i = 0; i < data.getNumberOfRows(); ++i){
        stream << Date.toString("yyyy-MM-dd") << ',';
        for(int j = 0; j < data.getNumberOfColumns();++j){
            QString temp;
            if(i > 40 && data(i,j) == 0)
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
{                                      /* Nordeste*/                                                                         /* Norte*/                                                     /* Suldeste*/                        /* Sul*/                   /* Centro-oeste*/
    QStringList estados = {"BiR_An", "AiL_An","BiA_An","CiE_An","MiA_An","PiB_An","PiE_An","PiI_An","RiN_An","SiE_An","RiO_An","AiC_An","AiM_An","RiR_An","PiA_An","AiP_An","TiO_An","MiG_An","EiS_An","RiJ_An","SiP_An","PiR_An","SiC_An","RiS_An","MiS_An","MiT_An","GiO_An","DiF_An"};
    QString tipoDados[4] = {"CA","OA","CN","ON"};
    QString isolamentoEstados = "GDM";

    for(uint8_t i = 0; i < 4; ++i)
        for(uint8_t j = 0; j < 28; ++j){
            std::string *Input = pegarDados(isolamentoEstados + estados[j].toStdString().c_str());
            std::string *Output = pegarDados(tipoDados[i] + estados[j].toStdString().c_str());
            //calculaModeloARMQ(matrix);
            //calculaModeloARMQE(matrix);

            //LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
            LinAlg::Matrix<double> data1 = calculaModeloARMQE(Output[1],0);
            //std::cout << data << std:endl;
            salvarDados(tipoDados[i] + estados[j], Output[0].c_str(), data1);

            //LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
            LinAlg::Matrix<double> data2 = calculaModeloARMQE(Output[1],0.5);
            salvarDados(tipoDados[i] + estados[j] + "50", Output[0].c_str(), data2);

//            LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
            LinAlg::Matrix<double> data3 = calculaModeloARMQE(Output[1],0.75);
            salvarDados(tipoDados[i] + estados[j] + "75", Output[0].c_str(), data3);
            LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 15);
            salvarDados(tipoDados[i] + estados[j] + "PN", Output[0].c_str(), data4);

//            LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
            LinAlg::Matrix<double> data5 = calculaModeloARMQE(Output[1],0.6);
            salvarDados(tipoDados[i] + estados[j] + "60", Output[0].c_str(), data5);
            std::cout << tipoDados[i].toStdString().c_str() << estados[j].toStdString().c_str() << std::endl;
        }

    QStringList municipios = {"BiASiliaioi","BiAFiiiaidiaitini","BiAVitiriaidioiqiiiti","BiAIiaiuiai","BiAJiaieiri","SiEAiaiaiui","SiEIiaiaiaiai","SiEEitiniii","SiELigirioi","AiLMiciii","AiLAiaiiiaiai","AiLMirici","AiLCiriripi","AiLPilieirioiniiisi","PiERicifi","PiEPitioiiiai","PiECiriaiui","PiBJiaieisiai","PiBCimiiiaiGiaidi","PiBPitisi","RiNNitili","RiNMisioioi","CiEFiriaieiai","CiEJiaieirioiNiriei","CiESibiai","PiITirisini","MiASioiLiii","MiAIipiritiii","MiACixiai"}; //"PiIPicisi","PiISioiRiiiuidioiaioi",/*"PiBSiuiai",*/
    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < municipios.count(); ++j){
            std::string *Input = pegarDados(isolamentoEstados + municipios[j][0]+ municipios[j][1]+ municipios[j][2] + "_An");
            std::string *Output = pegarDados(tipoDados[i] + municipios[j].toStdString().c_str());
            LinAlg::Matrix<double> Out = Output[1];
            //calculaModeloARMQ(matrix);
            //calculaModeloARMQE(matrix);
            //LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
//            LinAlg::Matrix<double> data1 = calculaModeloARMQ(Output[1]);
            LinAlg::Matrix<double> data1 = calculaModeloARMQE(Output[1],0);
            //std::cout << data << std:endl;
            salvarDados(tipoDados[i] + municipios[j], Output[0].c_str(), data1);
//            LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
            LinAlg::Matrix<double> data2 = calculaModeloARMQE(Output[1],0.5);
            salvarDados(tipoDados[i] + municipios[j] + "50", Output[0].c_str(), data2);
//            LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
            LinAlg::Matrix<double> data3 = calculaModeloARMQE(Output[1],0.75);
            salvarDados(tipoDados[i] + municipios[j] + "75", Output[0].c_str(), data3);
            LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 15);
            salvarDados(tipoDados[i] + municipios[j] + "PN", Output[0].c_str(), data4);

//            LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
            LinAlg::Matrix<double> data5 = calculaModeloARMQE(Output[1],0.6);
            salvarDados(tipoDados[i] + municipios[j] + "60", Output[0].c_str(), data5);
            std::cout << municipios[j].toStdString().c_str();
        }

    QStringList RegioesSaude = {"NERNRSCA24004", "NERNRSCA24008", "NERNRSCA24003", "NERNRSCA24006", "NERNRSCA24002", "NERNRSCA24001", "NERNRSCA24005", "NERNRSCA24007","NERNRSOA24004", "NERNRSOA24008", "NERNRSOA24003", "NERNRSOA24006", "NERNRSOA24002", "NERNRSOA24001", "NERNRSOA24005", "NERNRSOA24007","NEPBRSCA25011", "NEPBRSCA25007", "NEPBRSCA25003", "NEPBRSCA25002", "NEPBRSCA25015", "NEPBRSCA25001", "NEPBRSCA25009", "NEPBRSCA25005", "NEPBRSCA25010", "NEPBRSCA25006", "NEPBRSCA25016", "NEPBRSCA25014", "NEPBRSCA25004", "NEPBRSCA25008", "NEPBRSCA25013", "NEPBRSCA25012",/*"NEPBRSOA25011", */"NEPBRSOA25007", "NEPBRSOA25003", "NEPBRSOA25002", "NEPBRSOA25015", "NEPBRSOA25001", "NEPBRSOA25009", "NEPBRSOA25005", "NEPBRSOA25010", "NEPBRSOA25006", "NEPBRSOA25016", "NEPBRSOA25014", /*"NEPBRSOA25004",*/"NEPBRSOA25008", /* "NEPBRSOA25013",*/ "NEPBRSOA25012","NEBARSCA29023", "NEBARSCA29017", "NEBARSCA29001", "NEBARSCA29019", "NEBARSCA29025", "NEBARSCA29015", "NEBARSCA29026", "NEBARSCA29012", "NEBARSCA29022", "NEBARSCA29006", "NEBARSCA29010", "NEBARSCA29028", "NEBARSCA29011", "NEBARSCA29003", "NEBARSCA29009", "NEBARSCA29002", "NEBARSCA29008", "NEBARSCA29018", "NEBARSCA29021", "NEBARSCA29005", "NEBARSCA29007", "NEBARSCA29014", "NEBARSCA29027", "NEBARSCA29004", "NEBARSCA29016", "NEBARSCA29024", "NEBARSCA29020", "NEBARSCA29013","NEBARSOA29023", /*"NEBARSOA29017",*/ "NEBARSOA29001", "NEBARSOA29019", "NEBARSOA29025", "NEBARSOA29015", "NEBARSOA29026", "NEBARSOA29012", "NEBARSOA29022", "NEBARSOA29006", "NEBARSOA29010", "NEBARSOA29028", "NEBARSOA29011", "NEBARSOA29003", "NEBARSOA29009", "NEBARSOA29002", /*"NEBARSOA29008",*/ "NEBARSOA29018", /*"NEBARSOA29021",*/ "NEBARSOA29005", /*"NEBARSOA29007",*/ "NEBARSOA29014", "NEBARSOA29027", "NEBARSOA29004", "NEBARSOA29016", "NEBARSOA29024", "NEBARSOA29020", "NEBARSOA29013","NESERSCA28007", "NESERSCA28001", "NESERSCA28002", "NESERSCA28003", "NESERSCA28005", "NESERSCA28006", "NESERSCA28004","NESERSOA28007", "NESERSOA28001", "NESERSOA28002", "NESERSOA28003", "NESERSOA28005", "NESERSOA28006", "NESERSOA28004","NEALRSCA27010", "NEALRSCA27005", "NEALRSCA27007", "NEALRSCA27004", "NEALRSCA27001", "NEALRSCA27008", "NEALRSCA27003", "NEALRSCA27009", "NEALRSCA27006", "NEALRSCA27002","NEALRSOA27010", "NEALRSOA27005", "NEALRSOA27007", "NEALRSOA27004", "NEALRSOA27001", "NEALRSOA27008", "NEALRSOA27003", "NEALRSOA27009", "NEALRSOA27006", "NEALRSOA27002","NEMARSCA21001", "NEMARSCA21005", "NEMARSCA21006", "NEMARSCA21016", "NEMARSCA21002", "NEMARSCA21007", "NEMARSCA21014", "NEMARSCA21003", "NEMARSCA21019", "NEMARSCA21008", "NEMARSCA21009", "NEMARSCA21011", "NEMARSCA21004", "NEMARSCA21013", "NEMARSCA21018", "NEMARSCA21015", "NEMARSCA21010", "NEMARSCA21012", "NEMARSCA21017","NEMARSOA21001", "NEMARSOA21005", "NEMARSOA21006", "NEMARSOA21016", "NEMARSOA21002", "NEMARSOA21007", "NEMARSOA21014", "NEMARSOA21003", "NEMARSOA21019", "NEMARSOA21008", "NEMARSOA21009", "NEMARSOA21011", "NEMARSOA21004", "NEMARSOA21013", "NEMARSOA21018", "NEMARSOA21015", "NEMARSOA21010", "NEMARSOA21012", "NEMARSOA21017","NEPERSCA26010", "NEPERSCA26001", "NEPERSCA26009", "NEPERSCA26003", "NEPERSCA26008", "NEPERSCA26004", "NEPERSCA26005", "NEPERSCA26007", "NEPERSCA26002", "NEPERSCA26011", "NEPERSCA26012", "NEPERSCA26006","NEPERSOA26010", "NEPERSOA26001", "NEPERSOA26009", "NEPERSOA26003", "NEPERSOA26008", "NEPERSOA26004", "NEPERSOA26005", "NEPERSOA26007", "NEPERSOA26002", "NEPERSOA26011", "NEPERSOA26012", "NEPERSOA26006","NECERSCA23019", "NECERSCA23003", "NECERSCA23012", "NECERSCA23018", "NECERSCA23014", "NECERSCA23011", "NECERSCA23020", "NECERSCA23010", "NECERSCA23006", "NECERSCA23002", "NECERSCA23001", "NECERSCA23007", "NECERSCA23004", "NECERSCA23015", "NECERSCA23017", "NECERSCA23008", "NECERSCA23021", "NECERSCA23016", "NECERSCA23022", "NECERSCA23005", "NECERSCA23013", "NECERSCA23009","NECERSOA23019", "NECERSOA23003", "NECERSOA23012", "NECERSOA23018", "NECERSOA23014", "NECERSOA23011", "NECERSOA23020", "NECERSOA23010", "NECERSOA23006", "NECERSOA23002", "NECERSOA23001", "NECERSOA23007", "NECERSOA23004", "NECERSOA23015", "NECERSOA23017", "NECERSOA23008", "NECERSOA23021", "NECERSOA23016", "NECERSOA23022", "NECERSOA23005", "NECERSOA23013", "NECERSOA23009","NEPIRSCA22004", "NEPIRSCA22009", "NEPIRSCA22002", "NEPIRSCA22006", "NEPIRSCA22010", "NEPIRSCA22007", "NEPIRSCA22003", "NEPIRSCA22008", "NEPIRSCA22011", "NEPIRSCA22001", "NEPIRSCA22005","NEPIRSOA22004", "NEPIRSOA22009", "NEPIRSOA22002", "NEPIRSOA22006", "NEPIRSOA22010", "NEPIRSOA22007", "NEPIRSOA22003", /*"NEPIRSOA22008",*/ "NEPIRSOA22011", "NEPIRSOA22001", "NEPIRSOA22005","NRORSCA11005", "NRORSCA11001", "NRORSCA11006", "NRORSCA11002", "NRORSCA11007", "NRORSCA11004", "NRORSCA11003","NRORSOA11005", "NRORSOA11001", "NRORSOA11006", "NRORSOA11002", "NRORSOA11007", "NRORSOA11004", "NRORSOA11003","NACRSCA12002", "NACRSCA12001", "NACRSCA12003","NACRSOA12002", "NACRSOA12001", "NACRSOA12003","NAMRSCA13008", "NAMRSCA13009", "NAMRSCA13002", "NAMRSCA13003", "NAMRSCA13001", "NAMRSCA13005", "NAMRSCA13006", "NAMRSCA13007", "NAMRSCA13004","NAMRSOA13008", "NAMRSOA13009", "NAMRSOA13002", "NAMRSOA13003", "NAMRSOA13001", "NAMRSOA13005", "NAMRSOA13006", "NAMRSOA13007", "NAMRSOA13004","NRRRSCA14001", "NRRRSCA14002","NRRRSOA14001", "NRRRSOA14002","NPARSCA15011", "NPARSCA15003", "NPARSCA15007", "NPARSCA15013", "NPARSCA15001", "NPARSCA15002", "NPARSCA15012", "NPARSCA15014", "NPARSCA15006", "NPARSCA15009", "NPARSCA15008", "NPARSCA15010", "NPARSCA15004","NPARSOA15011", "NPARSOA15003", "NPARSOA15007", "NPARSOA15013", "NPARSOA15001", "NPARSOA15002", "NPARSOA15012", "NPARSOA15014", "NPARSOA15006", "NPARSOA15009", "NPARSOA15008", "NPARSOA15010", "NPARSOA15004","NAPRSCA16001", "NAPRSCA16002", "NAPRSCA16003","NAPRSOA16001", "NAPRSOA16002", "NAPRSOA16003","NTORSCA17007", "NTORSCA17002", "NTORSCA17005", "NTORSCA17001", "NTORSCA17004", "NTORSCA17003", "NTORSCA17008", "NTORSCA17006","NTORSOA17007", "NTORSOA17002", "NTORSOA17005", "NTORSOA17001", "NTORSOA17004", "NTORSOA17003", "NTORSOA17008", "NTORSOA17006","SPRRSCA41018", "SPRRSCA41002", "SPRRSCA41011", "SPRRSCA41014", "SPRRSCA41017", "SPRRSCA41008", "SPRRSCA41010", "SPRRSCA41015", "SPRRSCA41001", "SPRRSCA41006", "SPRRSCA41016", "SPRRSCA41003", "SPRRSCA41020", "SPRRSCA41012", "SPRRSCA41019", "SPRRSCA41022", "SPRRSCA41005", "SPRRSCA41007", "SPRRSCA41013", "SPRRSCA41021", "SPRRSCA41004", "SPRRSCA41009","SPRRSOA41018", "SPRRSOA41002", "SPRRSOA41011", "SPRRSOA41014", "SPRRSOA41017", "SPRRSOA41008", "SPRRSOA41010", "SPRRSOA41015", "SPRRSOA41001", "SPRRSOA41006", "SPRRSOA41016", "SPRRSOA41003", "SPRRSOA41020", "SPRRSOA41012", "SPRRSOA41019", "SPRRSOA41022", "SPRRSOA41005", "SPRRSOA41007", "SPRRSOA41013", "SPRRSOA41021", "SPRRSOA41004", "SPRRSOA41009","SSCRSCA42008", "SSCRSCA42003", "SSCRSCA42004", "SSCRSCA42002", "SSCRSCA42007", "SSCRSCA42010", "SSCRSCA42001", "SSCRSCA42013", "SSCRSCA42006", "SSCRSCA42011", "SSCRSCA42014", "SSCRSCA42016", "SSCRSCA42009", "SSCRSCA42005", "SSCRSCA42012", "SSCRSCA42015","SSCRSOA42008", "SSCRSOA42003", "SSCRSOA42004", "SSCRSOA42002", "SSCRSOA42007", "SSCRSOA42010", "SSCRSOA42001", "SSCRSOA42013", "SSCRSOA42006", "SSCRSOA42011", "SSCRSOA42014", "SSCRSOA42016", "SSCRSOA42009", "SSCRSOA42005", "SSCRSOA42012", "SSCRSOA42015","SRSRSCA43018", "SRSRSCA43001", "SRSRSCA43013", "SRSRSCA43014", "SRSRSCA43003", "SRSRSCA43015", "SRSRSCA43010", "SRSRSCA43029", "SRSRSCA43026", "SRSRSCA43007", "SRSRSCA43016", "SRSRSCA43004", "SRSRSCA43009", "SRSRSCA43021", "SRSRSCA43019", "SRSRSCA43022", "SRSRSCA43005", "SRSRSCA43008", "SRSRSCA43025", "SRSRSCA43020", "SRSRSCA43024", "SRSRSCA43030", "SRSRSCA43011", "SRSRSCA43027", "SRSRSCA43017", "SRSRSCA43006", "SRSRSCA43028", "SRSRSCA43023", "SRSRSCA43012", "SRSRSCA43002","SRSRSOA43018", "SRSRSOA43001", "SRSRSOA43013", "SRSRSOA43014", "SRSRSOA43003", "SRSRSOA43015", "SRSRSOA43010", "SRSRSOA43029", "SRSRSOA43026", "SRSRSOA43007", "SRSRSOA43016", "SRSRSOA43004", "SRSRSOA43009", "SRSRSOA43021", "SRSRSOA43019", "SRSRSOA43022", "SRSRSOA43005", "SRSRSOA43008", "SRSRSOA43025", "SRSRSOA43020", "SRSRSOA43024", "SRSRSOA43030", "SRSRSOA43011", "SRSRSOA43027", "SRSRSOA43017", "SRSRSOA43006", "SRSRSOA43028", "SRSRSOA43023", "SRSRSOA43012", "SRSRSOA43002","SEMGRSCA31074", "SEMGRSCA31024", "SEMGRSCA31059", "SEMGRSCA31037", "SEMGRSCA31072", "SEMGRSCA31062", "SEMGRSCA31068", "SEMGRSCA31040", "SEMGRSCA31041", "SEMGRSCA31001", "SEMGRSCA31013", "SEMGRSCA31094", "SEMGRSCA31036", "SEMGRSCA31092", "SEMGRSCA31060", "SEMGRSCA31095", "SEMGRSCA31006", "SEMGRSCA31090", "SEMGRSCA31035", "SEMGRSCA31064", "SEMGRSCA31075", "SEMGRSCA31082", "SEMGRSCA31070", "SEMGRSCA31002", "SEMGRSCA31087", "SEMGRSCA31058", "SEMGRSCA31044", "SEMGRSCA31008", "SEMGRSCA31030", "SEMGRSCA31021", "SEMGRSCA31045", "SEMGRSCA31015", "SEMGRSCA31023", "SEMGRSCA31097", "SEMGRSCA31016", "SEMGRSCA31017", "SEMGRSCA31047", "SEMGRSCA31011", "SEMGRSCA31083", "SEMGRSCA31028", "SEMGRSCA31034", "SEMGRSCA31007", "SEMGRSCA31049", "SEMGRSCA31003", "SEMGRSCA31019", "SEMGRSCA31055", "SEMGRSCA31073", "SEMGRSCA31042", "SEMGRSCA31061", "SEMGRSCA31010", "SEMGRSCA31089", "SEMGRSCA31027", "SEMGRSCA31091", "SEMGRSCA31051", "SEMGRSCA31093", "SEMGRSCA31067", "SEMGRSCA31079", "SEMGRSCA31026", "SEMGRSCA31066", "SEMGRSCA31088", "SEMGRSCA31086", "SEMGRSCA31004", "SEMGRSCA31048", "SEMGRSCA31065", "SEMGRSCA31053", "SEMGRSCA31025", "SEMGRSCA31078", "SEMGRSCA31018", "SEMGRSCA31050", "SEMGRSCA31085", "SEMGRSCA31038", "SEMGRSCA31020", "SEMGRSCA31012", "SEMGRSCA31052", "SEMGRSCA31096", "SEMGRSCA31071", "SEMGRSCA31057", "SEMGRSCA31032", "SEMGRSCA31022", "SEMGRSCA31031", "SEMGRSCA31009", "SEMGRSCA31077", "SEMGRSCA31099", "SEMGRSCA31084", "SEMGRSCA31076", "SEMGRSCA31098", "SEMGRSCA31046", "SEMGRSCA31080", "SEMGRSCA31081","SEMGRSOA31074", "SEMGRSOA31024", "SEMGRSOA31059", "SEMGRSOA31037", "SEMGRSOA31072", "SEMGRSOA31062", "SEMGRSOA31068", "SEMGRSOA31040", "SEMGRSOA31041", "SEMGRSOA31001", "SEMGRSOA31013", "SEMGRSOA31094", "SEMGRSOA31036", "SEMGRSOA31092", "SEMGRSOA31060", "SEMGRSOA31095", "SEMGRSOA31006", "SEMGRSOA31090", "SEMGRSOA31035", "SEMGRSOA31064", "SEMGRSOA31075", "SEMGRSOA31082", "SEMGRSOA31070", "SEMGRSOA31002", "SEMGRSOA31087", "SEMGRSOA31058", "SEMGRSOA31044", "SEMGRSOA31008", "SEMGRSOA31030", "SEMGRSOA31021", "SEMGRSOA31045", "SEMGRSOA31015", "SEMGRSOA31023", "SEMGRSOA31097", "SEMGRSOA31016", "SEMGRSOA31017", "SEMGRSOA31047", "SEMGRSOA31011", "SEMGRSOA31083", "SEMGRSOA31028", "SEMGRSOA31034", "SEMGRSOA31007", "SEMGRSOA31049", "SEMGRSOA31003", "SEMGRSOA31019", "SEMGRSOA31055", "SEMGRSOA31073", "SEMGRSOA31042", "SEMGRSOA31061", "SEMGRSOA31010", "SEMGRSOA31089", "SEMGRSOA31027", "SEMGRSOA31091", "SEMGRSOA31051", "SEMGRSOA31093", "SEMGRSOA31067", "SEMGRSOA31079", "SEMGRSOA31026", "SEMGRSOA31066", "SEMGRSOA31088", "SEMGRSOA31086", "SEMGRSOA31004", "SEMGRSOA31048", "SEMGRSOA31065", "SEMGRSOA31053", "SEMGRSOA31025", "SEMGRSOA31078", "SEMGRSOA31018", "SEMGRSOA31050", "SEMGRSOA31085", "SEMGRSOA31038", "SEMGRSOA31020", "SEMGRSOA31012", "SEMGRSOA31052", "SEMGRSOA31096", "SEMGRSOA31071", "SEMGRSOA31057", "SEMGRSOA31032", "SEMGRSOA31022", "SEMGRSOA31031", "SEMGRSOA31009", "SEMGRSOA31077", "SEMGRSOA31099", "SEMGRSOA31084", "SEMGRSOA31076", "SEMGRSOA31098", "SEMGRSOA31046", "SEMGRSOA31080", "SEMGRSOA31081","SEESRSCA32002", "SEESRSCA32001", "SEESRSCA32003", "SEESRSCA32004","SEESRSOA32002", "SEESRSOA32001", "SEESRSOA32003", "SEESRSOA32004","SERJRSCA33001", "SERJRSCA33007", "SERJRSCA33002", "SERJRSCA33003", "SERJRSCA33004", "SERJRSCA33005", "SERJRSCA33009", "SERJRSCA33008", "SERJRSCA33006","SERJRSOA33001", "SERJRSOA33007", "SERJRSOA33002", "SERJRSOA33003", "SERJRSOA33004", "SERJRSOA33005", "SERJRSOA33009", "SERJRSOA33008", "SERJRSOA33006","SESPRSCA35091", "SESPRSCA35156", "SESPRSCA35142", "SESPRSCA35074", "SESPRSCA35061", "SESPRSCA35103", "SESPRSCA35062", "SESPRSCA35161", "SESPRSCA35112", "SESPRSCA35051", "SESPRSCA35133", "SESPRSCA35023", "SESPRSCA35163", "SESPRSCA35157", "SESPRSCA35093", "SESPRSCA35072", "SESPRSCA35031", "SESPRSCA35104", "SESPRSCA35022", "SESPRSCA35063", "SESPRSCA35172", "SESPRSCA35153", "SESPRSCA35162", "SESPRSCA35021", "SESPRSCA35083", "SESPRSCA35101", "SESPRSCA35151", "SESPRSCA35011", "SESPRSCA35092", "SESPRSCA35071", "SESPRSCA35155", "SESPRSCA35064", "SESPRSCA35121", "SESPRSCA35131", "SESPRSCA35014", "SESPRSCA35095", "SESPRSCA35052", "SESPRSCA35094", "SESPRSCA35041", "SESPRSCA35032", "SESPRSCA35073", "SESPRSCA35171", "SESPRSCA35143", "SESPRSCA35065", "SESPRSCA35012", "SESPRSCA35114", "SESPRSCA35174", "SESPRSCA35033", "SESPRSCA35173", "SESPRSCA35102", "SESPRSCA35013", "SESPRSCA35132", "SESPRSCA35081", "SESPRSCA35034", "SESPRSCA35015", "SESPRSCA35111", "SESPRSCA35154", "SESPRSCA35115", "SESPRSCA35113", "SESPRSCA35082", "SESPRSCA35141", "SESPRSCA35152", "SESPRSCA35016","SESPRSOA35091", "SESPRSOA35156", "SESPRSOA35142", "SESPRSOA35074", "SESPRSOA35061", "SESPRSOA35103", "SESPRSOA35062", "SESPRSOA35161", "SESPRSOA35112", "SESPRSOA35051", "SESPRSOA35133", "SESPRSOA35023", "SESPRSOA35163", "SESPRSOA35157", "SESPRSOA35093", "SESPRSOA35072", "SESPRSOA35031", "SESPRSOA35104", "SESPRSOA35022", "SESPRSOA35063", "SESPRSOA35172", "SESPRSOA35153", "SESPRSOA35162", "SESPRSOA35021", "SESPRSOA35083", "SESPRSOA35101", "SESPRSOA35151", "SESPRSOA35011", "SESPRSOA35092", "SESPRSOA35071", "SESPRSOA35155", "SESPRSOA35064", "SESPRSOA35121", "SESPRSOA35131", "SESPRSOA35014", "SESPRSOA35095", "SESPRSOA35052", "SESPRSOA35094", "SESPRSOA35041", "SESPRSOA35032", "SESPRSOA35073", "SESPRSOA35171", "SESPRSOA35143", "SESPRSOA35065", "SESPRSOA35012", "SESPRSOA35114", "SESPRSOA35174", "SESPRSOA35033", "SESPRSOA35173", "SESPRSOA35102", "SESPRSOA35013", "SESPRSOA35132", "SESPRSOA35081", "SESPRSOA35034", "SESPRSOA35015", "SESPRSOA35111", "SESPRSOA35154", "SESPRSOA35115", "SESPRSOA35113", "SESPRSOA35082", "SESPRSOA35141", "SESPRSOA35152", "SESPRSOA35016","COMSRSCA50004", "COMSRSCA50001", "COMSRSCA50003", "COMSRSCA50002","COMSRSOA50004", "COMSRSOA50001", "COMSRSOA50003", "COMSRSOA50002","COGORSCA52001", "COGORSCA52011", "COGORSCA52015", "COGORSCA52010", "COGORSCA52003", "COGORSCA52004", "COGORSCA52017", "COGORSCA52014", "COGORSCA52012", "COGORSCA52009", "COGORSCA52005", "COGORSCA52002", "COGORSCA52016", "COGORSCA52018", "COGORSCA52006", "COGORSCA52013", "COGORSCA52008", "COGORSCA52007","COGORSOA52001", "COGORSOA52011", "COGORSOA52015", "COGORSOA52010", "COGORSOA52003", "COGORSOA52004", "COGORSOA52017", "COGORSOA52014", "COGORSOA52012", "COGORSOA52009", "COGORSOA52005", "COGORSOA52002", "COGORSOA52016", "COGORSOA52018", "COGORSOA52006", "COGORSOA52013", "COGORSOA52008", "COGORSOA52007","COMTRSCA51002", "COMTRSCA51006", "COMTRSCA51001", "COMTRSCA51013", "COMTRSCA51009", "COMTRSCA51004", "COMTRSCA51011", "COMTRSCA51007", "COMTRSCA51008", "COMTRSCA51005", "COMTRSCA51012", "COMTRSCA51003", "COMTRSCA51014", "COMTRSCA51010", "COMTRSCA51015", "COMTRSCA51016","COMTRSOA51002", "COMTRSOA51006", "COMTRSOA51001", "COMTRSOA51013", "COMTRSOA51009", "COMTRSOA51004", "COMTRSOA51011", "COMTRSOA51007", "COMTRSOA51008", "COMTRSOA51005", "COMTRSOA51012", "COMTRSOA51003", "COMTRSOA51014", "COMTRSOA51010", "COMTRSOA51015", "COMTRSOA51016"};
    //QStringList RegioesSaude = {"NERNRSCA24004", "NERNRSCA24008", "NERNRSCA24003", "NERNRSCA24006", "NERNRSCA24002", "NERNRSCA24001", "NERNRSCA24005", "NERNRSCA24007","NERNRSOA24004", "NERNRSOA24008", "NERNRSOA24003", "NERNRSOA24006", "NERNRSOA24002", "NERNRSOA24001", "NERNRSOA24005", "NERNRSOA24007","NEPBRSCA25011", "NEPBRSCA25007", "NEPBRSCA25003", "NEPBRSCA25002", "NEPBRSCA25015", "NEPBRSCA25001", "NEPBRSCA25009", "NEPBRSCA25005", "NEPBRSCA25010", "NEPBRSCA25006", "NEPBRSCA25016", "NEPBRSCA25014", "NEPBRSCA25004", "NEPBRSCA25008", "NEPBRSCA25013", "NEPBRSCA25012","NEPBRSOA25011", "NEPBRSOA25007", "NEPBRSOA25003", "NEPBRSOA25002", "NEPBRSOA25015", "NEPBRSOA25001", "NEPBRSOA25009", "NEPBRSOA25005", "NEPBRSOA25010", "NEPBRSOA25006", "NEPBRSOA25016", "NEPBRSOA25014", "NEPBRSOA25004", "NEPBRSOA25008", "NEPBRSOA25013", "NEPBRSOA25012","NEBARSCA29023", "NEBARSCA29017", "NEBARSCA29001", "NEBARSCA29019", "NEBARSCA29025", "NEBARSCA29003", "NEBARSCA29015", "NEBARSCA29026", "NEBARSCA29012", "NEBARSCA29022", "NEBARSCA29006", "NEBARSCA29010", "NEBARSCA29028", "NEBARSCA29011", "NEBARSCA29024", "NEBARSCA29002", "NEBARSCA29009", "NEBARSCA29008", "NEBARSCA29018", "NEBARSCA29021", "NEBARSCA29013", "NEBARSCA29005", "NEBARSCA29007", "NEBARSCA29014", "NEBARSCA29027", "NEBARSCA29004", "NEBARSCA29016", "NEBARSCA29020","NEBARSOA29023", "NEBARSOA29017", "NEBARSOA29001", "NEBARSOA29019", "NEBARSOA29025", "NEBARSOA29003", "NEBARSOA29015", "NEBARSOA29026", "NEBARSOA29012", "NEBARSOA29022", "NEBARSOA29006", "NEBARSOA29010", "NEBARSOA29028", "NEBARSOA29011", "NEBARSOA29024", "NEBARSOA29002", "NEBARSOA29009", "NEBARSOA29008", "NEBARSOA29018", "NEBARSOA29021", "NEBARSOA29013", "NEBARSOA29005", "NEBARSOA29007", "NEBARSOA29014", "NEBARSOA29027", "NEBARSOA29004", "NEBARSOA29016", "NEBARSOA29020","NESERSCA28007", "NESERSCA28001", "NESERSCA28002", "NESERSCA28003", "NESERSCA28005", "NESERSCA28006", "NESERSCA28004","NESERSOA28007", "NESERSOA28001", "NESERSOA28002", "NESERSOA28003", "NESERSOA28005", "NESERSOA28006", "NESERSOA28004","NEALRSCA27010", "NEALRSCA27005", "NEALRSCA27007", "NEALRSCA27004", "NEALRSCA27001", "NEALRSCA27008", "NEALRSCA27003", "NEALRSCA27009", "NEALRSCA27006", "NEALRSCA27002","NEALRSOA27010", "NEALRSOA27005", "NEALRSOA27007", "NEALRSOA27004", "NEALRSOA27001", "NEALRSOA27008", "NEALRSOA27003", "NEALRSOA27009", "NEALRSOA27006", "NEALRSOA27002","NEMARSCA21001", "NEMARSCA21005", "NEMARSCA21006", "NEMARSCA21016", "NEMARSCA21002", "NEMARSCA21007", "NEMARSCA21014", "NEMARSCA21003", "NEMARSCA21019", "NEMARSCA21008", "NEMARSCA21009", "NEMARSCA21011", "NEMARSCA21004", "NEMARSCA21013", "NEMARSCA21018", "NEMARSCA21015", "NEMARSCA21010", "NEMARSCA21012", "NEMARSCA21017","NEMARSOA21001", "NEMARSOA21005", "NEMARSOA21006", "NEMARSOA21016", "NEMARSOA21002", "NEMARSOA21007", "NEMARSOA21014", "NEMARSOA21003", "NEMARSOA21019", "NEMARSOA21008", "NEMARSOA21009", "NEMARSOA21011", "NEMARSOA21004", "NEMARSOA21013", "NEMARSOA21018", "NEMARSOA21015", "NEMARSOA21010", "NEMARSOA21012", "NEMARSOA21017","NEPERSCA26010", "NEPERSCA26001", "NEPERSCA26009", "NEPERSCA26003", "NEPERSCA26008", "NEPERSCA26004", "NEPERSCA26005", "NEPERSCA26007", "NEPERSCA26002", "NEPERSCA26011", "NEPERSCA26012", "NEPERSCA26006","NEPERSOA26010", "NEPERSOA26001", "NEPERSOA26009", "NEPERSOA26003", "NEPERSOA26008", "NEPERSOA26004", "NEPERSOA26005", "NEPERSOA26007", "NEPERSOA26002", "NEPERSOA26011", "NEPERSOA26012", "NEPERSOA26006","NECERSCA23019", "NECERSCA23003", "NECERSCA23012", "NECERSCA23018", "NECERSCA23014", "NECERSCA23011", "NECERSCA23020", "NECERSCA23010", "NECERSCA23006", "NECERSCA23002", "NECERSCA23001", "NECERSCA23007", "NECERSCA23004", "NECERSCA23015", "NECERSCA23017", "NECERSCA23008", "NECERSCA23021", "NECERSCA23016", "NECERSCA23022", "NECERSCA23005", "NECERSCA23013", "NECERSCA23009","NECERSOA23019", "NECERSOA23003", "NECERSOA23012", "NECERSOA23018", "NECERSOA23014", "NECERSOA23011", "NECERSOA23020", "NECERSOA23010", "NECERSOA23006", "NECERSOA23002", "NECERSOA23001", "NECERSOA23007", "NECERSOA23004", "NECERSOA23015", "NECERSOA23017", "NECERSOA23008", "NECERSOA23021", "NECERSOA23016", "NECERSOA23022", "NECERSOA23005", "NECERSOA23013", "NECERSOA23009","NEPIRSCA22009", "NEPIRSCA22004", "NEPIRSCA22002", "NEPIRSCA22006", "NEPIRSCA22010", "NEPIRSCA22007", "NEPIRSCA22003", "NEPIRSCA22008", "NEPIRSCA22011", "NEPIRSCA22001", "NEPIRSCA22005","NEPIRSOA22009", "NEPIRSOA22004", "NEPIRSOA22002", "NEPIRSOA22006", "NEPIRSOA22010", "NEPIRSOA22007", "NEPIRSOA22003", "NEPIRSOA22008", "NEPIRSOA22011", "NEPIRSOA22001", "NEPIRSOA22005","NRORSCA11005", "NRORSCA11001", "NRORSCA11006", "NRORSCA11002", "NRORSCA11007", "NRORSCA11004", "NRORSCA11003","NRORSOA11005", "NRORSOA11001", "NRORSOA11006", "NRORSOA11002", "NRORSOA11007", "NRORSOA11004", "NRORSOA11003","NACRSCA12002", "NACRSCA12001", "NACRSCA12003","NACRSOA12002", "NACRSOA12001", "NACRSOA12003","NAMRSCA13008", "NAMRSCA13009", "NAMRSCA13002", "NAMRSCA13003", "NAMRSCA13001", "NAMRSCA13005", "NAMRSCA13006", "NAMRSCA13007", "NAMRSCA13004","NAMRSOA13008", "NAMRSOA13009", "NAMRSOA13002", "NAMRSOA13003", "NAMRSOA13001", "NAMRSOA13005", "NAMRSOA13006", "NAMRSOA13007", "NAMRSOA13004","NRRRSCA14001", "NRRRSCA14002","NRRRSOA14001", "NRRRSOA14002","NPARSCA15011", "NPARSCA15003", "NPARSCA15007", "NPARSCA15013", "NPARSCA15001", "NPARSCA15002", "NPARSCA15012", "NPARSCA15014", "NPARSCA15006", "NPARSCA15009", "NPARSCA15008", "NPARSCA15010", "NPARSCA15004","NPARSOA15011", "NPARSOA15003", "NPARSOA15007", "NPARSOA15013", "NPARSOA15001", "NPARSOA15002", "NPARSOA15012", "NPARSOA15014", "NPARSOA15006", "NPARSOA15009", "NPARSOA15008", "NPARSOA15010", "NPARSOA15004","NAPRSCA16001", "NAPRSCA16002", "NAPRSCA16003","NAPRSOA16001", "NAPRSOA16002", "NAPRSOA16003","NTORSCA17007", "NTORSCA17002", "NTORSCA17005", "NTORSCA17001", "NTORSCA17004", "NTORSCA17003", "NTORSCA17008", "NTORSCA17006","NTORSOA17007", "NTORSOA17002", "NTORSOA17005", "NTORSOA17001", "NTORSOA17004", "NTORSOA17003", "NTORSOA17008", "NTORSOA17006","SPRRSCA41018", "SPRRSCA41002", "SPRRSCA41011", "SPRRSCA41014", "SPRRSCA41017", "SPRRSCA41008", "SPRRSCA41010", "SPRRSCA41015", "SPRRSCA41001", "SPRRSCA41006", "SPRRSCA41016", "SPRRSCA41003", "SPRRSCA41020", "SPRRSCA41012", "SPRRSCA41019", "SPRRSCA41022", "SPRRSCA41005", "SPRRSCA41007", "SPRRSCA41013", "SPRRSCA41021", "SPRRSCA41004", "SPRRSCA41009","SPRRSOA41018", "SPRRSOA41002", "SPRRSOA41011", "SPRRSOA41014", "SPRRSOA41017", "SPRRSOA41008", "SPRRSOA41010", "SPRRSOA41015", "SPRRSOA41001", "SPRRSOA41006", "SPRRSOA41016", "SPRRSOA41003", "SPRRSOA41020", "SPRRSOA41012", "SPRRSOA41019", "SPRRSOA41022", "SPRRSOA41005", "SPRRSOA41007", "SPRRSOA41013", "SPRRSOA41021", "SPRRSOA41004", "SPRRSOA41009","SSCRSCA42008", "SSCRSCA42003", "SSCRSCA42004", "SSCRSCA42002", "SSCRSCA42007", "SSCRSCA42010", "SSCRSCA42001", "SSCRSCA42013", "SSCRSCA42006", "SSCRSCA42011", "SSCRSCA42014", "SSCRSCA42016", "SSCRSCA42009", "SSCRSCA42005", "SSCRSCA42012", "SSCRSCA42015","SSCRSOA42008", "SSCRSOA42003", "SSCRSOA42004", "SSCRSOA42002", "SSCRSOA42007", "SSCRSOA42010", "SSCRSOA42001", "SSCRSOA42013", "SSCRSOA42006", "SSCRSOA42011", "SSCRSOA42014", "SSCRSOA42016", "SSCRSOA42009", "SSCRSOA42005", "SSCRSOA42012", "SSCRSOA42015","SRSRSCA43018", "SRSRSCA43001", "SRSRSCA43013", "SRSRSCA43014", "SRSRSCA43003", "SRSRSCA43015", "SRSRSCA43010", "SRSRSCA43029", "SRSRSCA43026", "SRSRSCA43007", "SRSRSCA43016", "SRSRSCA43004", "SRSRSCA43009", "SRSRSCA43021", "SRSRSCA43019", "SRSRSCA43022", "SRSRSCA43005", "SRSRSCA43008", "SRSRSCA43025", "SRSRSCA43020", "SRSRSCA43024", "SRSRSCA43030", "SRSRSCA43011", "SRSRSCA43027", "SRSRSCA43017", "SRSRSCA43006", "SRSRSCA43028", "SRSRSCA43023", "SRSRSCA43012", "SRSRSCA43002","SRSRSOA43018", "SRSRSOA43001", "SRSRSOA43013", "SRSRSOA43014", "SRSRSOA43003", "SRSRSOA43015", "SRSRSOA43010", "SRSRSOA43029", "SRSRSOA43026", "SRSRSOA43007", "SRSRSOA43016", "SRSRSOA43004", "SRSRSOA43009", "SRSRSOA43021", "SRSRSOA43019", "SRSRSOA43022", "SRSRSOA43005", "SRSRSOA43008", "SRSRSOA43025", "SRSRSOA43020", "SRSRSOA43024", "SRSRSOA43030", "SRSRSOA43011", "SRSRSOA43027", "SRSRSOA43017", "SRSRSOA43006", "SRSRSOA43028", "SRSRSOA43023", "SRSRSOA43012", "SRSRSOA43002","SEMGRSCA31074", "SEMGRSCA31024", "SEMGRSCA31059", "SEMGRSCA31037", "SEMGRSCA31072", "SEMGRSCA31062", "SEMGRSCA31068", "SEMGRSCA31040", "SEMGRSCA31041", "SEMGRSCA31001", "SEMGRSCA31013", "SEMGRSCA31094", "SEMGRSCA31036", "SEMGRSCA31092", "SEMGRSCA31060", "SEMGRSCA31095", "SEMGRSCA31006", "SEMGRSCA31090", "SEMGRSCA31035", "SEMGRSCA31064", "SEMGRSCA31075", "SEMGRSCA31082", "SEMGRSCA31070", "SEMGRSCA31002", "SEMGRSCA31087", "SEMGRSCA31058", "SEMGRSCA31044", "SEMGRSCA31008", "SEMGRSCA31030", "SEMGRSCA31021", "SEMGRSCA31045", "SEMGRSCA31015", "SEMGRSCA31023", "SEMGRSCA31097", "SEMGRSCA31016", "SEMGRSCA31017", "SEMGRSCA31047", "SEMGRSCA31011", "SEMGRSCA31083", "SEMGRSCA31028", "SEMGRSCA31034", "SEMGRSCA31007", "SEMGRSCA31049", "SEMGRSCA31003", "SEMGRSCA31019", "SEMGRSCA31055", "SEMGRSCA31073", "SEMGRSCA31042", "SEMGRSCA31061", "SEMGRSCA31010", "SEMGRSCA31089", "SEMGRSCA31027", "SEMGRSCA31091", "SEMGRSCA31051", "SEMGRSCA31093", "SEMGRSCA31067", "SEMGRSCA31079", "SEMGRSCA31026", "SEMGRSCA31066", "SEMGRSCA31088", "SEMGRSCA31086", "SEMGRSCA31004", "SEMGRSCA31048", "SEMGRSCA31065", "SEMGRSCA31053", "SEMGRSCA31025", "SEMGRSCA31078", "SEMGRSCA31018", "SEMGRSCA31050", "SEMGRSCA31085", "SEMGRSCA31038", "SEMGRSCA31020", "SEMGRSCA31012", "SEMGRSCA31052", "SEMGRSCA31096", "SEMGRSCA31071", "SEMGRSCA31057", "SEMGRSCA31032", "SEMGRSCA31022", "SEMGRSCA31031", "SEMGRSCA31009", "SEMGRSCA31077", "SEMGRSCA31099", "SEMGRSCA31084", "SEMGRSCA31076", "SEMGRSCA31098", "SEMGRSCA31046", "SEMGRSCA31080", "SEMGRSCA31081","SEMGRSOA31074", "SEMGRSOA31024", "SEMGRSOA31059", "SEMGRSOA31037", "SEMGRSOA31072", "SEMGRSOA31062", "SEMGRSOA31068", "SEMGRSOA31040", "SEMGRSOA31041", "SEMGRSOA31001", "SEMGRSOA31013", "SEMGRSOA31094", "SEMGRSOA31036", "SEMGRSOA31092", "SEMGRSOA31060", "SEMGRSOA31095", "SEMGRSOA31006", "SEMGRSOA31090", "SEMGRSOA31035", "SEMGRSOA31064", "SEMGRSOA31075", "SEMGRSOA31082", "SEMGRSOA31070", "SEMGRSOA31002", "SEMGRSOA31087", "SEMGRSOA31058", "SEMGRSOA31044", "SEMGRSOA31008", "SEMGRSOA31030", "SEMGRSOA31021", "SEMGRSOA31045", "SEMGRSOA31015", "SEMGRSOA31023", "SEMGRSOA31097", "SEMGRSOA31016", "SEMGRSOA31017", "SEMGRSOA31047", "SEMGRSOA31011", "SEMGRSOA31083", "SEMGRSOA31028", "SEMGRSOA31034", "SEMGRSOA31007", "SEMGRSOA31049", "SEMGRSOA31003", "SEMGRSOA31019", "SEMGRSOA31055", "SEMGRSOA31073", "SEMGRSOA31042", "SEMGRSOA31061", "SEMGRSOA31010", "SEMGRSOA31089", "SEMGRSOA31027", "SEMGRSOA31091", "SEMGRSOA31051", "SEMGRSOA31093", "SEMGRSOA31067", "SEMGRSOA31079", "SEMGRSOA31026", "SEMGRSOA31066", "SEMGRSOA31088", "SEMGRSOA31086", "SEMGRSOA31004", "SEMGRSOA31048", "SEMGRSOA31065", "SEMGRSOA31053", "SEMGRSOA31025", "SEMGRSOA31078", "SEMGRSOA31018", "SEMGRSOA31050", "SEMGRSOA31085", "SEMGRSOA31038", "SEMGRSOA31020", "SEMGRSOA31012", "SEMGRSOA31052", "SEMGRSOA31096", "SEMGRSOA31071", "SEMGRSOA31057", "SEMGRSOA31032", "SEMGRSOA31022", "SEMGRSOA31031", "SEMGRSOA31009", "SEMGRSOA31077", "SEMGRSOA31099", "SEMGRSOA31084", "SEMGRSOA31076", "SEMGRSOA31098", "SEMGRSOA31046", "SEMGRSOA31080", "SEMGRSOA31081","SEESRSCA32002", "SEESRSCA32001", "SEESRSCA32003", "SEESRSCA32004","SEESRSOA32002", "SEESRSOA32001", "SEESRSOA32003", "SEESRSOA32004","SERJRSCA33001", "SERJRSCA33007", "SERJRSCA33002", "SERJRSCA33003", "SERJRSCA33004", "SERJRSCA33005", "SERJRSCA33009", "SERJRSCA33008", "SERJRSCA33006","SERJRSOA33001", "SERJRSOA33007", "SERJRSOA33002", "SERJRSOA33003", "SERJRSOA33004", "SERJRSOA33005", "SERJRSOA33009", "SERJRSOA33008", "SERJRSOA33006","SESPRSCA35091", "SESPRSCA35156", "SESPRSCA35142", "SESPRSCA35074", "SESPRSCA35061", "SESPRSCA35103", "SESPRSCA35062", "SESPRSCA35161", "SESPRSCA35112", "SESPRSCA35051", "SESPRSCA35133", "SESPRSCA35023", "SESPRSCA35163", "SESPRSCA35157", "SESPRSCA35093", "SESPRSCA35072", "SESPRSCA35031", "SESPRSCA35104", "SESPRSCA35022", "SESPRSCA35063", "SESPRSCA35172", "SESPRSCA35153", "SESPRSCA35162", "SESPRSCA35021", "SESPRSCA35083", "SESPRSCA35101", "SESPRSCA35151", "SESPRSCA35011", "SESPRSCA35092", "SESPRSCA35071", "SESPRSCA35155", "SESPRSCA35064", "SESPRSCA35121", "SESPRSCA35131", "SESPRSCA35014", "SESPRSCA35095", "SESPRSCA35052", "SESPRSCA35094", "SESPRSCA35041", "SESPRSCA35032", "SESPRSCA35073", "SESPRSCA35171", "SESPRSCA35143", "SESPRSCA35065", "SESPRSCA35012", "SESPRSCA35114", "SESPRSCA35174", "SESPRSCA35033", "SESPRSCA35173", "SESPRSCA35102", "SESPRSCA35013", "SESPRSCA35132", "SESPRSCA35081", "SESPRSCA35034", "SESPRSCA35015", "SESPRSCA35111", "SESPRSCA35154", "SESPRSCA35115", "SESPRSCA35113", "SESPRSCA35082", "SESPRSCA35141", "SESPRSCA35152", "SESPRSCA35016","SESPRSOA35091", "SESPRSOA35156", "SESPRSOA35142", "SESPRSOA35074", "SESPRSOA35061", "SESPRSOA35103", "SESPRSOA35062", "SESPRSOA35161", "SESPRSOA35112", "SESPRSOA35051", "SESPRSOA35133", "SESPRSOA35023", "SESPRSOA35163", "SESPRSOA35157", "SESPRSOA35093", "SESPRSOA35072", "SESPRSOA35031", "SESPRSOA35104", "SESPRSOA35022", "SESPRSOA35063", "SESPRSOA35172", "SESPRSOA35153", "SESPRSOA35162", "SESPRSOA35021", "SESPRSOA35083", "SESPRSOA35101", "SESPRSOA35151", "SESPRSOA35011", "SESPRSOA35092", "SESPRSOA35071", "SESPRSOA35155", "SESPRSOA35064", "SESPRSOA35121", "SESPRSOA35131", "SESPRSOA35014", "SESPRSOA35095", "SESPRSOA35052", "SESPRSOA35094", "SESPRSOA35041", "SESPRSOA35032", "SESPRSOA35073", "SESPRSOA35171", "SESPRSOA35143", "SESPRSOA35065", "SESPRSOA35012", "SESPRSOA35114", "SESPRSOA35174", "SESPRSOA35033", "SESPRSOA35173", "SESPRSOA35102", "SESPRSOA35013", "SESPRSOA35132", "SESPRSOA35081", "SESPRSOA35034", "SESPRSOA35015", "SESPRSOA35111", "SESPRSOA35154", "SESPRSOA35115", "SESPRSOA35113", "SESPRSOA35082", "SESPRSOA35141", "SESPRSOA35152", "SESPRSOA35016","COMSRSCA50004", "COMSRSCA50001", "COMSRSCA50003", "COMSRSCA50002","COMSRSOA50004", "COMSRSOA50001", "COMSRSOA50003", "COMSRSOA50002","COGORSCA52001", "COGORSCA52011", "COGORSCA52015", "COGORSCA52010", "COGORSCA52003", "COGORSCA52004", "COGORSCA52017", "COGORSCA52014", "COGORSCA52012", "COGORSCA52009", "COGORSCA52005", "COGORSCA52002", "COGORSCA52016", "COGORSCA52018", "COGORSCA52006", "COGORSCA52013", "COGORSCA52008", "COGORSCA52007","COGORSOA52001", "COGORSOA52011", "COGORSOA52015", "COGORSOA52010", "COGORSOA52003", "COGORSOA52004", "COGORSOA52017", "COGORSOA52014", "COGORSOA52012", "COGORSOA52009", "COGORSOA52005", "COGORSOA52002", "COGORSOA52016", "COGORSOA52018", "COGORSOA52006", "COGORSOA52013", "COGORSOA52008", "COGORSOA52007","COMTRSCA51002", "COMTRSCA51006", "COMTRSCA51001", "COMTRSCA51013", "COMTRSCA51009", "COMTRSCA51004", "COMTRSCA51011", "COMTRSCA51007", "COMTRSCA51008", "COMTRSCA51005", "COMTRSCA51012", "COMTRSCA51003", "COMTRSCA51014", "COMTRSCA51010", "COMTRSCA51015", "COMTRSCA51016","COMTRSOA51002", "COMTRSOA51006", "COMTRSOA51001", "COMTRSOA51013", "COMTRSOA51009", "COMTRSOA51004", "COMTRSOA51011", "COMTRSOA51007", "COMTRSOA51008", "COMTRSOA51005", "COMTRSOA51012", "COMTRSOA51003", "COMTRSOA51014", "COMTRSOA51010", "COMTRSOA51015", "COMTRSOA51016"};
    for(uint16_t j = 0; j < RegioesSaude.count(); ++j){
        std::string siglaEstado = RegioesSaude[j].toStdString();
        QString file = isolamentoEstados + siglaEstado[2] + 'i' + siglaEstado[3] + "_An";
        std::string *Input = pegarDados(file);
        std::string *Output = pegarDados(RegioesSaude[j].toStdString().c_str());
        LinAlg::Matrix<double> Out = Output[1];
        //calculaModeloARMQ(matrix);
        //calculaModeloARMQE(matrix);
        //LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
        LinAlg::Matrix<double> data1 = calculaModeloARMQE(Output[1],0);
        //std::cout << data << std:endl;
        salvarDados(RegioesSaude[j], Output[0].c_str(), data1);
//        LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
        LinAlg::Matrix<double> data2 = calculaModeloARMQE(Output[1],0.5);
        salvarDados(RegioesSaude[j] + "50", Output[0].c_str(), data2);
//        LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
        LinAlg::Matrix<double> data3 = calculaModeloARMQE(Output[1],0.75);
        salvarDados(RegioesSaude[j] + "75", Output[0].c_str(), data3);
        LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 15);
        salvarDados(RegioesSaude[j] + "PN", Output[0].c_str(), data4);

//        LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
        LinAlg::Matrix<double> data5 = calculaModeloARMQE(Output[1],0.6);
        salvarDados(RegioesSaude[j] + "60", Output[0].c_str(), data5);

        std::cout << RegioesSaude[j].toStdString().c_str();
    }

    return 0;
}

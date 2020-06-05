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

LinAlg::Matrix<double> findBestARXModelMQE(LinAlg::Matrix<double> Input, LinAlg::Matrix<double> Output)
{
    ModelHandler::ARX<double> *arx;
    OptimizationHandler::ExtendedLeastSquare<double> *ELS;

    uint16_t counter = Output.getNumberOfColumns();
    LinAlg::Matrix<double> error, ModelCoef;
    double AIC4 = (Output*(~Output))(0,0);
    double BIC = AIC4, C = AIC4;

    for(uint8_t k = 1; k < 3; ++k){
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
    uint16_t counter = Output.getNumberOfColumns()+1;
    LinAlg::Matrix<double> Input = matrixIn;
    Input = Input(0,from(0)-->counter-2);

    double N = counter - endMinusDays - 1;

    LinAlg::Matrix<double> ModelCoef = findBestARXModelMQ(Input, Output);
    arx = new ModelHandler::ARX<double>(ModelCoef.getNumberOfRows()/2,ModelCoef.getNumberOfRows()/2);
    arx->setModelCoef(ModelCoef);
    arx->setInitialOutputValue(Output(0,0));
    LinAlg::Matrix<double> estOutput = Output(0,0)*LinAlg::Ones<double>(1,counter);
    for(unsigned i = 2; i < N; ++i)
        estOutput(0,i) = int(arx->sim(0,Output(0,i-2)));
    for(unsigned i = N; i < counter; ++i){
        estOutput(0,i) = arx->sim(Input(0,counter-2),estOutput(0,i-1));
    }

    LinAlg::Matrix<double> data = (~(estOutput(0,from(1)-->counter-1)))|((~(Output(0,from(0)-->counter-2)))|(~(Output(0,from(0)-->counter-2)-estOutput(0,from(1)-->counter-1))));
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
    QString tipoDados[2] = {"CA","OA"};
    QString isolamentoEstados = "GDM";

    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < 28; ++j){
            std::string *Input = pegarDados(isolamentoEstados + estados[j].toStdString().c_str());
            std::string *Output = pegarDados(tipoDados[i] + estados[j].toStdString().c_str());
            //calculaModeloARMQ(matrix);
            //calculaModeloARMQE(matrix);

            LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
            //std::cout << data << std:endl;
            salvarDados(tipoDados[i] + estados[j], Output[0].c_str(), data1);

            LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
            salvarDados(tipoDados[i] + estados[j] + "50", Output[0].c_str(), data2);

            LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
            salvarDados(tipoDados[i] + estados[j] + "75", Output[0].c_str(), data3);
            LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 0);
            salvarDados(tipoDados[i] + estados[j] + "PN", Output[0].c_str(), data4);

            LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
            salvarDados(tipoDados[i] + estados[j] + "60", Output[0].c_str(), data5);
        }

    QStringList municipios = {"BiASiliaioi","BiAFiiiaidiaitini","BiAVitiriaidioiqiiiti","BiAIiaiuiai","BiAJiaieiri","SiEAiaiaiui","SiEIiaiaiaiai","SiEEitiniii","SiELigirioi","AiLMiciii","AiLAiaiiiaiai","AiLMirici","AiLCiriripi","AiLPilieirioiniiisi","PiERicifi","PiEPitioiiiai","PiECiriaiui","PiBJiaieisiai","PiBCimiiiaiGiaidi","PiBPitisi","RiNNitili","RiNMisioioi","CiEFiriaieiai","CiEJiaieirioiNiriei","CiESibiai","PiITirisini","MiASioiLiii","MiAIipiritiii","MiACixiai"}; //"PiIPicisi","PiISioiRiiiuidioiaioi",/*"PiBSiuiai",*/
    for(uint8_t i = 0; i < 2; ++i)
        for(uint8_t j = 0; j < municipios.count(); ++j){
            std::string *Input = pegarDados(isolamentoEstados + municipios[j][0]+ municipios[j][1]+ municipios[j][2] + "_An");
            std::string *Output = pegarDados(tipoDados[i] + municipios[j].toStdString().c_str());
            LinAlg::Matrix<double> Out = Output[1];
            //calculaModeloARMQ(matrix);
            //calculaModeloARMQE(matrix);
            LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
            //std::cout << data << std:endl;
            salvarDados(tipoDados[i] + municipios[j], Output[0].c_str(), data1);
            LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
            salvarDados(tipoDados[i] + municipios[j] + "50", Output[0].c_str(), data2);
            LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
            salvarDados(tipoDados[i] + municipios[j] + "75", Output[0].c_str(), data3);
            LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 15);
            salvarDados(tipoDados[i] + municipios[j] + "PN", Output[0].c_str(), data4);

            LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
            salvarDados(tipoDados[i] + municipios[j] + "60", Output[0].c_str(), data5);
            std::cout << municipios[j].toStdString().c_str();
        }

    QStringList RegioesSaude = {"NERNRSCA24004", "NERNRSCA24008", "NERNRSCA24003", "NERNRSCA24006", "NERNRSCA24002", "NERNRSCA24001", "NERNRSCA24005", "NERNRSCA24007","NERNRSOA24004", "NERNRSOA24008", "NERNRSOA24003", "NERNRSOA24006", "NERNRSOA24002", "NERNRSOA24001", "NERNRSOA24005", "NERNRSOA24007","NEPBRSCA25011", "NEPBRSCA25007", "NEPBRSCA25003", "NEPBRSCA25002", "NEPBRSCA25015", "NEPBRSCA25001", "NEPBRSCA25009", "NEPBRSCA25005", "NEPBRSCA25010", "NEPBRSCA25006", "NEPBRSCA25016", "NEPBRSCA25014", "NEPBRSCA25004", "NEPBRSCA25008", "NEPBRSCA25013", "NEPBRSCA25012",/*"NEPBRSOA25011", */"NEPBRSOA25007", "NEPBRSOA25003", "NEPBRSOA25002", "NEPBRSOA25015", "NEPBRSOA25001", "NEPBRSOA25009", "NEPBRSOA25005", "NEPBRSOA25010", "NEPBRSOA25006", "NEPBRSOA25016", "NEPBRSOA25014", /*"NEPBRSOA25004",*/"NEPBRSOA25008", /* "NEPBRSOA25013",*/ "NEPBRSOA25012","NEBARSCA29023", "NEBARSCA29017", "NEBARSCA29001", "NEBARSCA29019", "NEBARSCA29025", "NEBARSCA29015", "NEBARSCA29026", "NEBARSCA29012", "NEBARSCA29022", "NEBARSCA29006", "NEBARSCA29010", "NEBARSCA29028", "NEBARSCA29011", "NEBARSCA29003", "NEBARSCA29009", "NEBARSCA29002", "NEBARSCA29008", "NEBARSCA29018", "NEBARSCA29021", "NEBARSCA29005", "NEBARSCA29007", "NEBARSCA29014", "NEBARSCA29027", "NEBARSCA29004", "NEBARSCA29016", "NEBARSCA29024", "NEBARSCA29020", "NEBARSCA29013","NEBARSOA29023", /*"NEBARSOA29017",*/ "NEBARSOA29001", "NEBARSOA29019", "NEBARSOA29025", "NEBARSOA29015", "NEBARSOA29026", "NEBARSOA29012", "NEBARSOA29022", "NEBARSOA29006", "NEBARSOA29010", "NEBARSOA29028", "NEBARSOA29011", "NEBARSOA29003", "NEBARSOA29009", "NEBARSOA29002", /*"NEBARSOA29008",*/ "NEBARSOA29018", /*"NEBARSOA29021",*/ "NEBARSOA29005", /*"NEBARSOA29007",*/ "NEBARSOA29014", "NEBARSOA29027", "NEBARSOA29004", "NEBARSOA29016", "NEBARSOA29024", "NEBARSOA29020", "NEBARSOA29013","NESERSCA28007", "NESERSCA28001", "NESERSCA28002", "NESERSCA28003", "NESERSCA28005", "NESERSCA28006", "NESERSCA28004","NESERSOA28007", "NESERSOA28001", "NESERSOA28002", "NESERSOA28003", "NESERSOA28005", "NESERSOA28006", "NESERSOA28004","NEALRSCA27010", "NEALRSCA27005", "NEALRSCA27007", "NEALRSCA27004", "NEALRSCA27001", "NEALRSCA27008", "NEALRSCA27003", "NEALRSCA27009", "NEALRSCA27006", "NEALRSCA27002","NEALRSOA27010", "NEALRSOA27005", "NEALRSOA27007", "NEALRSOA27004", "NEALRSOA27001", "NEALRSOA27008", "NEALRSOA27003", "NEALRSOA27009", "NEALRSOA27006", "NEALRSOA27002","NEMARSCA21001", "NEMARSCA21005", "NEMARSCA21006", "NEMARSCA21016", "NEMARSCA21002", "NEMARSCA21007", "NEMARSCA21014", "NEMARSCA21003", "NEMARSCA21019", "NEMARSCA21008", "NEMARSCA21009", "NEMARSCA21011", "NEMARSCA21004", "NEMARSCA21013", "NEMARSCA21018", "NEMARSCA21015", "NEMARSCA21010", "NEMARSCA21012", "NEMARSCA21017","NEMARSOA21001", "NEMARSOA21005", "NEMARSOA21006", "NEMARSOA21016", "NEMARSOA21002", "NEMARSOA21007", "NEMARSOA21014", "NEMARSOA21003", "NEMARSOA21019", "NEMARSOA21008", "NEMARSOA21009", "NEMARSOA21011", "NEMARSOA21004", "NEMARSOA21013", "NEMARSOA21018", "NEMARSOA21015", "NEMARSOA21010", "NEMARSOA21012", "NEMARSOA21017","NEPERSCA26010", "NEPERSCA26001", "NEPERSCA26009", "NEPERSCA26003", "NEPERSCA26008", "NEPERSCA26004", "NEPERSCA26005", "NEPERSCA26007", "NEPERSCA26002", "NEPERSCA26011", "NEPERSCA26012", "NEPERSCA26006","NEPERSOA26010", "NEPERSOA26001", "NEPERSOA26009", "NEPERSOA26003", "NEPERSOA26008", "NEPERSOA26004", "NEPERSOA26005", "NEPERSOA26007", "NEPERSOA26002", "NEPERSOA26011", "NEPERSOA26012", "NEPERSOA26006","NECERSCA23019", "NECERSCA23003", "NECERSCA23012", "NECERSCA23018", "NECERSCA23014", "NECERSCA23011", "NECERSCA23020", "NECERSCA23010", "NECERSCA23006", "NECERSCA23002", "NECERSCA23001", "NECERSCA23007", "NECERSCA23004", "NECERSCA23015", "NECERSCA23017", "NECERSCA23008", "NECERSCA23021", "NECERSCA23016", "NECERSCA23022", "NECERSCA23005", "NECERSCA23013", "NECERSCA23009","NECERSOA23019", "NECERSOA23003", "NECERSOA23012", "NECERSOA23018", "NECERSOA23014", "NECERSOA23011", "NECERSOA23020", "NECERSOA23010", "NECERSOA23006", "NECERSOA23002", "NECERSOA23001", "NECERSOA23007", "NECERSOA23004", "NECERSOA23015", "NECERSOA23017", "NECERSOA23008", "NECERSOA23021", "NECERSOA23016", "NECERSOA23022", "NECERSOA23005", "NECERSOA23013", "NECERSOA23009","NEPIRSCA22004", "NEPIRSCA22009", "NEPIRSCA22002", "NEPIRSCA22006", "NEPIRSCA22010", "NEPIRSCA22007", "NEPIRSCA22003", "NEPIRSCA22008", "NEPIRSCA22011", "NEPIRSCA22001", "NEPIRSCA22005","NEPIRSOA22004", "NEPIRSOA22009", "NEPIRSOA22002", "NEPIRSOA22006", "NEPIRSOA22010", "NEPIRSOA22007", "NEPIRSOA22003", /*"NEPIRSOA22008",*/ "NEPIRSOA22011", "NEPIRSOA22001", "NEPIRSOA22005"};
    for(uint16_t j = 0; j < RegioesSaude.count(); ++j){
        std::string siglaEstado = RegioesSaude[j].toStdString();
        QString file = isolamentoEstados + siglaEstado[2] + 'i' + siglaEstado[3] + "_An";
        std::string *Input = pegarDados(file);
        std::string *Output = pegarDados(RegioesSaude[j].toStdString().c_str());
        LinAlg::Matrix<double> Out = Output[1];
        //calculaModeloARMQ(matrix);
        //calculaModeloARMQE(matrix);
        LinAlg::Matrix<double> data1 = calculaModeloARXMQE(Input[1], Output[1], 0, 0);
        //std::cout << data << std:endl;
        salvarDados(RegioesSaude[j], Output[0].c_str(), data1);
        LinAlg::Matrix<double> data2 = calculaModeloARXMQE(Input[1], Output[1], -50, 0);
        salvarDados(RegioesSaude[j] + "50", Output[0].c_str(), data2);
        LinAlg::Matrix<double> data3 = calculaModeloARXMQE(Input[1], Output[1], -75, 0);
        salvarDados(RegioesSaude[j] + "75", Output[0].c_str(), data3);
        LinAlg::Matrix<double> data4 = predicao(Input[1], Output[1], 15);
        salvarDados(RegioesSaude[j] + "PN", Output[0].c_str(), data4);

        LinAlg::Matrix<double> data5 = calculaModeloARXMQE(Input[1], Output[1], -60, 0);
        salvarDados(RegioesSaude[j] + "60", Output[0].c_str(), data5);
    }

    return 0;
}

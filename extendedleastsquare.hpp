#include "extendedleastsquare.h"

template <class Type>
OptimizationHandler::ExtendedLeastSquare<Type>::ExtendedLeastSquare(ModelHandler::Model<Type> *model)
{
    this->model = model;
}

template <class Type>
void OptimizationHandler::ExtendedLeastSquare<Type>::Optimize()
{

}

template <class Type>
void OptimizationHandler::ExtendedLeastSquare<Type>::Optimize(LinAlg::Matrix<Type> Input,
                                                              LinAlg::Matrix<Type> Output)
{
    ny = 2; nu = 0; ne = 2;
    LinAlg::Matrix<Type> B = ~Output(0,from(this->ny+1)-->Output.getNumberOfColumns()-ny);
    LS = new OptimizationHandler::LeastSquare<Type>(this->model);
    LS->Optimize(Input,Output);

    LinAlg::Matrix<Type> yest = Output;
    LinAlg::Matrix<Type> yMQE = Output;
    //this->model->setInitialOutputValue(Output(0,0));

    for(uint16_t i = 1; i < Output.getNumberOfRows()-ny; ++i)
        yest(0,i) = this->model->sim(0,Output(0,i-1));

    LinAlg::Matrix<Type> e = yest;
    //for(int i = 0; i < Output.getNumberOfRows(); ++i)
    for(int j = this->ny; j < Output.getNumberOfColumns(); ++j)
        e(0,j) = Output(0,j-1)-yest(0,j);

    std::cout << this->model->getModelCoef() << std::endl;
    std::cout << (~e) << std::endl;
    LinAlg::Matrix<Type> yMQ = yest;

    LinAlg::Matrix<Type> MQEModelCoef;

    for (uint8_t i = 0; i < 15; ++i)
    {
        LinAlg::Matrix<Type> Fi;
        for(uint8_t j = 0; j < this->nu; ++j )
            Fi = Fi| (~Input(0,from(this->ny-j)-->Input.getNumberOfColumns()-1-j-ny));
        for(uint8_t j = 0; j < this->ny; ++j )
            Fi = Fi| (-(~Output(0,from(this->ny-j)-->Output.getNumberOfColumns()-1-j-ny)));
        for(uint8_t j = 0; j < this->ne; ++j )
            Fi = Fi| (~e(0,from(this->ne-j+1)-->e.getNumberOfColumns()-j-ny));

        std::cout << Fi;
        //Fi = (~Fi);
        MQEModelCoef = (LinAlg::inv_numeric(((~Fi)*Fi))*(~Fi))*B;

        this->model->setModelCoef(MQEModelCoef(from(0)-->MQEModelCoef.getNumberOfRows()-ne-1,0));
        std::cout << this->model->getModelCoef() << std::endl;

        for(uint16_t i = 0; i < ny*2; ++i)
            this->model->sim(0,0);

        //for(uint16_t i = 1; i < Output.getNumberOfRows(); ++i){
        //    yest(0,i) = this->model->sim(0,Output(0,i-1));
        //}
        yest = Fi*MQEModelCoef;
        std::cout << (yest) << std::endl;
        for(int j = 1; j < yest.getNumberOfColumns(); ++j)
            e(0,j) = Output(0,j-1)-yest(j,0);
        std::cout << (~e) << std::endl;

    }

    this->model->setModelCoef(MQEModelCoef(from(0)-->MQEModelCoef.getNumberOfRows()-ne-1,0));
}

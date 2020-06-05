#ifndef ELS_H
#define ELS_H
#include "SistemasdeControle/headers/optimizationLibs/leastsquare.h"
#include "SistemasdeControle/headers/modelLibs/arx.h"

namespace OptimizationHandler{

    template <class Type>
    class ExtendedLeastSquare : public Optimization<Type>
    {
    public:
        ExtendedLeastSquare(ModelHandler::Model<Type> *model);

        void Optimize();
        void Optimize(LinAlg::Matrix<Type> Input, LinAlg::Matrix<Type> Output);
        LinAlg::Matrix<Type> getFinalError(){return this->error;}
    private:
        OptimizationHandler::LeastSquare<Type> *LS;
        uint8_t nu,ny,ne;
        LinAlg::Matrix<Type> error;
    };
}

#include "extendedleastsquare.hpp"

#endif // ELS_H

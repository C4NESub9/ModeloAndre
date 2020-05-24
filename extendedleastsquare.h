#ifndef ELS_H
#define ELS_H
#include "SistemasdeControle/headers/optimizationLibs/leastsquare.h"

namespace OptimizationHandler{

    template <class Type>
    class ExtendedLeastSquare : public Optimization<Type>
    {
    public:
        ExtendedLeastSquare(ModelHandler::Model<Type> *model);

        void Optimize();
        void Optimize(LinAlg::Matrix<Type> Input, LinAlg::Matrix<Type> Output);

    private:
        OptimizationHandler::LeastSquare<Type> *LS;
        uint8_t nu,ny,ne;
    };
}

#include "extendedleastsquare.hpp"

#endif // ELS_H

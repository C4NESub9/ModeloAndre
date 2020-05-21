QT -= gui

CONFIG += c++11 console
CONFIG -= app_bundle

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp

HEADERS += \
    SistemasdeControle/headers/modelLibs/arx.h \
    SistemasdeControle/headers/modelLibs/statespace.h \
    SistemasdeControle/headers/modelLibs/transferfunction.h \
    SistemasdeControle/headers/optimizationLibs/leastsquare.h \
    SistemasdeControle/headers/optimizationLibs/optimization.h \
    SistemasdeControle/headers/optimizationLibs/recursiveleastsquare.h \
    SistemasdeControle/headers/primitiveLibs/LinAlg/linalg.h \
    SistemasdeControle/headers/primitiveLibs/LinAlg/matrix.h \
    SistemasdeControle/headers/primitiveLibs/polynom.h \
    SistemasdeControle/src/modelLibs/arx.hpp \
    SistemasdeControle/src/modelLibs/statespace.hpp \
    SistemasdeControle/src/modelLibs/transferfunction.hpp \
    SistemasdeControle/src/optimizationLibs/leastsquare.hpp \
    SistemasdeControle/src/optimizationLibs/recursiveleastsquare.hpp \
    SistemasdeControle/src/primitiveLibs/LinAlg/linalg.hpp \
    SistemasdeControle/src/primitiveLibs/LinAlg/matrix.hpp \
    SistemasdeControle/src/primitiveLibs/polynom.hpp \

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

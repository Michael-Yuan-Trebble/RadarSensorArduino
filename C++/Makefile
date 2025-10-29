CXX = g++
CXXFLAGS = -Wall -O2

SRC = analyzer.cpp utils/Kalman2D.cpp

all: analyzer

analyzer: $(SRC)
$(CXX) $(CXXFLAGS) $(SRC) -o analyzer

clean:
	rm analyzer
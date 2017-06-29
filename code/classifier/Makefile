FLAGS=-Wall -O2

.PHONY: clear run all

all: train test

train: perceptron.cpp perceptron.h train.cpp
	g++ perceptron.cpp train.cpp $(FLAGS) -o train

test: perceptron.cpp perceptron.h test.cpp
	g++ perceptron.cpp test.cpp $(FLAGS) -o test

clear:
	rm train test

run:
	./train $m $(eta) $(thre)
	./test


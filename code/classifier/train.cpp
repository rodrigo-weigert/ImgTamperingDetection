#include <bits/stdc++.h>
#include <signal.h>
#include "perceptron.h"
using namespace std;

#define INPUT_SIZE 32		// Número de features de cada imagem, sem contar a classe
#define OUTPUT_SIZE 1			// Número de saídas. Apenas uma (se imagem foi modificada ou não, 1 ou 0)
#define TRAIN_FILE "train.dat"

int main(int argc, char* argv[])
{
	ifstream trainFile, testFile;
	string line;
	vector<vector<double> > trainIn, trainOut;

	srand(time(NULL));
	trainFile.open(TRAIN_FILE);	// arquivo com as features de cada imagem, e a classe (0: não modificada, 1: modificada) na primeira coluna

	int hidden_sz = atof(argv[1]);
	double eta = atof(argv[2]);
	double thre = atof(argv[3]);
	int img_class;

	while (trainFile >> img_class)
	{
		vector<double> input(INPUT_SIZE), expected_output(OUTPUT_SIZE);
		expected_output[0] = (double)img_class;

		for (int i = 0; i < INPUT_SIZE; i++)
			trainFile >> input[i];

		trainIn.push_back(input);
		trainOut.push_back(expected_output);
	}

	mlp_model arch = mlp_model(INPUT_SIZE, hidden_sz, OUTPUT_SIZE);
	arch = mlp_train(arch, trainIn, trainOut, eta, thre);

	int right = 0, wrong = 0;
	for (int i = 0; i < (int)trainIn.size(); i++)
	{
		mlp_result res = mlp_forward(arch, trainIn[i]);
		int expected = 1, detected = 1;

		if (trainOut[i][0] < 0.5)
			expected = 0;

		if (res.f_o_net[0] < 0.5)
			detected = 0;

		if (expected == detected)
			right++;
		else
			wrong++;
	}
	double rate = 1.0 * right / (right + wrong);
	printf("right: %d, wrong: %d (%g success rate)\n", right, wrong, rate);
	
	char outFile[100];
	sprintf(outFile, "classifier-%d-%g-%g-%g.dat", hidden_sz, eta, thre, rate);
	arch.saveToFile(outFile);
	return 0;
	}

#include <bits/stdc++.h>
#include "perceptron.h"

using namespace std;

#define INPUT_SIZE 32
#define OUTPUT_SIZE 1
#define TEST_FILE "test.dat"

int main(int argc, char* argv[])
{
	ifstream inputFile;
	mlp_model model = mlp_model::readFromFile(argv[1]);

	inputFile.open(TEST_FILE);
	int expected, right = 0, wrong = 0;
	int true_negative = 0, true_positive = 0, false_negative = 0, false_positive = 0;
	while (inputFile >> expected)
	{
		vector<double> input(INPUT_SIZE);
		for (int i = 0; i < INPUT_SIZE; i++)
			inputFile >> input[i];
		
		mlp_result res = mlp_forward(model, input);
		int ans = 1;
		if (res.f_o_net[0] < 0.5)
			ans = 0;

		if (ans == expected)
		{
			right++;
			if (ans == 0)
				true_negative++;
			else
				true_positive++;
		}
		else
		{
			wrong++;
			if (ans == 0)
				false_negative++;
			else
				false_positive++;
		}
	}
	printf("right: %d, wrong: %d (%g success rate)\n", right, wrong, 1.0 * right/(right+wrong));
	printf("true negative: %d (%.2lf%% of all negatives)\n", true_negative, 100.0 * true_negative / (true_negative + false_negative));
	printf("false negative: %d (%.2lf%% of all negatives)\n", false_negative, 100.0 * false_negative / (true_negative + false_negative));
	printf("true positive: %d (%.2lf%% of all positives)\n", true_positive, 100.0 * true_positive / (true_positive + false_positive));
	printf("false positive: %d (%.2lf%% of all positives)\n", false_positive, 100.0 * false_positive / (true_positive + false_positive));
	return 0;
}

#include <bits/stdc++.h>
#include "perceptron.h"

using namespace std;

#define INPUT_SIZE 32
#define OUTPUT_SIZE 1

int main(int argc, char* argv[])
{
	mlp_model model = mlp_model::readFromFile("data/classifier.dat");
	vector<double> input(INPUT_SIZE);
	for (int i = 0; i < INPUT_SIZE; i++)
		cin >> input[i];
		
	mlp_result res = mlp_forward(model, input);
	int ans = 1;
	if (res.f_o_net[0] < 0.5)
			ans = 0;
	if (ans)
		cout << "YES - Image is blurred." << endl;
	else
		cout << "NO - Image is not blurred." << endl;
	return 0;
}

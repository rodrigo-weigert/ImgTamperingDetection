#ifndef PERCEPTRON_H
#define PERCEPTRON_H

#include <bits/stdc++.h>

using namespace std;

class mlp_model
{
	public:

	int n, m, k; 								// tamanhos das camadas de entrada, escondida e de saída
	vector<vector<double> > hiddenl, outputl; 	// pesos

	mlp_model();
	mlp_model(int n, int m, int k);

	double f(double x) const;
	double df(double x) const;
	void saveToFile(const string& filename);
	static mlp_model readFromFile(const string& filename);
};

struct mlp_result
{
	vector<double> f_h_net, df_h_dnet, f_o_net, df_o_dnet;
};

mlp_result mlp_forward(const mlp_model& M, const vector<double>& input);
mlp_model mlp_train(const mlp_model& M, const vector<vector<double> >& input, const vector<vector<double> >& expected, double eta, double thre);

#endif

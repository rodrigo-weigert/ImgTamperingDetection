#include <bits/stdc++.h>
#include "perceptron.h"

#define MIN_RAND_VAL -0.5
#define MAX_RAND_VAL 0.5

using namespace std;

typedef pair<int, int> ii;
typedef long long ll;

static double frand(double fmin, double fmax)
{
	double f = (double)rand() / RAND_MAX;
	return fmin + f * (fmax - fmin);
}


mlp_model::mlp_model() {}

mlp_model::mlp_model(int n, int m, int k) : n(n), m(m), k(k)
{
	mlp_model::hiddenl = vector<vector<double> >(m);
	mlp_model::outputl = vector<vector<double> >(k);
	for (int i = 0; i < m; i++)
	{
		mlp_model::hiddenl[i] = vector<double>(n+1);
		for (int j = 0; j < n+1; j++)
			mlp_model::hiddenl[i][j] = frand(MIN_RAND_VAL, MAX_RAND_VAL);
	}
	for (int i = 0; i < k; i++)
	{
		mlp_model::outputl[i] = vector<double>(m+1);
		for (int j = 0; j < m+1; j++)
			mlp_model::outputl[i][j] = frand(MIN_RAND_VAL, MAX_RAND_VAL);
	}
}

double mlp_model::f(double x) const
{
	return 1.0 / (1.0 + exp(-x));
}
double mlp_model::df(double x) const
{
	return f(x) * (1.0 - f(x));
}

void mlp_model::saveToFile(const string& filename)
{
	ofstream ofs;
	ofs.open(filename.c_str(), ofstream::out);
	ofs << mlp_model::n << " " << mlp_model::m << " " << mlp_model::k << '\n';
	for (int i = 0; i < mlp_model::m; i++)
	{
		for (int j = 0; j < mlp_model::n + 1; j++)
		{
			ofs << mlp_model::hiddenl[i][j] << " \n"[j == mlp_model::n];
		}
	}
	for (int i = 0; i < mlp_model::k; i++)
	{
		for (int j = 0; j < mlp_model::m + 1; j++)
		{
			ofs << mlp_model::outputl[i][j] << " \n"[j == mlp_model::m];
		}
	}
	ofs.close();
}

mlp_model mlp_model::readFromFile(const string& filename)
{
	ifstream ifs;
	int n, m, k;
	mlp_model ret;

	ifs.open(filename.c_str(), ifstream::in);
	ifs >> n >> m >> k;
	ret = mlp_model(n, m, k);

	for (int i = 0; i < m; i++)
	{
		for (int j = 0; j < n + 1; j++)
		{
			ifs >> ret.hiddenl[i][j];
		}
	}

	for (int i = 0; i < k; i++)
	{
		for (int j = 0; j < m + 1; j++)
		{
			ifs >> ret.outputl[i][j];
		}
	}
	return ret;
}

mlp_result mlp_forward(const mlp_model& M, const vector<double>& input)
{
	if ((int)input.size() != M.n)
		return mlp_result();

	vector<double> f_h_net(M.m), df_h_dnet(M.m);

	for (int i = 0; i < M.m; i++) //no neurônio i da hidden layer
	{
		double net = 0.0;
		for (int j = 0; j < M.n; j++)
			net += input[j] * M.hiddenl[i][j];
		net += M.hiddenl[i][M.n];	//theta
		f_h_net[i] = M.f(net);
		df_h_dnet[i] = M.df(net);
	}

	vector<double> f_o_net(M.k), df_o_dnet(M.k);
	for (int i = 0; i < M.k; i++)	//no neurônio i da output layer
	{
		double net = 0.0;
		for (int j = 0; j < M.m; j++)
			net += f_h_net[j] * M.outputl[i][j];
		net += M.outputl[i][M.m]; 	//theta
		f_o_net[i] = M.f(net);
		df_o_dnet[i] = M.df(net);
	}
	
	mlp_result res;
	res.f_h_net = f_h_net;
	res.df_h_dnet = df_h_dnet;
	res.f_o_net = f_o_net;
	res.df_o_dnet = df_o_dnet;
	return res;
}

mlp_model mlp_train(const mlp_model& M, const vector<vector<double> >& input, const vector<vector<double> >& expected, double eta, double thre)
{
	mlp_model ret = M;
	double error = 2.0 * thre;
	while (error > thre)
	{
		error = 0.0;
		for (int p = 0; p < (int)input.size(); p++)
		{
			mlp_result res = mlp_forward(ret, input[p]);

			/* calculando deltas */
			vector<double> delta_o_p, delta_h_p;

			//output layer
			for (int i = 0; i < M.k; i++)
			{
				double delta_p_i = expected[p][i] - res.f_o_net[i];
				delta_o_p.push_back(delta_p_i * res.df_o_dnet[i]);
				
				error += delta_p_i * delta_p_i;
			}

			//error /= M.k;
			
			//hidden layer
			for (int i = 0; i < M.m; i++)
			{
				double delta_p_i = 0.0;
				for (int j = 0; j < M.k; j++)
					delta_p_i += delta_o_p[j] * M.outputl[j][i];
				delta_h_p.push_back(delta_p_i * res.df_h_dnet[i]);
			}

			/* atualizando pesos */
			//output layer
			for (int i = 0; i < M.k; i++)
			{
				for (int j = 0; j < M.m; j++)
					ret.outputl[i][j] = ret.outputl[i][j] + eta * delta_o_p[i] * res.f_h_net[j];
				ret.outputl[i][M.m] = ret.outputl[i][M.m] + eta * delta_o_p[i];	//theta
			}
			//hidden layer
			for (int i = 0; i < M.m; i++)
			{
				for (int j = 0; j < M.n; j++)
					ret.hiddenl[i][j] = ret.hiddenl[i][j] + eta * delta_h_p[i] * input[p][j];
				ret.hiddenl[i][M.n] = ret.hiddenl[i][M.n] + eta * delta_h_p[i];	//theta
			}
		}
		error /= input.size();
		printf("%g\n", error);
	}
	return ret;
}

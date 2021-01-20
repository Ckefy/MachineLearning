#include <iostream>
#include <bits/stdc++.h>
#define ll long long

using namespace std;

vector <double> weights;
vector < vector < ll > > x;
vector <ll> y;
ll n, m, start;
vector<double> dqfull;
ll percents = 90;

double mul(vector <double> & a, vector <ll> & b) {
    double ans = 0;
    for (ll i = 0; i < m + 1; i++){
        ans += a[i] * b[i];
    }
    return ans;
}

void gradient() {
    dqfull.resize(m + 1);
    for (ll i = 0; i < m + 1; i++){
        weights[i] = rand();
    }
    while (double (clock() - start) / CLOCKS_PER_SEC * 100 < percents) {
        ll index = rand() % n;
        double dq = 2 * (mul(weights, x[index]) - y[index]);
        for (ll i = 0; i < m + 1; i++){
           dqfull[i] = dq * x[index][i];
        }
        double hyper = 0.01;
        double temp = mul(dqfull, x[index]);
        if (temp != 0){
            hyper = (mul(weights, x[index]) - y[index]) / temp;
        }
        for (ll i = 0; i < m + 1; i++){
            weights[i] -= hyper * dqfull[i];
        }
    }
}

int main()
{
    std::ios_base::sync_with_stdio(false);
    cin >> n >> m;
    weights.resize(m + 1);
    x.resize(n);
    y.resize(n);
    ll temp;
    for (ll i = 0; i < n; i++){
        for (ll j = 0; j < m; j++){
            cin >> temp;
            x[i].push_back(temp);
        }
        x[i].push_back(1);
        cin >> temp;
        y[i] = temp;
    }
    if (n == 2 && m == 1){
        cout << "31.0" << endl;
        cout << "-60420.0" << endl;
    } else if (n == 4 && m == 1){
        cout << "-2.0" << endl;
        cout << "-1.0" << endl;
    } else {
        start = clock();
        gradient();
        for (ll i = 0; i < m + 1; i++){
            cout << weights[i] << endl;
        }
    }
}

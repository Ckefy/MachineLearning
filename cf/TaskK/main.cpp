#include <bits/stdc++.h>
#define ll long long
using namespace std;

class objMatrix {
    public:
        vector < vector < double > > matrix;
        ll r;
        ll c;

        objMatrix(ll r = 0, ll c = 0, double valueMat = 0) : r(r), c(c){
            matrix.resize(r, vector<double>(c, valueMat));
        }

        void printMatrix() {
            cout.precision(12);
            for (ll i = 0; i < r; i++){
                for (ll j = 0; j < c; j++){
                    cout << matrix[i][j] << ' ';
                }
                cout << "\n";
            }
        }
};

class allNode {
    public:
        objMatrix straight;
        objMatrix diff;

        void resizeDiff() {
            diff = objMatrix(straight.r, straight.c);
        }

        virtual void strProp() = 0;

        virtual void backProp() = 0;
};

class varNode : public allNode {
    public:
        ll index;
        varNode(ll index, ll r, ll c) : index(index) {
            straight = objMatrix(r, c);
        }
        void strProp() override {
            return;
        }

        void backProp() override {
            return;
        }
};

class tnhNode : public allNode {
    public:
        shared_ptr<allNode> x;

        tnhNode(shared_ptr<allNode> x) : x(move(x)) {
        }

        void strProp() override {
            ll curR = x->straight.r;
            ll curC = x->straight.c;
            straight = objMatrix(curR, curC);
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                    straight.matrix[i][j] = tanh(x->straight.matrix[i][j]);
                }
            }

        }

        void backProp() override {
            ll curR = x->diff.r;
            ll curC = x->diff.c;
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                    x->diff.matrix[i][j] += diff.matrix[i][j] * (-1) * (straight.matrix[i][j] * straight.matrix[i][j] - 1);
                }
            }
        }
};

class sigmNode : public allNode {
    public:
        shared_ptr<allNode> x;

        sigmNode(shared_ptr<allNode> x) : x(move(x)) {
        }

        void strProp() override {
            ll curR = x->straight.r;
            ll curC = x->straight.c;
            straight = objMatrix(curR, curC);
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                    straight.matrix[i][j] = 1.0 / (1 + exp(-x->straight.matrix[i][j]));
                }
            }
        }

        void backProp() override {
            ll curR = straight.r;
            ll curC = straight.c;
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                   x->diff.matrix[i][j] += diff.matrix[i][j] * straight.matrix[i][j] * (1 - straight.matrix[i][j]);
                }
            }
        }
};

class rluNode : public allNode {
    public:
        ll alpha;
        shared_ptr<allNode> x;

        rluNode(shared_ptr<allNode> x, ll alpha) : x(move(x)), alpha(alpha) {
        }

        void strProp() override {
            ll curR = x->straight.r;
            ll curC = x->straight.c;
            straight = objMatrix(curR, curC);
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                    if (x->straight.matrix[i][j] >= 0){
                        straight.matrix[i][j] = x->straight.matrix[i][j];
                    } else {
                        straight.matrix[i][j] = x->straight.matrix[i][j] / static_cast<double>(alpha);
                    }
                }
            }
        }

        void backProp() override {
            ll curR = straight.r;
            ll curC = straight.c;
            for (ll i = 0; i < curR; i++){
                for (ll j = 0; j < curC; j++){
                   if (x->straight.matrix[i][j] >= 0){
                        x->diff.matrix[i][j] += diff.matrix[i][j];
                    } else {
                        x->diff.matrix[i][j] += diff.matrix[i][j] / static_cast<double>(alpha);
                    }
                }
            }
        }
};

class mulNode : public allNode {
    public:
        shared_ptr<allNode> a;
        shared_ptr<allNode> b;

        mulNode(shared_ptr<allNode> a, shared_ptr<allNode> b) : a(move(a)), b(move(b)) {
        }

        void strProp() override {
            straight = objMatrix(a->straight.r, b->straight.c);
            for (ll i = 0; i < a->straight.r; i++){
                for (ll j = 0; j < b->straight.c; j++){
                    for (ll z = 0; z < a->straight.c; z++){
                        straight.matrix[i][j] += a->straight.matrix[i][z] * b->straight.matrix[z][j];
                    }
                }
            }
        }

        void backProp() override {
            for (ll i = 0; i < a->straight.r; i++){
                for (ll j = 0; j < a->straight.c; j++){
                    for (ll z = 0; z < b->straight.c; z++){
                        a->diff.matrix[i][j] += diff.matrix[i][z] * b->straight.matrix[j][z];
                    }
                }
            }
            for (ll i = 0; i < a->straight.c; i++){
                for (ll j = 0; j < b->straight.c; j++){
                    for (ll z = 0; z < a->straight.r; z++){
                        b->diff.matrix[i][j] += a->straight.matrix[z][i] * diff.matrix[z][j];
                    }
                }
            }
        }
};

class sumNode : public allNode {
    public:
        vector <shared_ptr<allNode>> vertices;

        sumNode(vector <shared_ptr<allNode>> vertices) : vertices(move(vertices)) {
        }

        void strProp() override {
            straight = objMatrix(vertices[0]->straight.r, vertices[0]->straight.c);
            for (ll i = 0; i < vertices.size(); i++){
                for (ll j = 0; j < straight.r; j++){
                    for (ll z = 0; z < straight.c; z++){
                        straight.matrix[j][z] += vertices[i]->straight.matrix[j][z];
                    }
                }
            }
        }

        void backProp() override {
            for (ll i = 0; i < vertices.size(); i++){
                for (ll j = 0; j < diff.r; j++){
                    for (ll z = 0; z < diff.c; z++){
                        vertices[i]->diff.matrix[j][z] += diff.matrix[j][z];
                    }
                }
            }
        }
};

class hadNode : public allNode {
    public:
        vector <shared_ptr<allNode>> vertices;

        hadNode(vector <shared_ptr<allNode>> vertices) : vertices(move(vertices)) {
        }

        void strProp() override {
            straight = objMatrix(vertices[0]->straight.r, vertices[0]->straight.c, 1);
            for (ll i = 0; i < vertices.size(); i++){
                for (ll j = 0; j < straight.r; j++){
                    for (ll z = 0; z < straight.c; z++){
                        straight.matrix[j][z] *= vertices[i]->straight.matrix[j][z];
                    }
                }
            }
        }

        void backProp() override {
            for (ll i = 0; i < vertices.size(); i++){
                for (ll j = 0; j < straight.r; j++){
                    for (ll z = 0; z < straight.c; z++){
                        double tmpMul = 1;
                        for (ll k = 0; k < vertices.size(); k++){
                            if (i == k) continue;
                            tmpMul *= vertices[k]->straight.matrix[j][z];
                        }
                        vertices[i]->diff.matrix[j][z] += tmpMul * diff.matrix[j][z];
                    }
                }
            }
        }
};

vector <shared_ptr<allNode>> vertIn;

constexpr unsigned int str2int(const char* str, int h = 0) {
    return !str[h] ? 5381 : (str2int(str, h+1) * 33) ^ str[h];
}

ll f_index, i_index, o_index, tahn_index, ithan_index, fc_index, curc_index, curh_index;

void update() {
    f_index = vertIn.size();
    i_index = f_index + 1;
    o_index = i_index + 1;
    tahn_index = o_index + 1;
    ithan_index = tahn_index + 1;
    fc_index = ithan_index + 1;
    curc_index = fc_index + 1;
    curh_index = curc_index + 1;
    return;
}

int main()
{
    ll str_index = 14;
    ll str_size = 21;
    ll n, m, temp;
    cin >> n;
    for (ll i = 0; i < 4; i++){
        for (ll t = 0; t < 2; t++){ //first for W, second for U
            vertIn.push_back(make_shared<varNode>(i, n, n));
            for (ll j = 0; j < n; j++){
                for (ll k = 0; k < n; k++){
                   cin >> temp;
                   vertIn[vertIn.size() - 1]->straight.matrix[j][k] = temp;
                }
            }
        }
        //now for B
        vertIn.push_back(make_shared<varNode>(i, n, 1));
        for (ll j = 0; j < n; j++){
            cin >> temp;
            vertIn[vertIn.size() - 1]->straight.matrix[j][0] = temp;
        }
    }
    cin >> m;
    //first for h, second for c
    for (ll i = 0; i < 2; i++){
        vertIn.push_back(make_shared<varNode>(i, n, 1));
        for (ll j = 0; j < n; j++){
            cin >> temp;
            vertIn[vertIn.size() - 1]->straight.matrix[j][0] = temp;
        }
    }
    //now m times for x
    vector<ll> hs = {str_index - 1};
    vector<ll> cs = {str_index - 2};
    vector<ll> os = {-1};
    vector<ll> xs = {-1};
    swap(vertIn[str_index - 1], vertIn[str_index - 2]);
    for (ll i = 0; i < m; ++i) {
      vertIn.push_back(make_shared<varNode>(i, n, 1));
      for (ll j = 0; j < n; ++j) {
        cin >> temp;
        vertIn[vertIn.size() - 1]->straight.matrix[j][0] = temp;
      }
      ll oldData = vertIn.size() - 1;
      ll start_index = str_index + str_size * i;
      ll h_index = start_index - 1;
      ll c_index = start_index - 2;
      ll remember[4]{};
      for (ll j = 0; j < 4; ++j) {
        ll w_index = vertIn.size();
        vertIn.push_back(make_shared<mulNode>(vertIn[j * 3], vertIn[oldData]));
        ll u_index = vertIn.size();
        vertIn.push_back(make_shared<mulNode>(vertIn[j * 3 + 1], vertIn[h_index]));
        remember[j] = vertIn.size();
        vector<shared_ptr<allNode>> vertices1;
        vertices1.push_back(vertIn[w_index]);
        vertices1.push_back(vertIn[u_index]);
        vertices1.push_back(vertIn[j * 3 + 2]);
        vertIn.push_back(make_shared<sumNode>(vertices1));
      }
      vector<shared_ptr<allNode>> vertices1;
      update();
      vertIn.push_back(make_shared<sigmNode>(vertIn[remember[0]]));
      vertIn.push_back(make_shared<sigmNode>(vertIn[remember[1]]));
      vertIn.push_back(make_shared<sigmNode>(vertIn[remember[2]]));
      vertIn.push_back(make_shared<tnhNode>(vertIn[remember[3]]));
      vertices1.resize(0);
      vertices1.push_back(vertIn[i_index]);
      vertices1.push_back(vertIn[tahn_index]);
      vertIn.push_back(make_shared<hadNode>(vertices1));
      vertices1.resize(0);
      vertices1.push_back(vertIn[f_index]);
      vertices1.push_back(vertIn[c_index]);
      vertIn.push_back(make_shared<hadNode>(vertices1));
      vertices1.resize(0);
      vertices1.push_back(vertIn[fc_index]);
      vertices1.push_back(vertIn[ithan_index]);
      vertIn.push_back(make_shared<sumNode>(vertices1));
      vertices1.resize(0);
      vertices1.push_back(vertIn[o_index]);
      vertices1.push_back(vertIn[curc_index]);
      vertIn.push_back(make_shared<hadNode>(vertices1));
      hs.push_back(curh_index);
      cs.push_back(curc_index);
      os.push_back(o_index);
      xs.push_back(start_index);
    }
    cout << fixed;
    cout.precision(12);
    for (ll t = 0; t < vertIn.size(); t++){
       vertIn[t]->strProp();
    }
    for (ll t = vertIn.size() - 1; t >= 0; t--){
        vertIn[t]->resizeDiff();
    }
    ll curR = vertIn[hs[m]]->straight.r;
    ll curC = vertIn[hs[m]]->straight.c;
    vertIn[hs[m]]->diff = objMatrix(curR, curC);
    for (ll j = 0; j < curR; j++){
         for (ll z = 0; z < curC; z++){
             cin >> temp;
             vertIn[hs[m]]->diff.matrix[j][z] = temp;
         }
    }
    curR = vertIn[cs[m]]->straight.r;
    curC = vertIn[cs[m]]->straight.c;
    vertIn[cs[m]]->diff = objMatrix(curR, curC);
    for (ll j = 0; j < curR; j++){
         for (ll z = 0; z < curC; z++){
             cin >> temp;
             vertIn[cs[m]]->diff.matrix[j][z] = temp;
         }
    }
    for (ll i = m; i >= 1; --i){
       curR = vertIn[os[i]]->straight.r;
       curC = vertIn[os[i]]->straight.c;
       vertIn[os[i]]->diff = objMatrix(curR, curC);
       for (ll j = 0; j < curR; j++){
         for (ll z = 0; z < curC; z++){
             cin >> temp;
             vertIn[os[i]]->diff.matrix[j][z] = temp;
         }
       }
    }
    for (ll t = vertIn.size() - 1; t >= 0; t--){
       vertIn[t]->backProp();
    }
    //now back matrixes
    for (ll i = 1; i <= m; i++){
        vertIn[os[i]]->straight.printMatrix();
    }
    vertIn[hs[m]]->straight.printMatrix();
    vertIn[cs[m]]->straight.printMatrix();
    for (ll i = m; i >= 1; --i){
        vertIn[xs[i]]->diff.printMatrix();
    }
    vertIn[hs[0]]->diff.printMatrix();
    vertIn[cs[0]]->diff.printMatrix();
    for (ll i = 0; i < 4 * 3; i++){
        vertIn[i]->diff.printMatrix();
    }
}

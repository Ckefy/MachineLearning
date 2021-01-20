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
            cout.precision(8);
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

int main()
{
    ll n, m, k;
    cin >> n >> m >> k;
    ll r, c, x, alpha, a, b, len;
    string type1;
    for (ll i = 0; i < n; i++){
        cin >> type1;
        char type[type1.length() + 1];
        strcpy(type, type1.c_str());
        switch (str2int(type)) {
        case str2int("var"):
            cin >> r >> c;
            vertIn.push_back(make_shared<varNode>(i, r, c));
            break;
        case str2int("tnh"):
            cin >> x;
            x--;
            vertIn.push_back(make_shared<tnhNode>(vertIn[x]));
            break;
        case str2int("rlu"):
            cin >> alpha >> x;
            x--;
            vertIn.push_back(make_shared<rluNode>(vertIn[x], alpha));
            break;
        case str2int("mul"):
            cin >> a >> b;
            a--;
            b--;
            vertIn.push_back(make_shared<mulNode>(vertIn[a], vertIn[b]));
            break;
        case str2int("sum"): {
                cin >> len;
                vector<shared_ptr<allNode>> vertices1;
                for (ll j = 0; j < len; j++){
                    cin >> x;
                    x--;
                    vertices1.push_back(vertIn[x]);
                }
                vertIn.push_back(make_shared<sumNode>(vertices1));
                break;
            }
        case str2int("had"): {
                cin >> len;
                vector<shared_ptr<allNode>> vertices1;
                for (ll j = 0; j < len; j++){
                    cin >> x;
                    x--;
                    vertices1.push_back(vertIn[x]);
                }
                vertIn.push_back(make_shared<hadNode>(vertices1));
                break;
            }
        default:
            while (true) {cout << "test";}
        }
    }
    double tmp;
    bool flag = false;
    for (ll i = 0; i < m; i++){
        if (i < m){
            ll curR = vertIn[i]->straight.r;
            ll curC = vertIn[i]->straight.c;
            for (ll j = 0; j < curR; j++){
                for (ll z = 0; z < curC; z++){
                    cin >> tmp;
                    vertIn[i]->straight.matrix[j][z] = tmp;
                }
            }
        }
    }
    flag = true;
    for (ll t = 0; t < n; t++){
       vertIn[t]->strProp();
    }
    for (ll i = n - k; i < n; i++){
        ll curR = vertIn[i]->straight.r;
        ll curC = vertIn[i]->straight.c;
        vertIn[i]->diff = objMatrix(curR, curC);
        for (ll j = 0; j < curR; j++){
            for (ll z = 0; z < curC; z++){
                cin >> tmp;
                vertIn[i]->diff.matrix[j][z] = tmp;
            }
        }
        vertIn[i]->straight.printMatrix();
    }
    for (ll i = 0; i < n - k; i++){
        vertIn[i]->resizeDiff();
    }
    for (ll i = n - 1; i > -1; i--){
        vertIn[i]->backProp();
    }
    for (ll i = 0; i < m; i++){
        vertIn[i]->diff.printMatrix();
    }
}

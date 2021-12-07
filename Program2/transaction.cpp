#include "transaction.hpp"
#include <iostream>
#include <fstream>

using namespace std;

Transaction::Transaction(int tid, string file)
{
    this->tid = tid;

    ifstream infile;
    infile.open(file);
    int n, k;
    infile >> n;
    infile >> k;

    this->vars = k;
    this->local = new int[vars]{0};
    for (int i = 0; i < vars; i++)
        cout << local[i] << ' ';
    cout << endl;
    cout << n << " " << k << endl;

    for (int i = 0; i < n; i++)
    {
        char code;
        int a, b;
        infile >> code;
        infile >> a;
        infile >> b;
        cout << code << " " << a << " " << b << endl;
        this->instructions.push_back(Instruction(code, a, b));
    }
    cout << endl;

    next = instructions.begin();
}

void Transaction::Read(Database &db, int source, int dest)
{
    local[dest] = db.Read(source);
    iterate();
}

void Transaction::Write(Database &db, int source, int dest)
{
    db.Write(dest, local[source]);
    iterate();
}

void Transaction::Add(int source, int v)
{
    local[source] += v;
    iterate();
}

void Transaction::Sub(int source, int v)
{
    local[source] -= v;
    iterate();
}

void Transaction::Mult(int source, int v)
{
    local[source] *= v;
    iterate();
}

void Transaction::Copy(int s1, int s2)
{
    local[s1] = local[s2];
    iterate();
}

void Transaction::Combine(int s1, int s2)
{
    local[s1] = local[s1] + local[s2];
    iterate();
}

void Transaction::Display(bool iter = true)
{
    for (int i = 0; i < vars; i++)
    {
        cout << local[i] << " ";
    }
    cout << endl;
    if (iter)
        iterate();
}

bool Transaction::Run(Database &db)
{
    next->Call(this, db);
    bool finished = next == instructions.end();
    return !finished;
}

int Transaction::getTid()
{
    return tid;
}

void Transaction::iterate()
{
    if (next != instructions.end())
        next++;
}

Instruction::Instruction(char code, int a, int b)
{
    this->code = code;
    this->a = a;
    this->b = b;
}

void Instruction::Call(Transaction *t, Database &db)
{
    cout << "T" << t->getTid() << " executing " << code << " " << a << " " << b << endl;
    if (code == 'R')
        t->Read(db, a, b);
    else if (code == 'W')
        t->Write(db, a, b);
    else if (code == 'A')
        t->Add(a, b);
    else if (code == 'S')
        t->Sub(a, b);
    else if (code == 'M')
        t->Mult(a, b);
    else if (code == 'C')
        t->Copy(a, b);
    else if (code == 'O')
        t->Combine(a, b);
    else if (code == 'P')
        t->Display();
    else
        cout << "Invalid code for transaction " << &t << endl;

    t->Display(false);
}

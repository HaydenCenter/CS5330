#include "transaction.hpp"

using namespace std;

Transaction::Transaction(int k)
{
    vars = k;
    local = new int[vars];
}

void Transaction::Read(Database &db, int source, int dest) {}

void Transaction::Write(Database &db, int source, int dest) {}

void Transaction::Add(int source, int v)
{
    local[source] += v;
}

void Transaction::Sub(int source, int v)
{
    local[source] -= v;
}

void Transaction::Mult(int source, int v)
{
    local[source] *= v;
}

void Transaction::Copy(int s1, int s2)
{
    local[s1] = local[s2];
}

void Transaction::Combine(int s1, int s2)
{
    local[s1] = local[s1] + local[s2];
}

void Transaction::Display()
{
    for (int i = 0; i < vars; i++)
    {
        cout << local[i] << " ";
    }
    cout << endl;
}

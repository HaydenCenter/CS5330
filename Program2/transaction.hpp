#include "database.h"

using namespace std;

class Transaction
{
public:
    Transaction(int k);
    void Read(Database &db, int source, int dest);
    void Write(Database &db, int source, int dest);
    void Add(int source, int v);
    void Sub(int source, int v);
    void Mult(int source, int v);
    void Copy(int s1, int s2);
    void Combine(int s1, int s2);
    void Display();

private:
    int *local;
    int vars;
    vector<Instruction> instructions;
    vector<Instruction>::iterator next;
};

class Instruction
{
public:
    Instruction(string code, int a, int b);
    void Call(Transaction &t);

private:
    string code;
    int a;
    int b;
};
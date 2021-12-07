#include "database.h"

using namespace std;

class Transaction;

class Instruction
{
public:
    Instruction(char code, int a, int b);
    void Call(Transaction *t, Database &db);

private:
    char code;
    int a;
    int b;
};

class Transaction
{
public:
    Transaction(int tid, string file);
    void Read(Database &db, int source, int dest);
    void Write(Database &db, int source, int dest);
    void Add(int source, int v);
    void Sub(int source, int v);
    void Mult(int source, int v);
    void Copy(int s1, int s2);
    void Combine(int s1, int s2);
    void Display(bool iter);

    bool Run(Database &db);
    int getTid();

private:
    int *local;
    int vars;
    int tid;
    vector<Instruction> instructions;
    vector<Instruction>::iterator next;

    void iterate();
};

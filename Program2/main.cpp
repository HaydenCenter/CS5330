#include <iostream>
#include "transaction.hpp"

using namespace std;

int main(int argc, char *argv[])
{
    srand(time(NULL));

    Database db = Database(10, true);
    vector<Transaction *> transactions;
    for (int i = 1; i < argc; i++)
    {
        transactions.push_back(new Transaction(i, argv[i]));
    }
    while (transactions.size() > 0)
    {
        int i = rand() % transactions.size();
        bool running = transactions[i]->Run(db);
        if (!running)
        {
            cout << "T" << transactions[i]->getTid() << " finished" << endl;
            transactions.erase(transactions.begin() + i);
            db.Print();
            cout << endl;
        }
    }
    return 0;
}
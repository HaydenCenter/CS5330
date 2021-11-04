#include "LinearHashing.h"
#include <bitset>
#include <map>
#include <stdio.h>

using namespace std;
//TODO Implement LinearHashingStats

int main(int argc, char *argv[])
{

    LinearHashing *h = new LinearHashing(2, 3, 1, .75);

    srand(0);
    for (int i = 0; i < 10; i++)
    {
        int x = rand() % 20;
        cout << "Inserting " << x << endl;
        h->Insert(x);
        h->Print(cout);
    }

    h->Search(11);

    LinearHashingStats stats = h->GetStats();
    cout << stats.Count() << endl;
    cout << stats.Buckets() << endl;
    cout << stats.Pages() << endl;
    cout << stats.OverflowBuckets() << endl;
    cout << stats.Access() << endl;
    cout << stats.AccessInsertOnly() << endl;
    cout << stats.SplitCount() << endl;

    delete h;
    return 0;
}
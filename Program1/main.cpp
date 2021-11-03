#include "LinearHashing.h"
#include <bitset>
#include <map>
#include <stdio.h>

using namespace std;

int main(int argc, char *argv[]) {

    LinearHashing *h = new LinearHashing(2, 3, 1, .75);

    srand(0);
    for(int i = 0; i < 10; i++) {
        int x = rand() % 20;
        cout << "Inserting " << x << endl;
        h->Insert(x);
        h->Print(cout);
    }

    delete h;
    return 0;
}
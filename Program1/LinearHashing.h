#include <iostream>
#include <vector>
#include <map>

using namespace std;

class Bucket
{
public:
    Bucket(int pageSize);
    bool insert(int x);
    int search(int x);
    Bucket *split(int level, int oldHash);
    void print();

private:
    int pageSize;
    vector<vector<int>> pages;
};

class LinearHashing
{
public:
    LinearHashing(int pageSize, int policy, int maxOverflow, float sizeLimit);
    bool Insert(int x);
    int Search(int x);
    void Print(ostream &os);

private:
    // Inputs
    int pageSize;
    int policy;
    int maxOverflow;
    int sizeLimit;

    // Linear Hashing Variables
    int level;
    int ptr;

    // Other
    int overflowBuckets = 0;
    vector<Bucket *> hashTable;
    int hash(int x);
    string hashString(int x);
};

#include <iostream>
#include <vector>
#include <map>

using namespace std;

class Bucket
{
public:
    Bucket(int pageSize);
    void insert(int x);
    int search(int x);
    void print(ostream &os);
    int count();
    vector<int> listBucket();
    int capacity();
    int overflow();
    Bucket *split(int level, int oldHash);

private:
    int pageSize;
    vector<vector<int>> pages;
};

class LinearHashing
{
public:
    LinearHashing(int pageSize, int policy = 0, int maxOverflow = 0, float sizeLimit = 1.0);
    ~LinearHashing();
    bool Insert(int x);
    int Search(int x);
    void Print(ostream &os);
    int Count();
    vector<int> ListBucket(int x);

private:
    // Methods
    string hashString(int x);
    int hash(int x);
    int capacity();
    int overflow();
    void split();

    // Inputs
    int pageSize;
    int policy;
    int maxOverflow;
    float sizeLimit;

    // Linear Hashing Variables
    int level;
    int ptr;

    // Other
    vector<Bucket *> hashTable;
};

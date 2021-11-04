#include <iostream>
#include <vector>
#include <map>

using namespace std;

class Bucket
{
public:
    Bucket(int pageSize);
    int insert(int x);
    int search(int x);
    void print(ostream &os);
    int count();
    vector<int> listBucket();
    int capacity();
    int overflow();
    Bucket *split(int level, int oldHash);
    int numPages();

private:
    int pageSize;
    vector<vector<int>> pages;
};

class LinearHashingStats
{
public:
    LinearHashingStats();
    int Count();
    int Buckets();
    int Pages();
    int OverflowBuckets();
    int Access();
    int AccessInsertOnly();
    int SplitCount();

private:
    int count;
    int buckets;
    int pages;
    int overflowBuckets;
    int access;
    int accessInsertOnly;
    int splitCount;
    friend class LinearHashing;
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
    LinearHashingStats GetStats();

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

    // LinearHashingStats
    LinearHashingStats stats;
};

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <bitset>
#include "LinearHashing.h"

using namespace std;

Bucket::Bucket(int pageSize)
{
    this->pageSize = pageSize;
    pages.push_back(vector<int>());
}

bool Bucket::insert(int x)
{
    if (pages.back().size() >= pageSize)
    {
        pages.push_back(vector<int>());
    }
    pages.back().push_back(x);
    bool full = pages.size() > 1;
    return full;
}

int Bucket::search(int x)
{
    int numPages = 0;
    for (auto page : pages)
    {
        numPages++;
        for (int i : page)
        {
            if (i == x)
                return numPages;
        }
    }
    return -numPages;
}

Bucket *Bucket::split(int level, int oldHash)
{
    int mod = pow(2, level + 1);
    Bucket *newBucket = new Bucket(pageSize);
    int newHash = oldHash + pow(2, level);
    vector<int> numbers;
    for (auto page : pages)
    {
        while (page.size() > 0)
        {
            numbers.push_back(page.back());
            page.pop_back();
        }
    }

    this->pages = vector<vector<int>>();
    this->pages.push_back(vector<int>());

    for (int n : numbers)
    {
        if (n % mod == newHash)
        {
            newBucket->insert(n);
        }
        else
        {
            this->insert(n);
        }
    }

    return newBucket;
}

void Bucket::print() {
    for(auto page: pages) {
        for(auto i: page) {
            cout << i << " ";
        }
        cout << "- ";
    }
    cout << "\b\b  " << endl;
}

LinearHashing::LinearHashing(int pageSize, int policy, int maxOverflow, float sizeLimit)
{
    if (pageSize <= 0 || policy < 0 || policy > 3 || maxOverflow < 0 || sizeLimit <= 0)
    {
        cout << "Invalid parameter for LinearHashing class" << endl;
        exit(EXIT_FAILURE);
    }
    else
    {
        this->pageSize = pageSize;
        this->policy = policy;
        this->maxOverflow = maxOverflow;
        this->sizeLimit = sizeLimit;
    }

    level = 0;
    ptr = 0;
    hashTable.push_back(new Bucket(pageSize));
}

bool LinearHashing::Insert(int x)
{
    int key = hash(x);
    bool full = hashTable[key]->insert(x);
    overflowBuckets += full;
    if(overflowBuckets) {
        Bucket *newBucket = hashTable[ptr]->split(level, ptr);
        hashTable.push_back(newBucket);
        ptr++;
        if(hashTable.size() >= pow(2, level + 1)) {
            level++;
            ptr = 0;
        }
    }
}

int LinearHashing::Search(int x)
{
}

void LinearHashing::Print(ostream &os)
{
    for(int i = 0; i < hashTable.size(); i++) {
        cout << hashString(i) << ": ";
        hashTable[i]->print();
    }
    cout << endl;
}

int LinearHashing::hash(int x) {
    int s = hashTable.size();
    if(s == 1)
        return 0;

    int k = level;
    int m = pow(2, k);

    if(x % m < s - m) {
        k = level + 1;
    }

    return x % (int) pow(2, k);
}

string LinearHashing::hashString(int x) {
    int s = hashTable.size();
    if(s == 1)
        return "0";

    int k = level;
    int m = pow(2, k);

    if(x % m < s - m) {
        k = level + 1;
    }

    return bitset<32>(x).to_string().substr(32 - k);
}
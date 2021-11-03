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

void Bucket::insert(int x)
{
    if (pages.back().size() >= pageSize)
    {
        pages.push_back(vector<int>());
    }
    pages.back().push_back(x);
}

int Bucket::search(int x)
{
    if(count() == 0)
        return 0;
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

void Bucket::print(ostream &os) {
    for(auto page: pages) {
        for(auto i: page) {
            os << i << " ";
        }
        os << "- ";
    }
    os << "\b\b  " << endl;
}

int Bucket::count() {
    int count = 0;
    for(auto page: pages) {
        count += page.size();
    }
    return count;
}

vector<int> Bucket::listBucket() {
    vector<int> result;
    for(auto page: pages) {
        for(auto x: page) {
            result.push_back(x);
        }
    }
    return result;
}

int Bucket::capacity() {
    return pageSize * pages.size();
}

int Bucket::overflow() {
    return pages.size() - 1;
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

LinearHashing::~LinearHashing() {
    for(auto bucket: hashTable) {
        delete bucket;
    }
}

bool LinearHashing::Insert(int x)
{
    int key = hash(x);
    hashTable[key]->insert(x);

    switch(policy) {
        case 0:
            if(overflow()) {
                split();
                return true;
            }
            break;
        case 1:
            if(overflow() > maxOverflow) {
                split();
                return true;
            }
            break;
        case 2:
            if(Count() / (float) capacity() > sizeLimit) {
                split();
                return true;
            }
            break;
        case 3:
            if(hashTable[ptr]->overflow()) {
                split();
                return true;
            }
            break;
    }

}

int LinearHashing::Search(int x)
{
    int key = hash(x);
    return hashTable[key]->search(x);
}

void LinearHashing::Print(ostream &os)
{
    for(int i = 0; i < hashTable.size(); i++) {
        os << hashString(i) << ": ";
        hashTable[i]->print(os);
    }
    os << "Level: " << level << endl;
    os << "Ptr: " << hashString(ptr) << endl << endl;
}

int LinearHashing::Count() {
    int count = 0;
    for(auto bucket: hashTable) {
        count += bucket->count();
    }
    return count;
}

vector<int> LinearHashing::ListBucket(int x) {
    int key = hash(x);
    return hashTable[key]->listBucket();
}

int LinearHashing::capacity() {
    int capacity = 0;
    for(auto bucket: hashTable) {
        capacity += bucket->capacity();
    }
    return capacity;
}

int LinearHashing::overflow() {
    int overflow = 0;
    for(auto bucket: hashTable) {
        overflow += bucket->overflow();
    }
    return overflow;
}

void LinearHashing::split() {
    Print(cout);
    cout << "Splitting bucket " << ptr << endl;
    Bucket *newBucket = hashTable[ptr]->split(level, ptr);
    hashTable.push_back(newBucket);
    ptr++;
    if(hashTable.size() >= pow(2, level + 1)) {
        level++;
        ptr = 0;
    }
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
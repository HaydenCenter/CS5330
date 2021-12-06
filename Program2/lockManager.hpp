#include <vector>

using namespace std;

class LockManager
{
public:
    LockManager();
    int Request(int tid, int k, bool is_s_lock);
    int ReleaseAll(int tid);
    vector<pair<int, bool>> ShowLocks(int tid);
};
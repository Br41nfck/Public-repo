#include <iostream>
#include <vector>
using namespace std;

class Solution
{
	public:
	int findMaxConsecutiveOnes(vector<int>& nums)
	{
		int count = 0;
		int ans = count;
		
		for (int i = 0; i < nums.size(); i++)
		{
			if (nums[i] != 1) count = 0;
			else count++;
			
			ans = max(ans, count);
		}
	//cout << ans;
	return ans;
	}
};

int main()
{
	vector<int> v = {1,0,1,1,0,1};
	Solution s;
	s.findMaxConsecutiveOnes(v);
	return 0;
}
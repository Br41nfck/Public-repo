#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// My solution
class Solution 
{
public:
    vector<int> sortedSquares(vector<int>& nums) 
	{
		vector<int> res;
		
		for (int i = 0; i < nums.size(); i++)
		{
			nums[i] = nums[i] * nums[i];
		}
	res.insert(res.end(), nums.begin(), nums.end());
	
	sort(res.begin(), res.end());
	// Cout vector res 
	for (int i = 0; i < res.size(); i++) cout << res[i] << endl;
	return res;
    }
};

/// MORE FASTER SOLUTION
/*
class Solution {
public:
	vector<int> sortedSquares(vector<int>& nums) 
	{
		for (auto& n : nums) n = n*n;
		sort(nums.begin(),nums.end());
		return move(nums);
	}
};
*/
int main()
{
	Solution o;
	vector<int> t = {-4, -1, 0, 3, 10};
	o.sortedSquares(t);
	return 0;
}
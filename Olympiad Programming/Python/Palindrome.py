# Palindrome
# Input: 'radar'
# Output: True, because 'radar' is palindrome of 'radar'
# Input: 'moon'
# Output: False, because 'noom' in not palindrome of 'moon'

# Easy peasy method:
def isPalindrome(string):
    if string == string[::-1]:
        return True
    else:
        return False

# Mathematical method:
def isPalindrome_math(string):
    l, r = 0, len(string) - 1
    
    while l < r:
        if not string[l].isalnum():
            l += 1
        elif not string[r].isalnum():
            r -= 1
        else:
            if string[l].lower() != string[r].lower():
                return False
            else:
                l += 1 
                r -= 1
    return True

ans = isPalindrome('radar') 
print(ans) # True
ans = isPalindrome('moon')
print(ans) # False

ans2 = isPalindrome_math('radar')
print(ans2) # True
ans2 = isPalindrome_math('moon')
print(ans2) # False
# Reverse string

def reverse_string(string):
    #print(string[::-1])
    return string[::-1]
    
ans = reverse_string("Hello")
print(ans)

# Mirror

def reverseString(string):
    size = len(s)
	# Reverse string like a reflection
    for i in range(size//2):
        s[i], s[-i-1] = s[-i-1], s[i]
        
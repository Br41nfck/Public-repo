# Reverse integer
# Input: -1337
# Output: -7331

def reverse_int(integer):
    sign = [1,-1][integer < 0]
    out = sign * int(str(abs(integer))[::-1])

ans = reverse_int(-1337)
print(ans) # -7331
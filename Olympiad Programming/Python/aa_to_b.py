# Program change "aa" to "b"

"""
Example: aaaa = bb = c 
Description: aaaa = aa aa = b b = bb = c
Every time the program finds two identical characters,
it changes them to the character after the found ones.
"""

from string import ascii_lowercase
 
def aa_to_b(inp):
    try:
        nstring = [ascii_lowercase.index(s) for s in inp]
    except:
        return
    key = 0
    while True:
        #nstring.sort()
        if key >= len(nstring)-1 or len(nstring) <= 1:
            break
            
        if nstring[key] == nstring[key+1]:
            nstring[key] = nstring[key] + 1 
            if nstring[key] >= len(ascii_lowercase):
                nstring[key] = 0
            nstring.pop(key+1)
            key = 0
            
        else:
            key = key + 1
    return "".join([ascii_lowercase[n] for n in nstring])


user_string = input("Enter string:")
out = aa_to_b(str(user_string))
print("User_string:",user_string)
print("Changed string:",out)
        

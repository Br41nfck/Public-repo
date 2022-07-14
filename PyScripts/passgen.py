# Password Generator
from random import *
import string as st
chars = st.ascii_letters + st.punctuation + st.digits
psswd = "".join(choice(chars) for x in range(randint(8,24)))
print(psswd)


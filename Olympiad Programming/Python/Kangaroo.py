#!/bin/python3

import math
import os
import random
import re
import sys

def kangaroo(x1, v1, x2, v2):
    exist = False
    while(True):
        if x1 == x2:
            exist = True
            break
        if (v1 > v2 and x1 > x2) or (v2 > v1 and x2 > x1) or (v2 == v1 and x2 != x1):
            break
        x1 += v1
        x2 += v2
    
    if exist:
       return 'YES'
    else:
       return 'NO'
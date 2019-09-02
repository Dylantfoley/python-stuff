#easiest way is using numpy since it handles matrices better
import numpy as np
def rotateImage(a):
    a = np.rot90(a,k=3)# k is number of rotations
    return a
a = [[33,35,8,24,19,1,3,1,4,5],
 [25,27,40,25,17,35,20,3,19,3],
 [9,1,9,30,9,25,32,12,15,22],
 [30,47,25,10,18,1,19,17,43,17],
 [40,46,42,34,18,48,29,40,31,39],
 [37,42,37,19,45,1,4,46,48,13],
 [8,26,31,46,44,24,34,29,12,25],
 [45,48,36,12,33,12,4,45,22,37],
 [33,15,34,25,34,8,50,48,30,28],
 [18,19,22,29,15,43,38,30,8,47]]
b = rotateImage(a)
for i in range(0,len(b)):
    print(b[i])
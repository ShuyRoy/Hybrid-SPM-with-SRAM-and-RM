# a = [5,6,7,4,3,8,8,8,5]
#
# b = 10.23
# c = 3.94
# # d = a/b
# d = round(b/c,2)
# print(d)


# g = {1:4,2:4,3:2}
# g.pop(1)
# print(g)
import random

a = [1,2,3,4,5,6]
b = [7,8,9,10,11,12,13,14,15]
i = 0
c = []
while i < len(a):
    gap = random.randint(1,3)
    c.extend(a[i:i+gap])
    c.extend(b[i:i+gap])
    i = i + gap

c.extend(b[len(a):])
print(len(a),len(b),c,len(c))
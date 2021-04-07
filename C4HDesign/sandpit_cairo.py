import cmath as c
import math as m

z1 = complex(0,0)
z2 = complex(2,2)
z3 = complex(0,2)
z4 = complex(2,0)
z_list = [z1, z2, z3, z4]
print(z_list)
# z_list.clear()
print(z_list)
if z_list:
    print('yes')
else:
    print('no')

print(int(z2 in z_list))
print(z_list[z2 in z_list])
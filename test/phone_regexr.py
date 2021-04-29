import re

pattern = re.compile("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$")
string = '0978627659a'
if pattern.match(string):
    print('matched')

else:
    print('not matched')

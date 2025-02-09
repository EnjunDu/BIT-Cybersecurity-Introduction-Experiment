num = input()
if num[0] == '-':
    is_negative = True
    num = num[1:]
else:
    is_negative = False

reversed_num = num[::-1]

if is_negative:
    reversed_num = '-' + reversed_num

print(reversed_num)
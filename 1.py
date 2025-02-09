def method1(B,H):
    return B * H / 2

def method2(a,b,g):
    from math import sin,radians
    return a * b * sin(radians(g)) / 2

def method3(a,b,c):
    from math import sqrt
    p = (a + b + c) / 2
    return sqrt(p * (p - a)*(p - b)*(p - c))

print('**********************************************')
print('****      欢迎进入三角形面积计算程序      ****')
print('**********************************************')
print('1. 退出')
print('2. 三角形面积（已知底边和高）')
print('3. 三角形面积（已知两条边长以及夹角）')
print('4. 三角形面积（已知三条边长）')
while True:
    choice = input()
    if choice == '1':
        print('choice:Bye Bye!')
        break
    elif choice == '2':
        B = eval(input())
        H = eval(input())
        print('choice:Base:Height:The area is',method1(B,H))
    elif choice == '3':
        a = eval(input())
        b = eval(input())
        g = eval(input())
        print('choice:A:B:Gamma:The area is',method2(a,b,g))
    elif choice == '4':
        a = eval(input())
        b = eval(input())
        c = eval(input())
        print('choice:A:B:C:The area is',method3(a,b,c))
    else:
        break
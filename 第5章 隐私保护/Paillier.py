import random
import math
def keygen(input_bits):
    def is_prime(n, k=14):
        #The accuracy of the Miller-Rabin test after k iterations is 1 - (1/2^k). Empirical testing has shown that when k is set to 14, the accuracy of the test reaches 99.99%.
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for i in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for j in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    def generate_prime(bits):
        while True:
            p = random.getrandbits(bits)
            # 确认p是素数
            p |= 1
            if is_prime(p):
                return p

    def create_pq(bits):
        while True:
            p = generate_prime(bits)
            q = generate_prime(bits)
            if p != q:
                # 计算 gcd(p*q, (p-1)*(q-1))
                if math.gcd(p * q, (p - 1) * (q - 1)) == 1:
                    return p, q
    def calculate_miu(p, q, N, lambda_1):
        # mo zhi shu yun suan
        def mod_exp(base, exponent, modulus):
            result = 1
            base = base % modulus
            while exponent > 0:
                if exponent % 2 == 1:
                    result = (result * base) % modulus
                exponent = exponent >> 1
                base = (base * base) % modulus
            return result

        # mo ni yun suan
        def mod_inv(a, m):
            m0, x0, x1 = m, 0, 1
            while a > 1:
                q = a // m
                m, a = a % m, m
                x0, x1 = x1 - q * x0, x0
            return x1 + m0 if x1 < 0 else x1

        # calculate miu
        g = random.randint(2, N - 1)
        miu = mod_inv(((mod_exp(g, lambda_1, N ** 2) - 1) // N), N)

        return miu,g

    p, q = create_pq(input_bits)
    N=p*q
    lambda_1=abs((p-1)*(q-1))//math.gcd((p-1),(q-1))
    miu,g = calculate_miu(p, q, N, lambda_1)

    return N, g ,lambda_1,miu

def encrypt(m,N,g):
    r = random.randint(1, N**2 - 1)
    while math.gcd(r, N**2) != 1:
        r = random.randint(1, N**2 - 1)
    c = (pow(g, m, N**2) * pow(r, N, N**2)) % (N**2) #加密密文
    return c

def decrypt(c,lambda_1,N,miu):
    decrypted_m = ((pow(c, lambda_1, N**2) - 1) * miu // N) % N
    return decrypted_m

def main():
    N,g,lambda_1,miu=keygen(1024)

    m1=eval(input("请输入第一个明文"))
    m2=eval(input("请输入第二个明文"))

    c1=encrypt(m1,N,g)
    c2=encrypt(m2,N,g)

    print("对第一个明文加密后得到密文:{}".format(c1))
    print("对第二个明文加密后得到密文:{}".format(c2))

    c=c1*c2

    print("两密文相乘得到:{}".format(c))

    m=decrypt(c,lambda_1,N,miu)

    print("两密文相乘后解密得到的明文为:{}".format(m))

if __name__ == "__main__":
    main()

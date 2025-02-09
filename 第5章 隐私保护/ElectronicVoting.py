import time
import Paillier

print("***************************此程序模拟了基于Paillier算法的匿名电子投票的流程:*****************************************")
print("首先每位投票者为候选人投票并将结果加密发送给计票人。每人只有1张选票，选票上被投票的候选者得到1张选票，其他候选者得到0张选票;")
print("然后计票人将所有选票上对应候选人的加密的投票结果相乘，并将加密的统计结果发送给公布人;")
print("最后公布人对统计的票数进行解密并公布;")
print("***************************************************************************************************************************")

houxuan_num=eval(input("请设置候选人数："))
toupiao_num=eval(input("请设置投票人数："))

houxuanpiao=[0 for i in range (houxuan_num+1)]

for i in range(1,toupiao_num+1):
    print("----------请第{}名投票者为候选者投票----------".format(i))
    for j in range(1,houxuan_num+1):
        houxuanpiao[j]+=eval(input("请为第{}名候选者投票:".format(j)))

print("对该投票结果进行加密并发送给计票人")
print("-------计票人计票完成并将加密后的投票结果发给公布人-------")
print("加密后的投票结果为：")

N, g, lambda_1, miu = Paillier.keygen(1024)
encrypted_m=[0 for i in range (houxuan_num+1)]
decrypt_c=[0 for i in range (houxuan_num+1)]

for i in range (1,houxuan_num+1):
    encrypted_m[i]=Paillier.encrypt(houxuanpiao[i],N,g)
    print("第{}位候选人获得的选票票数的加密结果为：{}".format(i,encrypted_m[i]))
    time.sleep(1)

print("-------公布人解密计票结果并公布最终的投票结果-------")

for i in range (1,houxuan_num+1):
    decrypt_c[i]=Paillier.decrypt(encrypted_m[i],lambda_1,N,miu)
    print("第{}位候选人获得了{}张选票".format(i,decrypt_c[i]))
    time.sleep(1)

max_index=decrypt_c.index(max(decrypt_c))

print("最终第{}位候选人获得的选票最多，为{}张".format(max_index,decrypt_c[max_index]))

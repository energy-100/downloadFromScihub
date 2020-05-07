
import uuid
# def get_mac_address():
#     mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
#     # mac1 = (int(mac[0:2], 16) * 1218) % (256)
# #     print(int(mac[0:2], 16))
# #     print((int(mac[0:2], 16) * 1218))
# #     print(mac1)
# #     print(int(mac[0:2],16))
# #     print(r"/x"+r'/x'.join([hex(ord(c)).replace('0x', '') for c in mac])
# # )
# #     print(type(mac))
# #     return "".join([mac[e:e+2] for e in range(0,11,2)])
#     # return ":".join([mac[e:e+2] for e in range(0,11,2)])
#
#
#     mac1 = str((int(mac[0:2], 16) * 1218) % (256))
#     mac2 = str((int(mac[2:4], 16) * 1219) % (256))
#     mac3 = str((int(mac[4:6], 16) * 1220) % (256))
#     mac4 = str((int(mac[6:8], 16) * 1221) % (256))
#     mac5 = str((int(mac[8:10], 16) * 1222) % (256))
#     mac6 = str((int(mac[10:12], 16) * 1223) % (256))
#     macfinall = mac1 + mac2 + mac3 + mac4 + mac5 + mac6
#     print(macfinall)
#     return
# print(get_mac_address())
#
# # print(131544%256)

mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
print(mac)
add1=str((47*3+1000))
add2=str((105*3+1000))
add3=str((38*3+1000))
add4=str((117*3+1000))
add=add1+add2+add3+add4
print(add)



strr="root-1234-3306-long_distance_data"
a=list(map(ord, strr))
astr=""
for item in a:
    items=""
    if item <10:
        items="00"+str(item)
    elif item<100:
        items="0"+str(item)
    else:
        items=""+str(item)
    astr=astr+items

print(astr)
print(a)
strr=add+astr
add1 = str(int((int(strr[0:4]) - 1000) / 3))
add2 = str(int((int(strr[4:8]) - 1000) / 3))
add3 = str(int((int(strr[8:12]) - 1000) / 3))
add4 = str(int((int(strr[12:16]) - 1000) / 3))
address = add1 + "." + add2 + "." + add3 + "." + add4
print(address)
databaseinf = strr[16:]
ass = []
for i in range(int(len(databaseinf) / 3)):
    reallyi = i * 3
    ass.append(int(databaseinf[int(reallyi):int(reallyi + 3)]))
print("".join(map(chr, ass)))



    # "47.105.38.117",
    # "root",
    # "1234",
    # "long_distance_data",
    # port=3306,
    # charset='utf8'
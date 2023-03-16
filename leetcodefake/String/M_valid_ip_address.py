'''
 "1921680" ->
 ["1.9.216.80", "1.92.16.80", "1.92.168.0", 
 "19.2.16.80", "19.2.168.0", "19.21.6.80", "19.21.68.0", 
 "19.216.8.0", "192.1.6.80", "192.1.68.0", "192.16.8.0"]
注意一点 valid_ip.append(c)的时候因为c是列表 会出现当i=1时 第二个append到 valid_ip 的元素会影响第一个元素

'''


def validIPAddresses(string):
    valid_ip = []
    for i in range(1, 4):
        c = [""]*4
        c[0] = string[0:i]
        if not isValidPart(c[0]):
            continue
        for j in range(i+1, i+min(len(string)-i, 4)):
            c[1] = string[i:j]
            if not isValidPart(c[1]):
                continue
            for k in range(j+1, j+min(len(string)-j, 4)):
                c[2] = string[j:k]
                c[3] = string[k:]
                if not isValidPart(c[2]) or not isValidPart(c[3]):
                    continue
                valid_ip.append(".".join(c))

    return valid_ip


def isValidPart(string):
    number = int(string)
    if number > 255:
        return False
    if len(string) != len(str(number)):
        return False
    return True

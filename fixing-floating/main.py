import sys


def perevod1(num, x):
    dvnum = ''
    for i in range(2, len(num)):
        i = bin(int(num[i], 16))[2:]
        if len(i) < 4:
            i = '0' * (4 - len(i)) + i
        dvnum += i
    if x == 'f':
        dvnum = '0' * (32 - len(dvnum)) + dvnum
    elif x == 'h':
        dvnum = '0' * (16 - len(dvnum)) + dvnum
    return dvnum


def perevod2(num):
    dvnum = ''
    for i in range(len(num) // 4):
        dvnum += hex(int(num[i * 4:(i * 4 + 4)], 2))[2:]
    return dvnum


def hr(num):
    sign = num[0]
    exp = num[1:6]
    mant = num[6:]
    return [sign, exp, mant]


def fr(num):
    sign = num[0]
    exp = num[1:9]
    mant = num[9:]
    return [sign, exp, mant]


def round(sign, a, x, n):
    if sign % 2 == 0:
        if x == 2:
            if a[n + 1:].count('1') != 0:
                k = bin(int(a[:n + 1], 2) + int('1', 2))[2:]
                if len(k) > n + 1:
                    return k[1:n + 1] + 'k'
                else:
                    return k[1:n + 1]
            else:
                return a[1:n + 1]
        elif x == 1:
            if a[n + 1] == '1':
                k = bin(int(a[:n + 1], 2) + int('1', 2))[2:]
                if len(k) > n + 1:
                    return k[1:n + 1] + 'k'
                else:
                    return k[1:n + 1]
            else:
                return a[1:n + 1]
        else:
            return a[1:n + 1]
    else:
        if x == 3:
            if a[n + 1:].count('1') != 0:
                k = bin(int(a[:n + 1], 2) + int('1', 2))[2:]
                if len(k) > n + 1:
                    return k[1:n + 1] + 's'
                else:
                    return k[1:n + 1]
            else:
                return a[1:n + 1]
        elif x == 1:
            if a[n + 1] == '1':
                k = bin(int(a[:n + 1], 2) + int('1', 2))[2:]
                if len(k) > n + 1:
                    return k[1:n + 1] + 's'
                else:
                    return k[1:n + 1]
            else:
                return a[1:n + 1]
        else:
            return a[1:n + 1]


def star(a, b, x, r):
    if x == 'f':
        a, b = fr(perevod1(a, x)), fr(perevod1(b, x))
    else:
        a, b = hr(perevod1(a, x)), hr(perevod1(b, x))
    mantlen, explen = len(a[2]), len(a[1]) - 1
    mk = mantlen
    sign = int(a[0]) ^ int(b[0])
    if (a[1] + a[2]).count('1') == 0 and not (b[1].count('0') == 0 and b[2].count('1') == 0) or (
            (b[1] + b[2]).count('1') == 0 and not (a[1].count('0') == 0 and a[2].count('1') == 0)):
        if x == 'f':
            return '0x0.000000p+0' if sign % 2 == 0 else '-0x0.000000p+0'
        else:
            return '0x0.000p+0' if sign % 2 == 0 else '-0x0.000p+0'
    elif (a[1].count('0') == 0 and a[2].count('1') != 0) or (b[1].count('0') == 0 and b[2].count('1') != 0):
        return 'nan'
    elif ((a[1] + a[2]).count('1') == 0 and b[1].count('0') == 0 and b[2].count('1') == 0) or (
            (b[1] + b[2]).count('1') == 0 and a[1].count('0') == 0 and a[2].count('1') == 0):
        return 'nan'
    elif (a[1].count('0') == 0 and a[2].count('1') == 0) or (b[1].count('0') == 0 and b[2].count('1') == 0):
        return 'inf' if sign % 2 == 0 else '-inf'
    else:
        if a[1].count('1') != 0 and b[1].count('1') != 0:
            mant = bin(int('1' + a[2], 2) * int('1' + b[2], 2))[2:]
            k = len(mant) - 2 * mantlen - 1
        elif a[1].count('1') != 0 and b[1].count('1') == 0:
            mant = bin(int('1' + a[2], 2) * int(b[2][b[2].find('1'):] + '0' * (mantlen - b[2].find('1')), 2))[2:]
            k = - b[2].find('1')
        elif a[1].count('1') == 0 and b[1].count('1') != 0:
            mant = bin(int('1' + b[2], 2) * int(a[2][a[2].find('1'):] + '0' * (mantlen - a[2].find('1')), 2))[2:]
            k = - a[2].find('1')
        else:
            mant = bin(int(b[2][b[2].find('1'):] + '0' * (b[2].find('1') + 1), 2) * int(
                a[2][a[2].find('1'):] + '0' * (a[2].find('1') + 1), 2))[2:]
            k = - a[2].find('1') - b[2].find('1')

        exp = (int(a[1], 2) + int(b[1], 2) - 2 * (2 ** explen - 1)) + k
        if len(mant) < 2 * mantlen:
            mant += '0' * 2 * mantlen
        if int(exp) < - 2 ** explen + 1:
            mantlen -= (-2 ** (explen + 1) - int(exp))

        mant = round(sign, mant, r, mk)
        if mant[-1] == 'k':
            exp += 1
            mant = mant[:-1]
        elif mant[-1] == 's':
            exp -= 1
            mant = mant[:-1]
        if mantlen != mk:
            mant += '0' * (mk - mantlen + 1)
        if x == 'f':
            mant = perevod2(mant + '0')
        else:
            mant = perevod2(mant + '00')

        if exp >= 0:
            exp = '+' + str(exp)

        if int(exp) >= 2 ** explen:
            return 'inf' if sign % 2 == 0 else '-inf'
        elif (x == 'f' and int(exp) < -149) or (x == 'h' and int(exp) < - 24):
            if sign % 2 == 0 and r == 2:
                return '0x1.000p-24' if x == 'h' else '0x1.000000p-149'
            elif sign % 2 != 0 and r == 3:
                return '-0x1.000p-24' if x == 'h' else '-0x1.000000p-149'
            elif x == 'f':
                return '0x0.000000p+0' if sign % 2 == 0 else '-0x0.000000p+0'
            else:
                return '0x0.000p+0' if sign % 2 == 0 else '-0x0.000p+0'
        else:
            return '0x1.' + mant + 'p' + str(exp) if sign % 2 == 0 else '-0x1.' + mant + 'p' + str(exp)


def slash(a, b, x, r):
    if x == 'f':
        a, b = fr(perevod1(a, x)), fr(perevod1(b, x))
    else:
        a, b = hr(perevod1(a, x)), hr(perevod1(b, x))
    mantlen, explen = len(a[2]), len(a[1]) - 1
    mk = mantlen
    sign = int(a[0]) ^ int(b[0])
    if ((a[1] + a[2]).count('1') == 0 and (b[1] + b[2]).count('1') == 0) or (
            a[2].count('1') == 0 and b[2].count('1') == 0 and a[1].count('0') == 0 and b[1].count('0') == 0):
        return 'nan'
    elif (a[1].count('0') == 0 and a[2].count('1') != 0) or (b[1].count('0') == 0 and b[2].count('1') != 0):
        return 'nan'
    elif (a[1] + a[2]).count('1') == 0 and (b[1] + b[2]).count('1') != 0:
        if x == 'f':
            return '0x0.000000p+0' if sign % 2 == 0 else '-0x0.000000p+0'
        else:
            return '0x0.000p+0' if sign % 2 == 0 else '-0x0.000p+0'
    elif (b[2] + b[1]).count('1') == 0:
        return '-inf' if int(a[0]) * int(b[0]) % 2 != 0 else 'inf'
    else:
        k = 0
        if int(a[1], 2) == int(b[1], 2) and int(a[2], 2) == int(b[2], 2):
            if x == 'h':
                return '1x0.000p+0' if sign % 2 == 0 else '-1x0.000p+0'
            else:
                return '1x0.000000p+0' if sign % 2 == 0 else '-1x0.000000p+0'
        if int(a[2], 2) == 0 and int(b[2], 2) == 0:
            k -= 2
        if a[1].count('1') != 0 and b[1].count('1') == 0:
            b[2] = b[2][b[2].find('1'):] + '0' * (mantlen - len(b[2][b[2].find('1'):]) + 1)
            a[2] = '1' + a[2]
            k -= b[2].find('1')
        elif a[1].count('1') == 0 and b[1].count('1') != 0:
            a[2] = a[2][a[2].find('1'):] + '0' * (mantlen - len(a[2][a[2].find('1'):]) + 1)
            b[2] = '1' + b[2]
            k -= a[2].find('1')
        elif a[1].count('1') == 0 and b[1].count('1') == 0:
            a[2] = a[2][a[2].find('1'):] + '0' * (mantlen - len(a[2][a[2].find('1'):]) + 1)
            b[2] = b[2][b[2].find('1'):] + '0' * (mantlen - len(b[2][b[2].find('1'):]) + 1)
            k -= a[2].find('1') + b[2].find('1')
        else:
            a[2] = '1' + a[2]
            b[2] = '1' + b[2]
            k += 2

        mant = bin(int(a[2], 2) * 2 ** (2 * mantlen * 2) // int(b[2], 2))[2:]
        if int(a[2][:mantlen + 1], 2) < int(b[2][:mantlen + 1], 2):
            k -= 1

        exp = (int(a[1], 2) - int(b[1], 2)) - k

        mant = round(sign, mant, r, mantlen)
        if mant[-1] == 'k':
            exp -= 1
            mant = mant[:-1]
        elif mant[-1] == 's':
            exp += 1
            mant = mant[:-1]
        if mantlen != mk:
            mant += '0' * (mk - mantlen + 1)
        if x == 'f':
            mant = perevod2(mant + '0')
        else:
            mant = perevod2(mant + '00')

        if exp >= 0:
            exp = '+' + str(exp)

        if int(exp) > 2 ** explen:
            return 'inf' if sign % 2 == 0 else '-inf'
        elif (x == 'f' and int(exp) < -149) or (x == 'h' and int(exp) < - 24):
            if sign % 2 == 0 and r == 2:
                return '0x1.000p-24' if x == 'h' else '0x1.000000p-149'
            elif sign % 2 != 0 and r == 3:
                return '-0x1.000p-24' if x == 'h' else '-0x1.000000p-149'
            elif x == 'f':
                return '0x0.000000p+0' if sign % 2 == 0 else '-0x0.000000p+0'
            else:
                return '0x0.000p+0' if sign % 2 == 0 else '-0x0.000p+0'
        else:
            return '0x1.' + mant + 'p' + str(exp) if sign % 2 == 0 else '-0x1.' + mant + 'p' + str(exp)


def plus(a, b, x, r):
    if x == 'f':
        a, b = fr(perevod1(a, x)), fr(perevod1(b, x))
    else:
        a, b = hr(perevod1(a, x)), hr(perevod1(b, x))
    mantlen, explen = len(a[2]), len(a[1])
    if int(a[0], 2) ^ int(b[0], 2) % 2 != 0 and (
            a[1].count('0') == 0 and b[1].count('0') == 0 and a[2].count('1') == 0 and b[2].count('1') == 0):
        return 'nan'
    elif (a[1].count('0') == 0 and a[2].count('1') != 0) or (b[1].count('0') == 0 and b[2].count('1') != 0):
        return 'nan'
    elif int(a[0], 2) ^ int(b[0], 2) % 2 == 0 and (
            a[1].count('0') == 0 and b[1].count('0') == 0 and a[2].count('1') == 0 and b[2].count('1') == 0):
        return 'inf' if int(a[0], 2) % 2 == 0 else '-inf'
    elif (a[1] + a[2]).count('1') == 0 and (b[1] + b[2]).count('1') == 0:
        if x == 'f':
            return '0x0.000000p+0'  # if int(a[0], 2) ^ int(b[0], 2) % 2 == 0 else '-0x0.000000p+0'
        else:
            return '0x0.000p+0'  # if int(a[0], 2) ^ int(b[0], 2) % 2 == 0 else '-0x0.000p+0'
    elif (a[1] + a[2]).count('1') == 0:
        b = '0x' + perevod2(b[0] + b[1] + b[2])
        return star('0x3F800000', b, x, r) if x == 'f' else star('0x3C00', b, x, r)
    elif (b[1] + b[2]).count('1') == 0:
        a = '0x' + perevod2(a[0] + a[1] + a[2])
        return star('0x3F800000', a, x, r) if x == 'f' else star('0x3C00', a, x, r)
    else:
        if int(a[0]) == 0:
            sign1 = int(a[1], 2) * 2 ** mantlen + int(a[2], 2)
        else:
            sign1 = - (int(a[1], 2) * 2 ** mantlen + int(a[2], 2))
        if int(b[0]) == 0:
            sign2 = int(b[1], 2) * 2 ** mantlen + int(b[2], 2)
        else:
            sign2 = - (int(b[1], 2) * 2 ** mantlen + int(b[2], 2))
        if sign1 + sign2 >= 0:
            sign = 0
        else:
            sign = -1
        if a[1].count('1') == 0 and b[1].count('1') != 0:
            i = a[2].find('1')
            a[2] = a[2][i + 1:] + '0' * (i + 2)
            a[1] = int(a[1], 2) - i - 1
            b[1] = int(b[1], 2)
        elif a[1].count('1') != 0 and b[1].count('1') == 0:
            i = b[2].find('1')
            b[2] = b[2][i + 1:] + '0' * (i + 2)
            b[1] = int(b[1], 2) - i - 1
            a[1] = int(a[1], 2)
        elif a[1].count('1') == 0 and b[1].count('1') == 0:
            i = a[2].find('1')
            a[2] = a[2][i + 1:] + '0' * (i + 2)
            a[1] = int(a[1], 2) - i - 1
            j = b[2].find('1')
            b[2] = b[2][j + 1:] + '0' * (j + 2)
            b[1] = int(b[1], 2) - j - 1
        else:
            a[1] = int(a[1], 2)
            b[1] = int(b[1], 2)
        xmin = min(a[1], b[1])
        xmax = max(a[1], b[1])
        k = 0
        if a[1] == b[1]:
            if sign1 * sign2 < 0:
                mant = bin(abs(int('1' + a[2], 2) - int('1' + b[2], 2)))[2:]
            else:
                mant = bin(abs(int('1' + a[2], 2) + int('1' + b[2], 2)))[2:]
            if len(mant) > mantlen:
                k += len(mant) - mantlen - 1

            elif len(mant) < mantlen:
                k -= mantlen - len(mant) + 1
                mant += '0' * (mantlen - len(mant))

            if int(mant, 2) == 0:
                return '0x0.000p+0' if x == 'h' else '0x0.000000p+0'
        else:
            if sign1 * sign2 >= 0:
                mant = bin(abs(int('1' + a[2] + '0' * (a[1] - xmin), 2) + int('1' + b[2] + '0' * (b[1] - xmin), 2)))[2:]
            else:
                mant = bin(abs(int('1' + a[2] + '0' * (a[1] - xmin), 2) - int('1' + b[2] + '0' * (b[1] - xmin), 2)))[2:]

            if len(mant) < xmax - xmin + mantlen + 1:
                i = xmax - xmin + mantlen + 1 - len(mant)
                k -= i
                mant = mant + '0' * i
            exp = xmax - xmin
            if len(mant) > mantlen:
                exp += 1
            k += len(mant) - mantlen - 1
        mant = round(sign, mant, r, mantlen)
        exp = xmin + k - (2 ** (explen - 1) - 1)
        if mant[-1] == 'k':
            exp += 1
            mant = mant[:-1]
        elif mant[-1] == 's':
            exp += 1
            mant = mant[:-1]
        mant += '0' * (mantlen - len(mant) + 1)
        if x == 'f':
            mant = perevod2(mant + '0')
        else:
            mant = perevod2(mant + '00')

        if exp >= 0:
            exp = '+' + str(exp)

        if int(exp) > 2 ** (explen - 1) - 1:
            return 'inf' if sign % 2 == 0 else '-inf'
        elif (x == 'f' and int(exp) < -149) or (x == 'h' and int(exp) < - 24):
            if sign % 2 == 0 and r == 2:
                return '0x1.000p-24' if x == 'h' else '0x1.000000p-149'
            elif sign % 2 != 0 and r == 3:
                return '-0x1.000p-24' if x == 'h' else '-0x1.000000p-149'
            elif x == 'f':
                return '0x0.000000p+0'
            else:
                return '0x0.000p+0'
        else:
            return '0x1.' + mant + 'p' + str(exp) if sign != -1 else '-0x1.' + mant + 'p' + str(exp)


def minus(a, b, x, r):
    if x == 'f':
        b = fr(perevod1(b, x))
    else:
        b = hr(perevod1(b, x))
    b[0] = str((int(b[0], 2) - 1) % 2)
    b = '0x' + perevod2(b[0] + b[1] + b[2])
    return plus(a, b, x, r)


def fix(num, a, b):
    num = perevod1(num, 1)
    num = '0' * (a + b - len(num)) + num
    return num[-a - b:]


def Print(num, a, b, x, r, sign):
    k = 0
    if r == 1:
        num = fix(num, a, b)
        numa = int(num[1:], 2) - int(num[0], 2) * 2 ** (a + b - 1)
        if numa < 0:
            num = bin(int('1' * (a + b), 2) - int(num, 2) + 1)[2:]
            num = '0' * (a + b - len(num)) + num
            if x == 2 or x == 3:
                x = 6 // x
            sign = -1
            k = 1
        numa = int(num[:a], 2)
        numb = num[-b:]

    else:
        numa = int(num[:a], 2)
        numb = num[-b:]
    numb += '0' * 100

    if sign == -1 and k == 0 and (x == 2 or x == 3):
        x = 6 // x

    tail = 0
    for i in range(100):
        tail += int(numb[i]) * 2 ** (99 - i)
    tail *= 10 ** 1000 // 2 ** 100
    tail = str(tail)
    i = 0

    if (numb[0] + numb[1] + numb[2] + numb[3] + numb[4]).count('1') == 0:
        i += 1
        if (numb[5] + numb[6] + numb[7] + numb[8] + numb[9] + numb[10]).count('1') <= 1:
            i += 1
    elif (numb[0] + numb[1] + numb[2]).count('1') == 0 and (numb[3] + numb[4]).count('1') == 1:
        i += 1
    tail = '0' * i + tail
    tail += '000'

    if x == 0 or x == 3:
        tail = tail[:3]
    elif x == 1:
        if int(tail[3]) > 5:
            tail = str(int(tail[:3]) + 1)
            if len(tail) > 3:
                numa += 1
            tail = tail[:3]
        elif int(tail[3]) == 5:
            if int(tail[2]) % 2 == 0:
                tail = tail[:3]
            else:
                tail = str(int(tail[:3]) + 1)
                if len(tail) > 3:
                    numa += 1
                tail = tail[:3]
        else:
            tail = tail[:3]
    else:
        if int(tail[3:], 10) == 0:
            tail = tail[:3]
        else:
            tail = str(int(tail[:3]) + 1)
            if len(tail) > 3:
                numa += 1
            tail = tail[:3]
    tail = '0' * (3 - len(tail)) + tail
    return '-' + str(numa) + '.' + tail if sign == -1 else str(numa) + '.' + tail


def plus_fix(num1, num2, a, b, x):
    num1 = fix(num1, a, b)
    num2 = fix(num2, a, b)

    numa = int(num1[1:], 2) - int(num1[0]) * 2 ** (a + b - 1) + int(num2[1:], 2) - int(num2[0]) * 2 ** (a + b - 1)
    if numa >= 0:
        num = bin(numa)[2:]
        if len(num) < a + b:
            num = '0' * (a + b - len(num)) + num
        numb = num[-b:]
        numa = num[-a - b:-b]
        sign = 1
    else:
        sign = -1
        num = bin(abs(numa))[2:]
        if len(num) < a + b:
            num = '0' * (a + b - len(num)) + num
        numb = num[-b:]
        numa = num[-a - b:-b]
    num = numa + numb
    if num[0] == '1':
        sign *= -1
        num = bin(int('1' * (a + b), 2) - int(num, 2) + 1)[2:]
        num = '0' * (a + b - len(num)) + num
    return Print(num, a, b, x, 0, sign)


def minus_fix(num1, num2, a, b, x):
    num2 = fix(num2, a, b)
    num = bin(int('1' * (a + b), 2) - int(num2, 2) + 1)[2:]
    num = '0' * (4 * (a + b) - len(num)) + num
    num2 = '0x' + perevod2(num)
    return plus_fix(num1, num2, a, b, x)


def star_fix(num1, num2, a, b, x):
    num1 = fix(num1, a, b)
    num2 = fix(num2, a, b)
    sign = 1

    if int(num1[0]) == 1:
        num1 = bin(int('1' * (a + b), 2) - int(num1, 2) + 1)[2:]
        num1 = '0' * (a + b - len(num1)) + num1
        if x == 2 or x == 3:
            x = 6 // x
        sign *= -1
    if int(num2[0]) == 1:
        num2 = bin(int('1' * (a + b), 2) - int(num2, 2) + 1)[2:]
        num2 = '0' * (a + b - len(num2)) + num2
        if x == 2 or x == 3:
            x = 6 // x
        sign *= -1
    num = bin(int(num1, 2) * int(num2, 2))[2:]
    if len(num) < a + 2 * b:
        num = '0' * (a + 2 * b - len(num)) + num
    num = num[- 2 * b - a:]
    numa = int(num[1:a], 2) - int(num[0]) * 2 ** (a - 1)
    numb = num[-2 * b:]
    if numa >= 0:
        if x == 0 or x == 3:
            numb = numb[:b]
        elif x == 1:
            if numb[b] == '1':
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
            else:
                numb = numb[:b]
        else:
            if numb[b:].count('1') == 0:
                numb = numb[:b]
            else:
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
    else:
        sign *= -1
        if x == 0 or x == 2:
            numb = numb[:b]
        elif x == 1:
            if numb[b] == '1':
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
            else:
                numb = numb[:b]
        else:
            if numb[b:].count('1') == 0:
                numb = numb[:b]
            else:
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numa += 1
                    numb = numb[1:]
        """numb = bin(int('1' * b, 2) - int(numb, 2) + 1)[2:]
        numb = '0' * (b - len(numb)) + numb
        numa += 1"""

    numa = bin(abs(numa))[2:]
    numa = '0' * (a - len(numa)) + numa
    num = numa + numb

    if num[0] == '1':
        sign *= -1
        num = bin(int('1' * (a + b), 2) - int(num, 2) + 1)[2:]
        num = '0' * (a + b - len(num)) + num
    return Print(num, a, b, x, 0, sign)


def slash_fix(num1, num2, a, b, x):
    num1 = fix(num1, a, b)
    num2 = fix(num2, a, b)
    sign = 1
    if int(num2, 2) == 0:
        return 'error'

    if int(num1[0], 2) == 1:
        num1 = bin(int('1' * (a + b), 2) - int(num1, 2) + 1)[2:]
        num1 = '0' * (a + b - len(num1)) + num1
        if x == 2 or x == 3:
            x = 6 // x
        sign *= -1
    if int(num2[0], 2) == 1:
        num2 = bin(int('1' * (a + b), 2) - int(num2, 2) + 1)[2:]
        num2 = '0' * (a + b - len(num2)) + num2
        if x == 2 or x == 3:
            x = 6 // x
        sign *= -1
    numw = bin(int(num1, 2) // int(num2, 2))[2:]
    num = bin(int(num1 + '0' * 200, 2) // int(num2, 2))[2:]

    if numw != '0':
        numa = int(num[:len(numw)], 2)
        numb = num[len(numw):]
    else:
        numa = 0
        numb = num 

    numb += '0' * 32
    if numa >= 0:
        if x == 0 or x == 3:
            numb = numb[:b]
        elif x == 1:
            if numb[b] == '1':
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
            else:
                numb = numb[:b]
        else:
            if numb[b:].count('1') == 0:
                numb = numb[:b]
            else:
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
    else:
        sign *= -1
        if x == 0 or x == 2:
            numb = numb[:b]
        elif x == 1:
            if numb[b] == '1':
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numb = numb[1:]
                    numa += 1
            else:
                numb = numb[:b]
        else:
            if numb[b:].count('1') == 0:
                numb = numb[:b]
            else:
                numb = bin(int(numb[:b], 2) + 1)[2:]
                if len(numb) > b:
                    numa += 1
                    numb = numb[1:]
        numb = bin(int('1' * b, 2) - int(numb, 2) + 1)[2:]
        numb = '0' * (b - len(numb)) + numb
        numa += 1

    numa = bin(abs(numa))[2:]
    numa = '0' * (a - len(numa)) + numa
    num = numa + numb

    if num[0] == '1':
        sign *= -1
        num = bin(int('1' * (a + b), 2) - int(num, 2) + 1)[2:]
        num = '0' * (a + b - len(num)) + num
    return Print(num, a, b, x, 0, sign)


if __name__ == "__main__":
    args = sys.argv[1:]
    s = args
    try:
        (len(s) == 3 or len(s) == 5)
    except Exception:
        print('format error')
        exit(0)

    try:
        ((int(s[1]) in [0, 1, 2, 3]) and (len(s) == 5 and s[3] in ['+', '-', '*', '/']))
    except Exception:
        print('data error')
        exit(0)

    if len(s) == 3:
        if s[0] == 'f':
            print(star('0x3F800000', s[2], 'f', int(s[1])))
        elif s[0] == 'h':
            print(star('0x3C00', s[2], 'h', int(s[1])))
        else:
            k = s[0].split('.')
            print(Print(s[2], int(k[0]), int(k[1]), int(s[1]), 1, 1))
    else:
        if s[0] == 'f' or s[0] == 'h':
            if s[3] == '*':
                print(star(s[2], s[4], s[0], int(s[1])))
            elif s[3] == '/':
                print(slash(s[2], s[4], s[0], int(s[1])))
            elif s[3] == '+':
                print(plus(s[2], s[4], s[0], int(s[1])))
            else:
                print(minus(s[2], s[4], s[0], int(s[1])))
        else:
            k = s[0].split('.')
            if s[3] == '*':
                print(star_fix(s[2], s[4], int(k[0]), int(k[1]), int(s[1])))
            elif s[3] == '/':
                print(slash_fix(s[2], s[4], int(k[0]), int(k[1]), int(s[1])))
            elif s[3] == '+':
                print(plus_fix(s[2], s[4], int(k[0]), int(k[1]), int(s[1])))
            else:
                print(minus_fix(s[2], s[4], int(k[0]), int(k[1]), int(s[1])))

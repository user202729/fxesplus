import lib_570esp

from collections import defaultdict

working = ['log(', 'ln(', 'sin(', 'cos(', 'tan(', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Pol(', 'Rec(', '+', '-', '`', 'A', 'B', 'C', 'D', 'E', 'F', 'X', 'Y', 'M', ',', 'sin⁻(', 'cos⁻(', 'tan⁻(', 'Ran#', 'π', 'RanInt#(', '%', 'Ans', '𝐞', '×', '÷', '!', '=', ':', '×⏨', '.']

fasts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '×', '÷', 'Ans', '×⏨', 'DEL', '.', 'AC', 'EXE']

alts = {252: 'CALC', 221: 'Int', 212: '^-1', 219: 'logxx', 208: 'Frac', 211: 'sqrt(', 213: '^2', 248: 'ENG', 9: 'hyp', 250: 'S<>D', 238: 'M+', 237: 'EXE', 254: 'DEL', 230: 'AC', 237: 'EXE'}

working.extend(alts.values())

def get_npress(it):
    ans = 0
    for i in it:
        if to_key(i) in fasts: ans += 0.5
        elif i in alts: ans += 1
        else: ans += lib_570esp.get_npress(i)
    return ans

def to_key(i):
    if i in alts: return alts[i]
    return lib_570esp.to_key(i)

def generate_pairs():
    it = defaultdict(lambda: (float('inf'),))
    for i in range(256):
        if to_key(i) in working:
            for j in range(256):
                if to_key(j) in working:
                    it[(i + j) % 256] = min(it[(i + j) % 256], (get_npress((i, j)), (i, j)))
    return it

pairs = generate_pairs()

def get_pair(i):
    pair = pairs[i][1]
    return to_key(pair[0]) + ' ' + to_key(pair[1])

def format(i):
    ans = [['', 0]]
    for j in i:
        t = get_pair(j)
        if ans[-1][0] == t:
            ans[-1][1] += 1
        else:
            ans.append([t, 1])
    del ans[0]
    ans2 = []
    for i, j in ans:
        if j >= 5:
            ans2.append('%dx{%s}'%(j, i))
        else:
            ans2.extend([i] * j)
    return '\n'.join(ans2)+'\n'

if __name__ == '__main__':
    for i in range(256):
        try: print(get_pair(i))
        except IndexError: print('UNTYPEABLE')

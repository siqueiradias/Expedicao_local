a = [(1, 2), (2, 3), (3, 4)]
b = [(2, 5, 0), (7, 9, 1), (1, 2, 3)]
c = [(2, 5), (7, 9), (1, 2)]

for i in b:
    print(i[0:2])

print('*'*10)

d = []
for item in b:
    d.append(item[0:2])

print(d)

for num in a:
    if not num in d:
        print(num)

a = 0
b = 1
i = 0
while i < n:
    summa = a + b
    a = b
    b = summa
    i = i + 1
print(a)
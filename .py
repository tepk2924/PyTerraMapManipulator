with open("aaaaa", "wb") as f:
    f.write("시부랄".encode('utf-8'))

with open("aaaaa", 'rb') as f:
    B = f.read().decode('utf-8')

print(B)
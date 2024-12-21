out = []

try:
    print(out[-1])
    out.append(1)
    print(out[-1])
    out.append(2)
    out.append(3)
    out.append(4)
    out.append(5)
    print(out[-1])
except:
    print("something went wrong")

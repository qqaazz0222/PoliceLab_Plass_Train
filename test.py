arr = [0, 1, 2, 3, 9, 10, 11]
def get_range(arr):
    result = []
    temp = []
    prev = -2
    for t in arr:
        if t != prev + 1:
            if len(temp) > 0:
                result.append(temp)
                temp = []
            temp = [t, t]
        else:
            temp[1] = t
        if t == arr[-1]:
            result.append(temp)
        prev = t
    return result
            

print(get_range(arr))
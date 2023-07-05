def string_to_array(s):
    word = s.split()
    arr = []
    for x in word:
        if not x:
            arr.append("")
        else:
            arr.append(x)
            
    return arr

print(repr(string_to_array('')))
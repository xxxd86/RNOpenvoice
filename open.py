def readAllText():
    f2 = open("text.txt", encoding='utf-8')
    lines = f2.readlines()
    result = ""
    for line3 in lines:
        result += line3
    return result
if __name__ == '__main__':
    print(readAllText())
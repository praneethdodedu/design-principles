str = "Hello World How are you"

char_count = {}

for char in str:
    if char in char_count:
        char_count[char] = char_count.get(char) + 1
    else:
        char_count[char] = 1

for char in str:
    if char_count[char] == 1:
        print("first non repeating character is: ", char)
        break
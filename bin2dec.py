binary = input("You must input a binary string (example: 010101010). Only 0 and 1"
               "\nenter a num: ")
while len(binary) > 8:
    binary = input("enter a num less than 8 symbols: ")
binary2 = binary
binary3 = binary

print("Result with first logic")
result = int(binary, 2)
print(result)

print("Result with second logic")
decimal = 0
for digit in binary2:
    decimal = decimal*2 + int(digit)
print(decimal)
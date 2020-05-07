## lab file

def sum(numbers):
    n = len(numbers)
    sum = 0
    for i in range(n):
            sum += numbers[i]
    return sum

n = [1,2,3]
print('the sum of', n, 'is', sum(n))



## scopes and index


numbers = [1,2,3,4,5,6,7,8,9]

for number in numbers:
        if number % 2 == 0:
            print('the number ', number, "is even")
            print("its index is", numbers.index(number))
        else:
            print('the number ', number, "is odd")






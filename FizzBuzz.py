# FizzBuzz program
# This program prints numbers from 1 to 100.
# For multiples of three, it prints "fizz" instead of the number.
# For multiples of five, it prints "buzz" instead of the number.
# For multiples of both three and five, it prints "FizzBuzz".

# Loop through numbers from 1 to 100
for number in range(1, 101):  # The range function generates numbers from 1 to 100.
    # Check if the number is a multiple of both three and five
    if number % 3 == 0 and number % 5 == 0:  # % is the modulus operator. It checks for remainders.
        print("FizzBuzz")  # If the number is divisible by both, print "FizzBuzz".
    # Check if the number is a multiple of three
    elif number % 3 == 0:  # If the number is divisible by 3, print "fizz".
        print("fizz")
    # Check if the number is a multiple of five
    elif number % 5 == 0:  # If the number is divisible by 5, print "buzz".
        print("buzz")
    else:
        print(number)  # If none of the above conditions are met, print the number itself.

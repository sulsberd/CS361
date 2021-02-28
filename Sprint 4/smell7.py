
"""
Lab_Python_03
Solution for Question 1
"""

#program to get the first 50 primes

def main()
    n = 50

    print "the first 50 primes:"


    prime_count = 0
    possible_prime = 2

    while prime_count < n:

        divisor_count = 0
        for i in range(1,possible_prime+1):
            if possible_prime % i == 0:
                divisor_count += 1

        if divisor_count == 2:

            #(Comma print WITHOUT a newline - prevent the newline)
            print possible_prime,
            prime_count += 1

            #if mult of 10 print new line
            if prime_count % 10 == 0:
                print

    possible_prime += 1

if __name__ == '__main__':
    main()


    © 2021 GitHub, Inc.
    Terms
    Privacy
    Security
    Status
    Docs

    Contact GitHub
    Pricing
    API
    Training
    Blog
    About


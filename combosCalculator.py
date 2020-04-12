def factorial(n):
    if n==1:
        return 1
    else:
        return n*factorial(n-1)
# 
def combosWithoutCaringAboutScore():
    total = 0
    for numLeft in range(1, 49):
        total += factorial(numLeft+11)/(factorial(numLeft)*factorial(11))

    return total

def combosWithCaringAboutScore():
    total = 0
    for numLeft in range(1, 49):
        total += factorial(numLeft+11)/(factorial(numLeft)*factorial(11))*(48-numLeft+1)

    return total


# print(combosWithoutCaringAboutScore())
print(combosWithCaringAboutScore())
# 1,399,358,844,974.0
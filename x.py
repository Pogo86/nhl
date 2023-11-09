'''
x = 0
rolls = pow(10, 10)
i=0
while i < rolls:
    if ran.randint(1,6) == 6:x+=1
    i+=1

print(rolls)                - 10000000000               Rolls
print(x)                    -  1666630367               Number of 6's
print(x/rolls)              - 0.1666630367              As a Fraction
print((x/rolls) - (1/6))    - -3.6299666666683716e-06   Amout off an actuial 6th

'''
# Initial numbers
a = 10  # Binary: 1010
b = 20  # Binary: 10100

print(f"Before swap: a = {a}, b = {b}")

# The swap logic
a = a ^ b
b = a ^ b
a = a ^ b

print(f"After swap: a = {a}, b = {b}")
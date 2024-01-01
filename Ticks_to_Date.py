import json

# Load the JSON data from the file
with open('response.json', 'r') as file:
    data = json.load(file)

# Extract the "TTO" value and split it into individual parts
tto_value = data["TTO"].split(',')

# Assign the values to separate variables
s1 = int(tto_value[0])
s2 = int(tto_value[1])
s3 = int(tto_value[2])

# Print the values to verify
print("s1:", s1)
print("s2:", s2)
print("s3:", s3)

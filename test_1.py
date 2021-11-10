from mock_data import mock_data

# List collection of values
# Arrays in JavaScript List in Python
# Dictionary values in key:value pairs.

# Dictionary

me = {
    "name": "Jimmy",
    "last": "Newtron",
    "age": 50,
    "hobbies": [],
    "address": {
        "street": "EverGreen",
        "city": "Springfield",
    }
}
# Create new elements inside the dictionary
me["new"] = 1
# modify existing
me["age"] = 13

full_name = me["name"] + " " + me["last"]

# print(full_name)
# print(me["address"]["city"])
# print(me)



# List

names = []

names.append("Guil")
names.append("Jake")
names.append("Shane")

# print(names)

# get elements 
# print(names[0])
# print(names[2])

# for loop
# for name in names: 
    # print(name)



ages = [12, 32, 456, 10, 23, 678, 4356, 2, 46, 789, 23, 67, 13]

youngest = ages[0]

for age in ages:
    if age < youngest:
        youngest = age

# print(youngest)

# print the title for every product in mock data

for data in mock_data:
    print(data["title"])


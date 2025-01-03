F = {
"item-test": "192.50, 53.03",
"item-test2": "234.36" "25.04"
}

D = {1: 'Geeks', 2: 'For',
        3: {'A': 'Welcome', 'B': 'To', 'C': 'Geeks'}}

print(F["item-test"])
print("\n")
print(F["item-test2"])
print("\n")

print(D[3]['A'])

########################################################################################################################

DATA = {}
DATA["name"] = {}
DATA["name"]["pos"] = {}
DATA["name"]["pos"]["x"] = "New X Value"
DATA["name"]["pos"]["y"] = "New Y Value"

print(DATA)
print(DATA["name"]["pos"]["x"])  # Output: "New Value"
print(DATA["name"]["pos"]["y"])  # Output: "New Y Value"

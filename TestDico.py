

m = {'XY': (1, 2)}
cc={"k1":[3,2], "k2": ("d",23), "mat": m}

#cc["mat"] = m


# Afficher les deux dictionnaires
print("Avant la modification:")
print("cc:", cc)
print("m:", m)

# Modifier dict2
m["id"] = "456"

# Afficher les deux dictionnaires après modification
print("\nAprès la modification:")
print("cc:", cc)
print("m:", m)



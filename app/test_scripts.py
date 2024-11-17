from seesus import SeeSus

# text1 = "We aim to contribute to the mitigation of climate change by reducing carbon emissions in the city."
text1 = "Our team is dedicated to promoting gender equality in the workplace. We’ve achieved a 50/50 gender balance in leadership roles this year!"
result1 = SeeSus(text1)

# # print a summary of the results
print(result1)

# # print result on whether a statement aligns with sustainability, True or False
print(result1.sus)

# print the names of identified SDGs
print(result1.sdg)
# print the descriptions of identified SDGs
print(result1.sdg_desc)

# print the names of identified SDG targets
print(result1.target)
# print the descriptions of identified SDG targets
print(result1.target_desc)

# determine which dimension of sustainability (social, environmental, or economic) a statement belongs to
print(result1.see)
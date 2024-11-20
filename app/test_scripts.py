from seesus import SeeSus
import json


# text1 = "We aim to contribute to the mitigation of climate change by reducing carbon emissions in the city."
text1 = "Our team is dedicated to promoting gender equality "
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

result_json = {
    "text": text1,
    "sus": result1.sus,
    "sdgs": {
        "names": result1.sdg,
        "descriptions": result1.sdg_desc
    },
    "targets": {
        "names": result1.target,
        "descriptions": result1.target_desc
    },
    "sustainability_dimensions": result1.see
}

# Convert to JSON string for printing
result_json_str = json.dumps(result_json, indent=4)

# Print the JSON
print(result_json_str)
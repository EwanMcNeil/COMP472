##writing a parse that returns a dict structure that pairs a role to a tuple containing the name and agle

in_file = open('serenity.csv')
entries = in_file.readlines()

serenity_crew = dict()

for line in entries:
    entry = line.split(",")
    serenity_crew[entry[1]]= [entry[0], entry[2]]


print ( serenity_crew['Captain'])
print ( serenity_crew['Second'])
print ( serenity_crew['Pilot'])
print ( serenity_crew['Mechanic'])



serenity_crew['Captain'].append(0)

print ( serenity_crew['Captain'])
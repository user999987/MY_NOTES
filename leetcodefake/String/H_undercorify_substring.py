'''
"testthis is a testtest to see if testestest it works" ->
"_test_this is a _testtest_ to see if _testestest_ it works"
1. find substring locations
2. collapse overlappings
3. build new string
'''
def underscorifySubstring(string, substring):
    # Write your code here.
    # find locations
    locations = findSubstringLocations(string, substring)

    if len(locations) <= 0:
        return string

    # collapse
    newLocations = collapseOverlappings(locations)

    r = insertUnderscore(string, newLocations)

    return r
def findSubstringLocations(string, substring):
    locations = []
    subn = len(substring)
    for i, v in enumerate(string):
        start = string.find(substring, i)
        if start != -1:
            if [start, start + subn] not in locations:
                locations.append([start, start + subn])
    return locations[:]

def collapseOverlappings(locations: list):
    locations = locations[:] # [[0, 4], [14, 18], [18, 22], [33, 37], [36, 40], [39, 43]]
    newLocations = []
    prev = locations[0]
    for i in range(1, len(locations)):
        current = locations[i]
        if current[0] <= prev[1]:
            prev[1] = current[1]
        else:
            newLocations.append(prev)
            prev = current
    newLocations.append(prev) # [[0, 4], [14, 22], [33, 43]]
    return newLocations[:]

def insertUnderscore(string, newLocations):
    r = string[0:newLocations[0][0]]
    i = 0
    while i < len(newLocations) - 1:
        pair = newLocations[i]
        nextPair = newLocations[i + 1]
        r = r + "_" + string[pair[0]:pair[1]] + "_"
        r = r + string[pair[1]:nextPair[0]]
        i += 1
    pair = newLocations[-1]
    r = r + "_" + string[pair[0]:pair[1]] + "_"
    r = r + string[newLocations[-1][1]:]
    return r
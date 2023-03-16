'''



TUPLE



'''# A tuple is a collection which is ordered, unchangeable, duplicable
thistuple = ("apple", "banana", "cherry", "apple", "cherry")
# or
thattuple = tuple(("apple", "banana", "cherry", "apple", "cherry"))

# Access tuples like access list
print(thistuple[2:3])

# Update tuples is not available unless you do a workaround. Convert it to list then convert it back
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)

print(x)

# Unpacking tuples

fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

# if you have more values to be unpacked then you need use *
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")

(*green, yellow, red) = fruits
'''
>>>['apple', 'mango', 'papaya']
>>>pineapple
>>>cherry
'''

# Tuple methods
# index, Searches the tuple for a specified value and returns the position of where it was found
thistuple.index('cherry')
# >>> 2
# count, Returns the number of times a specified value occurs in a tuple
thistuple.count('cherry')
#>>> 2


'''



SET 




'''

# A set is a collection which is both unordered and unindexed.
# Using set() constructor
thisset = set(("apple", "banana", "cherry")) 

# Add items
thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset)

# Merge 2 sets or a list into set
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

mylist = ["kiwi", "orange"]

thisset.update(mylist)

# Remove items
thisset = {"apple", "banana", "cherry"}
# if the item to remove does not exist, remove() will raise an error
# you can use discard() which will not raise an error
thisset.remove("banana")
print(thisset)

# pop() is available and remove last item of collection but set is not ordered
# thisset.clear() will empty the set
# del thisset will delete set completely
del thisset


# Join sets
set1 = {"a","b","c"}
set2 = {1, 2, 3}
# Union will return a new set
set3 = set1.union(set2)
# update inserts items in set2 into set1
set1.update(set2)

# intersection() will return a new set
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

z = x.intersection(y)

# keeps only the intersection
x.intersection_update()


x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
# symmetric_difference() will return a new set
z = x.symmetric_difference(y)
# symmetric_difference_update() method will keep only the elements that are NOT present in both sets.
x.symmetric_difference_update(y)


'''


DICTIONARY



''' 
# After 3.7 dictionary is ordered
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
# if key does not exist return 0
thisdict.get('cao',0)
# returns the value of the item with the specified key.
# if key does not exist  insert the key, with the specified value
thisdict.setdefault('cao','heihei')

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2020})

thisdict.pop('brand')
# pop last item
thisdict.popitem()
del thisdict['brand']
thisdict.clear()
del thisdict

# copy dict
mydict = thisdict.copy()
# or
mydict = dict(thisdict)


'''



LIST



'''
# list constructor
thislist = list(("apple", "banana", "cherry"))

# list's update is extend
thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)

thistuple = ("kiwi", "orange")
thislist.extend(thistuple)

# list remove
# if there are duplicated values, it will remove the first one
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
# remove specified index
thislist.pop(1)
thislist.pop()
del thislist[0]
del thislist
thislist.clear()

thislist.sort()

def mycunf(n):
    return abs(n-50)
#  modifies the list in-place.
thislist.sort(key=myfunc)

# builds a new sorted list from an iterable
from operator import itemgetter, attrgetter
sorted(student_tuples, key=itemgetter(1,2))
# >>>[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
sorted(student_objects, key=attrgetter('grade', 'age'))
# >>>[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

# copy list
mylist = thislist.copy()
mylist = thislist[:]
mylist = list(thislist)

# tuple and list can use "+"
list1 = [1,2,3]
list2 = ["a","b","c"]
list3 = list1 + list2
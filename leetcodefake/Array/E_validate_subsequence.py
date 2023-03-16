'''
{
  "array": [5, 1, 22, 25, 6, -1, 8, 10],
  "sequence": [1, 6, -1, 10]
}
return True
'''

def isValidSubsequence(array, sequence):
    array_index=0
    sequence_index=0
    while array_index<len(array) and sequence_index<len(sequence):
        if array[array_index]==sequence[sequence_index]:
            sequence_index+=1
        array_index+=1
	print(sequence_index)
    if sequence_index==len(sequence):
        return True
    return False

def isValidSubsequence(array, sequence):
    # Write your code here.
	sequence_index=0
	for outer in array:
		if sequence[sequence_index]==outer:
			sequence_index+=1
		if sequence_index==len(sequence):
			return True
	return False
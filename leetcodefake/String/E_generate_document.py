'''
"characters": "abcabc",
"document": "aabbccc"
return false 
因为document多一个c
'''


def generateDocument(characters, document):
    char_count_dict = {}
    for c in characters:
        char_count_dict[c] = char_count_dict.get(c, 0)+1
    for c in document:
        if c not in char_count_dict or char_count_dict[c] == 0:
            return False
        char_count_dict[c] -= 1
    return True
    
# below is easier to understand
# def generateDocument(characters, document):
#     char_count_dict={}
#     for c in characters:
#         char_count_dict[c] = char_count_dict.get(c,0)+1
#     for c in document:
#         if c not in char_count_dict:
#             return False
#         char_count_dict[c]-=1
#         if char_count_dict[c]<0:
#             return False
# 	return True
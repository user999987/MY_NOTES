'''
["this", "that", "did", "deed", "them!", "a"] -> ["t", "t", "h", "i", "s", "a", "d", "d", "e", "e", "m", "!"]
no order requirement
'''
def minimumCharactersForWords(words):
    char_counter={}
    for word in words:
        chars={}
        for w in word:
            chars[w]=chars.get(w,0)+1
            char_counter[w] = max(char_counter.get(w,0),chars[w])
        
    chars_list=[]
    for k,v in char_counter.items():
        chars_list = chars_list+[k]*v
    return chars_list
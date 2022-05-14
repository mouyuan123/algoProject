class CompressedTrie():
    def __init__(self):
        """
        Create a root dictionary to store the starting character of different string (E.g. dog & cat have different
        starting character, which is "d" and "c"
        """
        self._data = {}
        self._sentiment = {}

    # Insert the positive and negative words into the compressed trie
    def insert(self, word, sentiment):
        # Retrieve the root dictionary
        data = self._data
        self._sentiment[word] = sentiment  # E.g., if "dog" is a + word, then {"dog" : "+"}
        i = 0
        while 1:
            try:
                # To check whether the first character in the word exists in the root dictionary
                node = data[word[i:i+1]]
            # Execute when KeyError occurs (the key is not found in a dictionary)
            except KeyError:
                # To check whether a dictionary is empty
                if data:  # If the dictionary is not empty
                    """
                    for each key in dictionary, it takes an array as value. Each array will consists of 2 values
                    first is the branching to the rest of values, the second is another dictionary that further branches from the 1st values
                    (E.g., "dog" and "doggie" are inserted, it looks like this: {'d': ['og', {'': ['', {}], 'g': ['ie', {}]}]}
                    """
                    data[word[i:i + 1]] = [word[i + 1:], {}]
                else:
                    if word[i:i+1] == '':
                        return
                    else:
                        if i != 0:
                            """
                            # Suppose "dog" and "doggie" is inserted, data[''] = ['',{}] 
                            acts as a terminator to tell the program that dog is also a different string while being the prefix of "doggie"
                            """
                            data[''] = ['', {}]
                        data[word[i:i+1]] = [word[i+1:], {}]
                return

            i += 1
            if word.startswith(node[0], i):
                if len(word[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            node[1]['']
                        except KeyError:
                            data = node[1]
                            data[''] = ['', {}]
                    return
                else:
                    i += len(node[0])
                    data = node[1]
            else:
                """
                When there is more than one branch edging from the parent
                E.g., insert "dog" and "dock", do => g, do => ck
                """
                ii = i
                j = 0
                """
                 Traverse until where different characters are found between parent and child
                 E.g. When insert "dog", compressed trie: d => og
                      When want to insert "dock", character c is different from character g
                """
                while ii != len(word) and j != len(node[0]) and word[ii:ii+1] == node[0][j:j+1]:
                    ii += 1
                    j += 1
                tmpdata = {}
                tmpdata[node[0][j:j + 1]] = [node[0][j + 1:], node[1]]  # splits out 'g' as another dictionary ( d => o => g)
                tmpdata[word[ii:ii + 1]] = [word[ii + 1:], {}]  # Starts from 'c' in "dock", built its own dictionary (c => k)
                # From line 73 & 74, {'g': ['', {}], 'c': ['k', {}]} is created
                data[word[i - 1:i]] = [node[0][:j], tmpdata]  # combine the "tmpdata" with the old dictionary
                # Finally, it looks like this: {'d': ['o', {'g': ['', {}], 'c': ['k', {}]}]}, implying ( d => o => g || d => o => ck)
                return

    # Search for the positive and negative words using the words array from each article
    # E.g., {'d': ['o', {'g': ['', {}], 'c': ['k', {}]}]} & "dog" is searched after inserting "dog" and "dock"
    def search(self, word):
        data = self._data  # Access the root dictionary
        i = 0
        while 1:
            try:
                node = data[word[i:i + 1]]  # node = data['d'] = ['o', {'g': ['', {}], 'c': ['k', {}]}]
            except KeyError:
                return False  # If the first character in the pattern does not exist in the root dictionary
            i += 1
            if word.startswith(node[0], i):
                if len(word[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            node[1]['']
                        except KeyError:
                            return False
                    print(word+" is a "+self._sentiment[word]+" word")
                    return True  # If the word is found within the Compressed Trie
                else:
                    i += len(node[0])
                    data = node[1]  # To access the deeper path (dictionary). E.g., Since "do" in "dog" is accessed, "do" can go to either "g" or "ck"
            else:
                return False


    __getitem__ = search

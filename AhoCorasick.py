from collections import deque

""" Store the positive, negative and neutral words in a 2D array before searching through the long text (each article) """
AdjList = []

def process(wordList, text):
    init_trie(wordList)
    return get_keywords_found(text)

def init_trie(keywords):
    """ creates a trie of keywords, then sets fail transitions """
    create_empty_trie()
    add_keywords(keywords)
    set_fail_transitions()

# We will insert the words into a trie before implementing the searching function
def create_empty_trie():
    """ initalize the root of the trie """
    # 'next_states are the goto state that check whether the character exists along the trie
    # 'fail_state' is the failure state that allows the searching backtracks to the longest suffix in the trie
    # 'output' is the container that stores the complete word at the end of the inserting process
    AdjList.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []}) # The empty root works as a failure state


def add_keywords(keywords):
    """ add all keywords in list of keywords """
    for keyword in keywords:
        add_keyword(keyword)


def find_next_state(current_state, value):
    # current_state = 0 represents the root is being accessed (Always insert starting from the root)
    for node in AdjList[current_state]["next_states"]:
        if AdjList[node]["value"] == value:
            return node
    return None


def add_keyword(keyword):
    """ add a keyword to the trie and mark output at the last node """
    current_state = 0
    j = 0
    keyword = keyword.lower() # Convert all the characters to lowercase before program execution
    child = find_next_state(current_state, keyword[j]) # Check whether the first character exists in the root
    """ If the first character is linked to the root, we will go down to the trie """
    while child is not None:
        current_state = child
        j = j + 1
        if j < len(keyword):
            child = find_next_state(current_state, keyword[j])
        else:
            break
    """ Insert the words into the trie at the place where it is not found """
    for i in range(j, len(keyword)):
        node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
        """ Whenever a new node is added, it is appended to the back of the AdjList """
        AdjList.append(node)
        """ Link the previous node with the node created using the 'next_states' container """
        AdjList[current_state]["next_states"].append(len(AdjList) - 1)
        current_state = len(AdjList) - 1 # After the link is built, now we move on to the next state
    """ After we insert a word into the trie completely, the 'output' container of the last character in the word will store the whole word """
    # E.g., for "he" AdjList[2]["output"] will store "he"
    AdjList[current_state]["output"].append(keyword)


def set_fail_transitions():
    q = deque() # Quicker append and pop operations from both end of the container
    child = 0
    """ Set the failure state for each node """
    for node in AdjList[0]["next_states"]:
        q.append(node)
        # All the node that connects directly to the root node will have failure state = 0
        # E.g., "h" has the suffix "h" (excluding itself) and "". Since root has value of "", we will return to the root
        AdjList[node]["fail_state"] = 0
    """ Here, we use a BFS to build the failure state of each node """
    while q:
        r = q.popleft()
        for child in AdjList[r]["next_states"]:
            q.append(child)
            state = AdjList[r]["fail_state"]
            while find_next_state(state, AdjList[child]["value"]) is None and state != 0:
                state = AdjList[state]["fail_state"]
            AdjList[child]["fail_state"] = find_next_state(state, AdjList[child]["value"])
            if AdjList[child]["fail_state"] is None:
                AdjList[child]["fail_state"] = 0
            AdjList[child]["output"] = AdjList[child]["output"] + AdjList[AdjList[child]["fail_state"]]["output"]


def get_keywords_found(line):
    """ returns true if line contains any keywords in trie """
    line = line.lower() # Lowercase all the characters in the long text (each article)
    current_state = 0
    sentimentLength = 0;
    # keywords_found = []  # (Can use this array to validate whether all the positive words in the article text is found)
    for i in range(len(line)):
        while find_next_state(current_state, line[i]) is None and current_state != 0:
            current_state = AdjList[current_state]["fail_state"]
        current_state = find_next_state(current_state, line[i])
        if current_state is None:
            current_state = 0
        else:
            for word in AdjList[current_state]["output"]:
                sentimentLength += 1
                # keywords_found.append({"index": i - len(word) + 1, "positive word": word})
    # for i in range(len(keywords_found)):
    #     print(keywords_found[i])
    return sentimentLength

# We need to clear it every time before using this list, else the negative and positive words will be appended together
def clear_Trie():
    AdjList.clear()

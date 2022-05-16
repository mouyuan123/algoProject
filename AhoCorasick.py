from collections import deque

AdjList = []

def process(wordList, text):
    init_trie(wordList)
    return get_keywords_found(text)

def init_trie(keywords):
    """ creates a trie of keywords, then sets fail transitions """
    create_empty_trie()
    add_keywords(keywords)
    set_fail_transitions()


def create_empty_trie():
    """ initalize the root of the trie """
    AdjList.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []})


def add_keywords(keywords):
    """ add all keywords in list of keywords """
    for keyword in keywords:
        add_keyword(keyword)


def find_next_state(current_state, value):
    for node in AdjList[current_state]["next_states"]:
        if AdjList[node]["value"] == value:
            return node
    return None


def add_keyword(keyword):
    """ add a keyword to the trie and mark output at the last node """
    current_state = 0
    j = 0
    keyword = keyword.lower()
    child = find_next_state(current_state, keyword[j])
    while child is not None:
        current_state = child
        j = j + 1
        if j < len(keyword):
            child = find_next_state(current_state, keyword[j])
        else:
            break
    for i in range(j, len(keyword)):
        node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
        AdjList.append(node)
        AdjList[current_state]["next_states"].append(len(AdjList) - 1)
        current_state = len(AdjList) - 1
    AdjList[current_state]["output"].append(keyword)


def set_fail_transitions():
    q = deque()
    child = 0
    for node in AdjList[0]["next_states"]:
        q.append(node)
        AdjList[node]["fail_state"] = 0
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
    line = line.lower()
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

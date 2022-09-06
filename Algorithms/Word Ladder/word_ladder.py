from collections import defaultdict, deque
from tracemalloc import start

class WordLadder:

    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def get_nextwords(word, dictionary):
        # Find possible next words from the dictionary
        # by counting the mismatched characters they share
        # if the mismatch is 1 append it to the list of possible next
        # words and return it
        L = len(word)
        result = []


        for next_word in dictionary:
            mismatch = 0
            if(len(next_word) == L):
                for i in range(L):
                    if word[i] != next_word[i]:
                        mismatch += 1
                if(mismatch == 1):
                    result.append(next_word)
            else:
                continue
        return result

    def getNeighbors(word, dictionary):
        # Find if the words are acceptable by comparing the number
        # of different characters they share
        # PULPING and CUPPING share 1 char difference etc.
        L = len(word)
        result = []
        
        for next_word in dictionary:
            if(len(next_word) == L):
                if(set(word).difference(set(next_word)) == set(next_word).difference(set(word))):
                    result.append(next_word)
            else:
                continue
        return result




    def intersection(word1, dictionary):
        # Find the intersection of two words 
        # by the characters they use
        L = len(word1)
        result = []
        for next_word in dictionary:
            if(len(next_word) == L ):
                if(word1 != next_word):
            
                    if len(list(set(word1) & set(next_word))) == 6:
                        # If the words share 6 characters it is acceptable

                        result.append(next_word)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        return result

    def getter(word, dictionary):
        # Function to get all words that share a pattern
        # *AP -> GAP, RAP etc.
        neighbors = defaultdict(dictionary)

        for word in dictionary:
            for j in range(len(word)):
                pattern = word[:j] +  "*" + word[j + 1:]
                neighbors[pattern].append(word)


    def find_path(dictionary, start_word, end_word):

        # If the dictionary is empty
        if(len(dictionary) == 0):
            return []
        # If the end_word/start_word is not in the dictionary
        # or they're the same word
        if(end_word not in dictionary or start_word == end_word):
            return []

        # If one of the words has more than characters than the other
        if(len(end_word) != len(start_word)):
            return []
        
        # Terminal condition
        fin = False

        # List to return
        result = []

        # Backtrack
        backtrack = {start: None}

        # Queue for BFS
        q = deque([start_word])
    

        while(not fin):
            # get the current node
            current_word = q.popleft()
            # get the neighbors of the current node
            neighbors = get_nextwords(current_word, dictionary)
            for neighbor in neighbors:
                if neighbor not in backtrack:
                    backtrack[neighbor] = current_word
                    q.append(neighbor)
            if end_word in backtrack:
                # found our target word
                fin = True

        # backtrack the path
        if fin:
            current_word = end_word

            # backtrack until the begin word
            while current_word != start_word:
                result.append(current_word)
                current_word = backtrack[current_word]
            # add the begin word
            result.append(start_word)
            # sort the list in the correct order
            result.reverse()
        return result
    
    def main():
        dictionary = ['PULPING', 'PULLING', 'CALLING', 'CALVING', 'SALVING', 'SOLVING', 'CUPPING']
        start = input("Enter begining word").upper()
        target = input("Enter target word").upper()

        WordLadder.find_path(dictionary, start, target)
        

    if __name__ == "__main__":
        main()






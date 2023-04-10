from boyer_moore import bm_search
import time
import math 


"""Returns all occurences of 'search_word'
in 'text' as a list of indices. """
def find_all_occurences(search_word: str, text: str) -> list[int]:
    left_bound = 0
    right_bound = len(text) 
    occurences = []
    while True:
        left_bound = text.find(search_word, left_bound +1, right_bound)
        if left_bound != -1:
            occurences.append(left_bound)
        else:
            break
    
    return occurences


"""Returns the elapsed time in milliseconds
of a strings.find."""
def time_find(search_word : str, text: str) -> float:
    start_time = time.time()
    occurences = find_all_occurences(search_word, text)
    return 1000.0* float(time.time() - start_time)

"""Returns the elapsed time in milliseconds of a bm_search"""
def time_bm(search_word : str, text: str) -> float:
    start_time = time.time()
    occurences = bm_search(search_word, text)
    return 1000.0* float(time.time() - start_time)




def main():
    stringer = "halloj lllollLLlol och den bruna räven hoppar lll"
    a = find_all_occurences("l", stringer)
    b = bm_search("l", stringer)

    print ("a ", a)
    print ("b ", b)

if __name__== "__main__":
    main()
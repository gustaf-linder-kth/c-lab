from boyer_moore import bm_search
import time
from pandas import DataFrame
import matplotlib.pyplot as plt

# Length of montaigne.txt
LENGTH_MONTAIGNE = 3052882

"""Returns all occurences of 'search_word'
in 'text' as a list of indices using strings.find. """
def find_search(search_word: str, text: str) -> list[int]:
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
    occurences = find_search(search_word, text)
    return 1000.0* float(time.time() - start_time)

"""Returns the elapsed time in milliseconds of a bm_search.
The time returned is the truncated mean of 10 tries."""
def time_bm(search_word : str, text: str) -> float:
    time_data = []
    for i in range(10):
        start_time = time.time()
        occurences = bm_search(search_word, text) # Occurences will not be used
        time_data.append(1000.0* float(time.time() - start_time))
    time_data.remove(min(time_data))
    time_data.remove(max(time_data))

    return sum(time_data) / len(time_data)

"""Takes a file and returns its as a string"""
def load_file(path: str) -> str:
    start_time = time.time() # Not relevant, but interesting
    file = open(path, "r")
    content = file.read()
    print("Took ", str(time.time() - start_time),  " to read", path)
    file.close()
    return content

"""Returns a dataframe with times on variable length
    length      bm_time (ms)    find_time (ms)
    8               x0              y0
    16              x1              y1
    32
    ...
    ...
    ...
    2097152         x20             y20
    """
def benchmark_text_length(search_word: str):
    df = DataFrame(columns=['length', 'bm_time', 'find_time'])
    text_length = 8 

    book = load_file("books/montaigne.txt")

    # Prevents searchword longer than text
    #if len(search_word) > text_length:
    #    text_length = len(search_word)

    while text_length < 1000000: #LENGTH_MONTAIGNE:
        new_row = [text_length, time_bm(search_word, book[:text_length]),
                   time_find(search_word, book[:text_length])]
        # Add a new row to dataframe
        df.loc[len(df)] = new_row
        print("We're at ", text_length)
        text_length *= 2

    return df

"""Returns a big dataframe with different lengths of search word."""
def benchmark_search_length():
    df = benchmark_text_length("L")
    
    # Let us create som data for longer search words.
    df10 = benchmark_text_length("Lorem ipsu")
    df100 = benchmark_text_length("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem u")
    df1000 = benchmark_text_length("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem uLorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget enim nulla. Fusce quis lorem u")

    # Let us now add the new data to the first dataframe
    df["bm_time10"] = df10["bm_time"]
    df["find_time10"] = df10["find_time"]
    
    df["bm_time100"] = df100["bm_time"]
    df["find_time100"] = df100["find_time"]

    df["bm_time1000"] = df1000["bm_time"]
    df["find_time1000"] = df1000["find_time"]

    print(str(df))
    return df

        

# Length of montaigne.txt seems to be 3052882
def main():
    df = benchmark_text_length("hello")
    df_search_words = benchmark_search_length()

    # defining layout
    fig, axes = plt.subplots(nrows=2, ncols=3)

    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    df.plot(x="length", y=["bm_time", "find_time"], ax=axes[0,0])
    df.plot(x="length", y="bm_time", ax=axes[0,1])
    df.plot(x="length", y="find_time", ax=axes[0,2])
    df_search_words.plot(x="length", y=["bm_time","bm_time10","bm_time100","bm_time1000"], ax=axes[1,0])
    df_search_words.plot(x="length", y=["find_time","find_time10","find_time100","find_time1000"], ax=axes[1,1])

    axes[0,0].set_title("Logarithmic plot of both")
    axes[0,1].set_title("Just Boyer-moore")
    axes[0,2].set_title("Just strings.find()")
    axes[1,0].set_title("BM with different searchwords")
    axes[1,1].set_title("strings.find() with different searchwords")
    # fourth?

    axes[0,0].set_yscale("log")
    axes[0,0].set_xscale("log")
    
    plt.xticks(rotation=45)
    plt.show()

if __name__== "__main__":
    main()
import sys
import pickle
import random
from ngram_model import NGramModel

def main(max_test_records, gram_length, max_length):
    pickle_file = open('../pickles/ngram_model.pkl', 'rb')
    model = pickle.load(pickle_file)
    
    test_file = "../data/methods_30k.txt"
    with open(test_file, encoding="utf-8") as file:
        lines = [line.rstrip() for line in file]
        random.shuffle(lines)
        lines = lines[0:max_test_records]

        for line in lines:
            line = line.split()
                         
            context = line[:gram_length-1]
          
            completion = model.sample(context, max_length)
            print(" ".join(completion))
            print()


if __name__ == "__main__":
    max_test_records = int(sys.argv[1])
    gram_length = int(sys.argv[2])
    max_length = int(sys.argv[3])
    main(max_test_records, gram_length, max_length)

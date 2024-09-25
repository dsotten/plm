from collections import defaultdict, Counter
import re
import math
import pickle

class NGramModel:
    def __init__(self, n):
        self.n = int(n)
        self.ngrams = defaultdict(Counter)
        self.count_distribution = Counter()
    

    def split_code_tokens(self, code):
        # code is already tokenized in methods_10k.txt
        try:
            tokens = code.split() #list(javalang.tokenizer.tokenize(code))
            tokens = [code for code in tokens]
            return tokens
        except Exception as e:
            raise Exception from e

    def train(self, corpus):
        for method in corpus:
            try:
                tokens = self.split_code_tokens(method)
                padded_tokens = ['<s>'] * (self.n - 1) + tokens + ['</s>']
                for i in range(len(padded_tokens) - self.n + 1):
                    context = tuple(padded_tokens[i:i + self.n - 1])
                    next_token = padded_tokens[i + self.n -1 ]
                    self.ngrams[context][next_token] += 1
            except:
                continue

        self.compute_count_distribution()

    def compute_count_distribution(self):
        for context_counts in self.ngrams.values():
            self.count_distribution.update(context_counts.values())
                
    def good_turing_adjustment(self, count):
        if count == 0:
            return self.count_distribution[1] / sum(self.count_distribution.values()) 
        next_count_freq = self.count_distribution[count]
        current_count_freq = self.count_distribution[count]
        return (count + 1) * next_count_freq / current_count_freq if current_count_freq > 0 else count

    def get_probability(self, context, token):
        context = tuple(context[-(self.n - 1):])
        count = self.ngrams[context][token]
        adjusted_count = self.good_turing_adjustment(count)
        total_ngrams = sum(self.ngrams[context].values())
        return adjusted_count / total_ngrams if total_ngrams > 0 else 0

    def predict(self, context):
        context = tuple(context[-(self.n - 1):])
        if self.ngrams[context] and context in self.ngrams:
            return max(self.ngrams[context], key=self.ngrams[context].get)
        else:
            return '<UNK>'
    
    def sample(self, context, max_len=20):
        output = list(context)
        for _ in range(max_len):
            next_token = self.predict(output)
            if next_token == '</s>':
                break
            output.append(next_token)
        return output

    def calculate_perplexity(self, corpus):
        perplexity = 0
        N = 0
        epsilon = 1e-10
        for sentence in corpus:
            try :
                tokens = self.split_code_tokens(sentence)
            except:
                continue
            padded_sentence = ['<s>'] * (self.n - 1) + tokens + ['</s>']
            for i in range(self.n - 1, len(padded_sentence)):
                context = padded_sentence[i - (self.n - 1):i]
                next_token = padded_sentence[i]
                probability = self.get_probability(context, next_token)

                # avoid log(0)
                probability = max(probability, epsilon)

                perplexity += -math.log2(probability)
                N += 1
        return math.pow(2, perplexity / N)

if __name__ == "__main__":
    dataset = []
    with open("../data/methods_30k.txt", 'r', encoding='utf-8') as f:
        for line in f:
            dataset.append(line)

    num_classes = 500 # as per instructions
    corpus = dataset[:num_classes]

    ngram_model = NGramModel(3)
    ngram_model.train(corpus)

    context = ["public", "static"]
    sample_completion = ngram_model.sample(context)
    print(sample_completion)

    output = open('../pickles/model.pkl', 'wb')
    pickle.dump(ngram_model, output)
    output.close()

    print("Pickle dump created.")

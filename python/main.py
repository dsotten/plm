import sys
import pickle
import random
from collections import defaultdict

from ngram_model import NGramModel

def load_dataset(path):
    dataset = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
           dataset.append(line)

    return dataset

def split_dataset(data, train_ratio=0.8):
    shuffled_data = data.copy()
    random.shuffle(shuffled_data)

    total_samples = len(shuffled_data)
    train_samples = int(total_samples * train_ratio)

    training_set = shuffled_data[:train_samples]
    test_set = shuffled_data[train_samples:]

    return training_set, test_set

def train_model(training_set, num_grams):
    model = NGramModel(num_grams)
    model.train(training_set)

    return model

def test_model(model, test_set):
    perplexity = model.calculate_perplexity(test_set)
    return perplexity

def find_best_model(dataset, num_grams, model_count=3):
    scores = defaultdict(float)
    for i in range(0, model_count):
        train, test = split_dataset(dataset, 0.5)

        model = train_model(train, num_grams)
        perplexity = test_model(model, test)

        scores[model] = perplexity
        print("Calculated model perplexity:", perplexity)

    model = min(scores, key=scores.get)
    perplexity = scores[model]
    return model, perplexity

def save_model(model, output_file="ngram_model.pkl"):
    output = open(f'../pickles/{output_file}', 'wb')
    pickle.dump(model, output)
    output.close()


if __name__ == "__main__":
    # .8*625 = 500 classes for training
    classes = 1000
    num_grams = sys.argv[1]
    dataset_path = sys.argv[2]

    json_records = load_dataset(dataset_path)
    random.shuffle(json_records)
    mini_dataset = json_records[:classes]

    best_model, perplexity = find_best_model(mini_dataset, num_grams)
    save_model(best_model)

    print()
    print("---- results ----")
    print("Perplexity:", perplexity)
    print("Best model saved to Pickle file under /pickles. You may test using 'model_test.py'.")

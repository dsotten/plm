# Project Name

Probabalistic language model built by the following authors:

- Nishat Sultana
- Danny Otten
- Joseph Call

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

Follow these steps to install and set up the project:

1. Clone the repository:
   ```
   git clone https://github.com/dsotten/plm.git
   ```

2. Navigate to the project directory:
   ```
   cd plm
   ```

3. Pull the data:
   ```
   git lfs pull
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Model training / testing (picks the best out of 3):
   ```
   python3 main.py <number of grams> ../data/methods_30k.txt
   ```
   
   ```
   python3 main.py 3 ../data/methods_30k.txt
   ```

## Usage

You can run model_test.py to actually make predictions on code fragments. Note that number of grams must be >= the number of grams used during training. Increasing this parameter will simply start the code prediction from the last n-1 tokens.

```
python3 model_test.py <number of datasamples> <number of grams> <number of tokens to predict>
```

```
python3 model_test.py 50 3 20
```

## Features

- Trains multiple models to find the one with the lowest perplexity
- Can be expanded for actual code prediction

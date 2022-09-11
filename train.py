import argparse
import os
import numpy as np
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', type=str, help='путь к директории, в которой лежит коллекция документов. Если '
                                                  'данный аргумент не задан, тексты вводятся из stdin.')
parser.add_argument('--model', type=str, help='путь к файлу, в который сохраняется модель.')
args = parser.parse_args()


def clean(string):
    ret = []
    cur_str = ''
    for c in string:
        c = c.lower()
        if 'а' <= c <= 'я':
            cur_str += c
        else:
            if cur_str != '':
                ret.append(cur_str)
            cur_str = ''
            if c == '.':
                ret.append(c)
    return ret


text = []
if args.input_dir:
    for file in os.listdir(args.input_dir):
        if file.endswith('.txt'):
            print(os.path.join(args.input_dir, file))
            r = open(os.path.join(args.input_dir, file), encoding='utf-8').read()
            text.extend(clean(r))
else:
    r = input()
    text.extend(clean(r))

text = np.array(text)
model = {}

print(f"Training model with {text.size} words...")
for i in range(2, text.size):
    if text[i-1] in model:
        model[text[i-1]].append(text[i])
    else:
        model[text[i-1]] = [text[i]]

    pref_2 = text[i-2]+" "+text[i-1]
    if pref_2 in model:
        model[pref_2].append(text[i])
    else:
        model[pref_2] = [text[i]]

print("Model have trained successfully! Saving...")
with open(args.model, 'wb') as path:
    pickle.dump(model, path)
    path.close()

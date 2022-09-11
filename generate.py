import argparse
import numpy as np
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='model.pkl', help='путь к файлу, в который сохраняется модель.')
parser.add_argument('--prefix', type=str, nargs='+', help='Начало предложения (одно или несколько слов).')
parser.add_argument('--length', type=int, required=True, help='Длина генерируемой последовательности.')
args = parser.parse_args()

with open(args.model, 'rb') as path:
    model = pickle.load(path)
    path.close()

ans = ''
sp = []
if args.prefix:
    sp = args.prefix
    ans = " ".join(sp)

pred2, pred1 = '', ''
if len(sp) > 0: pred1 = sp[-1].lower()
if len(sp) > 1: pred2 = sp[-2].lower()

for i in range(args.length - len(sp)):
    word = np.random.choice(model['.'])
    if pred1 and pred2 and pred2+' '+pred1 in model:
        word = np.random.choice(model[pred2+' '+pred1])
    elif pred1 and pred1 in model:
        word = np.random.choice(model[pred1])

    if word == '.': ans += '.'
    elif len(ans) and ans[-1] == '.':
        ans += ' ' + word[0].upper()
        if len(ans) > 1: ans += word[1:]
    else: ans += ' ' + word
    pred2, pred1 = pred1, word

ans = ans[0].upper() + ans[1:]
print(ans)

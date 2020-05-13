import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

path = Path('./data/')

def iter_pages(path):
    for d in path.iterdir():
        if d.is_dir():
            for p in d.iterdir():
                with p.open() as f:
                    page = json.load(f)
                yield page

titles = [page['title'] for page in iter_pages(path)]

tfidf = TfidfVectorizer()
X = tfidf.fit_transform(page['extract'] for page in iter_pages(path))

pca = PCA(n_components=2)
Y = pca.fit_transform(X.todense())

for title, yi in zip(titles, Y):
    print(f'{title:25} {yi[0]:10.4f} {yi[1]:10.4f}')

def transform(text):
    return pca.transform(tfidf.transform([text]).todense())


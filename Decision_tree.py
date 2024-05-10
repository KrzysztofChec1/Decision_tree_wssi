import numpy as np
from collections import Counter
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None): # z * jezeli hccemy podac value to musimy napisac value = cos
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None


class Decision_Tree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self,X,y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1],self.n_features)
        self.root = self._grow_tree(X,y)

    def _grow_tree(self, X,y,depth = 0):
        n_samples,n_feats = X.shape
        n_labels = len(np.unique(y))

        #sprawdzdmy konczace
        if depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split:
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        feat_idxs = np.random.choice(n_feats,self.n_features,replace=False)
        #szukanie najlepszego rozdzielenia

        best_feature,best_thresh = self._best_split(X, y,feat_idxs)

    def _best_split(self,X,y,feat_idxs):
        best_gain = -1
        split_idx,spilt_threshold = None,None

        for feat_idxs in feat_idxs:
            X_column = X[:,feat_idxs]
            thresholds = np.unique(X_column)

            for t in thresholds:
                gain = self._information_gain(y,X_column,t)

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idxs
                    spilt_threshold = t
        return split_idx

    def _information_gain(self, y, X_column, threshold):
        # entropia rodzica
        parent_entropy = self._entropy(y)

        #tworzymy dzieci
        left_idxs, right_idxs = self._split(X_column, threshold)

        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        n = len(y)
        n_l, n_r = len(left_idxs), len(right_idxs)
        e_l, e_r = self._entropy(y[left_idxs]), self._entropy(y[right_idxs])
        child_entropy = (n_l / n) * e_l + (n_r / n) * e_r

        # calculate the IG
        information_gain = parent_entropy - child_entropy
        return information_gain


    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten() # wartosci ktore sa mniejsze od st ktore sa konwertowane do 1 tab (flatten)
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs

    def _entropy(self, y):
        hist = np.bincount(y) # zlicza ilosc wystpien danych lioczb
        ps = hist / len(y) # to jest to p(X)
        return -np.sum([p * np.log(p) for p in ps if p > 0])

    def _most_common_label(self,y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value
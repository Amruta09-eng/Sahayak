"""Neural network: MLP (4-8-1) with manual backpropagation. Predicts site severity (0-10)."""
import numpy as np

def true_severity(X):   # hidden "ground truth" used to synthesise training data
    r, w, d, e = X.T
    return 10 * np.clip(0.35 * r + 0.30 * w + 0.15 * d + 0.10 * e + 0.25 * r * w, 0, 1)

def make_dataset(n=800, seed=1):
    rng = np.random.default_rng(seed)
    X = rng.random((n, 4))
    y = (true_severity(X) + rng.normal(0, 0.3, n)).clip(0, 10) / 10
    return X, y.reshape(-1, 1)

class MLP:
    def __init__(self, sizes=(4, 8, 1), lr=0.8, seed=0):
        rng = np.random.default_rng(seed)
        self.W = [rng.normal(0, 0.5, (a, b)) for a, b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(b) for b in sizes[1:]]
        self.lr = lr

    def forward(self, X):
        self.a = [X]
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = self.a[-1] @ W + b
            self.a.append(np.tanh(z) if i < len(self.W) - 1 else 1 / (1 + np.exp(-z)))
        return self.a[-1]

    def backward(self, y):
        m = len(y); out = self.a[-1]
        delta = (out - y) * out * (1 - out)                     # dMSE/dz at sigmoid output
        for i in reversed(range(len(self.W))):
            gW, gb = self.a[i].T @ delta / m, delta.mean(0)
            if i > 0:
                delta = (delta @ self.W[i].T) * (1 - self.a[i] ** 2)   # tanh derivative
            self.W[i] -= self.lr * gW; self.b[i] -= self.lr * gb

    def fit(self, X, y, epochs=3000):
        hist = []
        for _ in range(epochs):
            p = self.forward(X); self.backward(y)
            hist.append(float(((p - y) ** 2).mean()))
        return hist

    def predict(self, X):
        return self.forward(np.atleast_2d(X)).ravel() * 10

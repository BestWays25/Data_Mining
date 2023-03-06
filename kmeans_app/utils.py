import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# create a function to calculate the euclidean distance between two data points
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))

# create the KMeans class
class KMeans:
    def __init__(self, K=3, max_iters=100, plot_steps=False):
        self.K = K
        self.max_iters = max_iters
        self.plot_steps = plot_steps

    # assign labels to each data point based on their closest centroid
    def _assign_labels(self, X, centroids):
        # calculate the distance between each data point and the centroids
        distances = []
        for i in range(self.K):
            distances.append(euclidean_distance(X, centroids[i]))
        # assign the label of the closest centroid to each data point
        return np.argmin(distances)

    # update the centroid of each cluster
    def _update_centroids(self, X, labels):
        centroids = np.zeros((self.K, X.shape[1]))
        for k in range(self.K):
            # collect all data points assigned to the k-th cluster
            Xk = X[labels == k]
            # calculate the mean of the data points to get the new centroid
            centroids[k] = np.mean(Xk, axis=0)
        return centroids

    # fit the data to the model
    def fit(self, X):
        # randomly initialize K centroids
        self.centroids = X[np.random.choice(X.shape[0], self.K, replace=False), :]
        # assign labels to each data point based on the initial centroids
        self.labels = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            self.labels[i] = self._assign_labels(X[i], self.centroids)
        # update the centroids and the labels iteratively
        for i in range(self.max_iters):
            self.centroids = self._update_centroids(X, self.labels)
            if self.plot_steps:
                self.plot(X, self.centroids, self.labels)
            self.labels = np.zeros(X.shape[0])
            for j in range(X.shape[0]):
                self.labels[j] = self._assign_labels(X[j], self.centroids)
        if self.plot_steps:
            self.plot(X, self.centroids, self.labels)
    
    # plot the data and the centroids
    def plot(self, X, centroids, labels):
        fig, ax = plt.subplots(figsize=(12,8))
        customcmap = plt.get_cmap('viridis')
        for i in range(self.K):
            ax.scatter(X[labels == i, 0], X[labels == i, 1], marker='o', cmap=customcmap(i), s=8**2, alpha=0.5)
        for i in range(self.K):
            ax.scatter(*centroids[i], marker='*', color=customcmap(i), s=200, alpha=0.8)
        plt.title('Iteration number {}'.format(i))
        plt.show()



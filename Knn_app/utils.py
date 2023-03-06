from csv import reader
from math import sqrt
import matplotlib
matplotlib.use('TkAgg')
from operator import itemgetter
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def load_data_set(filename):
    try:
        with open(filename, newline='') as iris:
            return list(reader(iris, delimiter=','))
    except FileNotFoundError as e:
        raise e


def convert_to_float(data_set, set_type):
    """
    Convert the given data set to a list of floats.
    """
    converted_set = []
    try:
        for instance in data_set:
            if set_type == 'training':
                converted_set.append([float(val) for val in instance[:-1]])
                converted_set[-1].append(instance[-1])
            elif set_type == 'test':
                converted_set.append([float(val) for val in instance])
    except ValueError:
        return None

    return converted_set


def get_classes(training_set):
    return list(set([c[-1] for c in training_set]))


def find_neighbors(distances, k):
    return distances[0:k]


def find_response(neighbors, classes):
    votes = [0] * len(classes)

    for instance in neighbors:
        for ctr, c in enumerate(classes):
            if instance[-2] == c:
                votes[ctr] += 1

    return max(enumerate(votes), key=itemgetter(1))


def knn(training_set, test_set, k):
    distances = []
    dist = 0
    limit = len(training_set[0]) - 1

    # generate response classes from training data
    classes = get_classes(training_set)
    class_set = set(classes)

    results = []
    class_list = []

    try:
        for test_instance in test_set:
            for row in training_set:
                for x, y in zip(row[:limit], test_instance):
                    dist += (x-y) * (x-y)
                distances.append(row + [sqrt(dist)])
                dist = 0

            distances.sort(key=itemgetter(len(distances[0])-1))

            # find k nearest neighbors
            neighbors = find_neighbors(distances, k)

            # get the class with maximum votes
            index, value = find_response(neighbors, classes)

            # Add prediction to results and classes lists
            results.append(classes[index])
            class_list.append(classes)

            # empty the distance list
            distances.clear()

    except Exception as e:
        print(e)

    return results, class_list

def plot_data(training_set, test_set):
    df_training = pd.DataFrame(training_set)
    df_test = pd.DataFrame(test_set)

    # Define figure size and arrows for plotting
    plt.figure(figsize=(8,6))
    ax = plt.axes()
    ax.arrow(-1, 0, 2, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
    ax.arrow(0, -1, 0, 2, head_width=0.1, head_length=0.1, fc='k', ec='k')

    # plot training data
    for label in set(df_training.iloc[:, -1]):
        indices = df_training.iloc[:, -1] == label
        plt.scatter(df_training[indices][0], df_training[indices][1],
                    s=60, alpha=.7)
    # plot test data
    plt.scatter(df_test[0], df_test[1], c='r', marker='x', linewidths=3)

    plt.xlabel('Sepal Width')
    plt.ylabel('Sepal Length')
    plt.title('Training and Test Data Sets')
    plt.savefig('my_plot.png')
    plt.show()

from tempfile import NamedTemporaryFile

def plot_training_and_test_sets(training_set, test_set):
    # Create temporary file to save plot
    with NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        # Plot the training and test sets
        plot_data(training_set, test_set)

        # Save plot to temporary file
        plt.savefig(tmpfile)

    # Return the filepath to the saved image
    return tmpfile.name

import io

def plot_data1(training_set, test_set):
    df_training = pd.DataFrame(training_set)
    df_test = pd.DataFrame(test_set)

    # Define figure size and arrows for plotting
    plt.figure(figsize=(8,6))
    ax = plt.axes()
    ax.arrow(-1, 0, 2, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
    ax.arrow(0, -1, 0, 2, head_width=0.1, head_length=0.1, fc='k', ec='k')

    # plot training data
    for label in set(df_training.iloc[:, -1]):
        indices = df_training.iloc[:, -1] == label
        plt.scatter(df_training[indices][0], df_training[indices][1],
                    s=60, alpha=.7)
    # plot test data
    plt.scatter(df_test[0], df_test[1], c='r', marker='x', linewidths=3)

    plt.xlabel('Sepal Width')
    plt.ylabel('Sepal Length')
    plt.title('Training and Test Data Sets')

    # convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    print(img)
    return img


import matplotlib
matplotlib.use('Agg')  
import base64
from io import BytesIO
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib import pyplot as plt
import pandas as pd
from .utils import convert_to_float, knn, load_data_set, plot_data, plot_data1, plot_training_and_test_sets

def index(request):
    if request.method == 'POST':
        k = int(request.POST['k'])
        training_file = request.FILES['training_file']
        test_file = request.FILES['test_file']
        
        # Save uploaded files to disk
        training_file_path = os.path.join(settings.MEDIA_ROOT, training_file.name)
        with open(training_file_path, 'wb') as f:
            for chunk in training_file.chunks():
                f.write(chunk)
        
        test_file_path = os.path.join(settings.MEDIA_ROOT, test_file.name)
        with open(test_file_path, 'wb') as f:
            for chunk in test_file.chunks():
                f.write(chunk)
        
        training_set = convert_to_float(load_data_set(training_file_path), 'training')
        test_set = convert_to_float(load_data_set(test_file_path), 'test')

        if not training_set:
            context = {'error_message': 'Empty training set'}
            return render(request, 'knn.html', context)

        elif not test_set:
            context = {'error_message': 'Empty test set'}
            return render(request, 'knn.html', context)

        elif k > len(training_set):
            context = {'error_message': 'Expected number of neighbors is higher than number of training data instances'}
            return render(request, 'knn.html', context)

        else:
            results, classes = knn(training_set, test_set, k)
            plot_data(training_set, test_set)
            context = {'results': results, 'classes': classes}
            return render(request, 'knn-resaults.html', context)

    else:
        return render(request, 'knn.html')

def home_knn(request):
    return render(request, 'index.html')

def knn_blog(request):
    return render(request, 'knn-blog.html')

import io
import urllib
import os
picture = os.system('my_plot.png')

def results(request):
    k = int(request.GET.get('k'))
    training_file = request.FILES.get('training_file')
    test_file = request.FILES.get('test_file')

    training_set = convert_to_float(load_data_set(training_file), 'training')
    test_set = convert_to_float(load_data_set(test_file), 'test')

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

    # Generate and encode the plot image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Calculate the results and classes
    results, classes = knn(training_set, test_set, k)
    context = {}
    if not training_set:
        context['error_message'] = 'Empty training set'
        return render(request, 'knn.html', context)

    elif not test_set:
        context['error_message'] = 'Empty test set'
        return render(request, 'knn.html', context)

    elif k > len(training_set):
        context['error_message'] = 'Expected number of neighbors is higher than number of training data instances'
        return render(request, 'knn.html', context)

    else:
        # Render the plot image to pass to the context
        img_data = urllib.parse.quote(graphic)
        plot_url = f"data:image/png;base64,{img_data}"
        plot_data1= plot_data(training_set, test_set)
        context = {
            'results': results,
            'classes': classes,
            'plot_data': plot_data1,
            'picture': picture,
        }

        return render(request, 'knn-results.html', context)

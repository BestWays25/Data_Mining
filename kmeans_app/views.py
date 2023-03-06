from django.shortcuts import render
import matplotlib.pyplot as plt
from .utils import KMeans
import numpy as np
from io import BytesIO
import base64

def kmeans_view(request):
    num_points = request.POST.get('num_points', 2000) # Default value is 2000
    num_clusters = request.POST.get('num_clusters', 5) # Default value is 5
    # create `num_points` random data points to cluster
    X = np.random.rand(int(num_points), 2) * 10
    # create a KMeans object with `num_clusters` and fit the data
    kmeans = KMeans(K=int(num_clusters), max_iters=100, plot_steps=False)
    kmeans.fit(X)
    # create a dictionary to pass data to the template
    context = {'centroids': kmeans.centroids.tolist(),
               'labels': kmeans.labels.tolist(),
               'data': X.tolist()}
    
    # create a plot image and add it to the context dictionary
    fig, ax = plt.subplots(figsize=(12,8))
    customcmap = plt.get_cmap('viridis')
    for i in range(kmeans.K):
        ax.scatter(X[kmeans.labels == i, 0], X[kmeans.labels == i, 1], marker='o', cmap=customcmap(i), s=8**2, alpha=0.5)
    for i in range(kmeans.K):
        ax.scatter(*kmeans.centroids[i], marker='*', color=customcmap(i), s=200, alpha=0.8)
    ax.set_title('KMeans Clustering')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    context['graphic'] = graphic
    
    return render(request, 'kmeans.html', context)


def home(request):
    return render(request, 'base.html')
def kmeans_blog(request):
    return render(request, 'kmeans-blog.html')

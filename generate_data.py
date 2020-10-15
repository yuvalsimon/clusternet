#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from shutil import copyfile
import os
import sys

cluster_shapes = ['circle', 'halfmoon', 'filled_circle', 'line']

def usage():
    programName = os.path.basename(__file__)
    print('''
    Usage: python %s <cluster_shape>

    cluster_shape: %s
    ''' % (programName, "|".join(cluster_shapes)))
    exit(1)

def main(args):
    if(len(args) == 0):
        usage()
    cluster_shape = args[0]
    if(cluster_shape not in cluster_shapes):
        usage()

    num_classes = 2 # the code supports only 2 classes
    radius1 = 20
    radius2 = 4
    noise = 1
    vertex_class_prob = 0.5
    V = 2000
    E = 10000
    prob_edge_between_classes = 0.3
    train_pct = 0.4
    test_pct =  0.5

    labels = np.array([np.random.binomial(num_classes - 1, vertex_class_prob) for _ in range(V)])
    class_vertices_dict = {}
    for c in range(num_classes):
        class_vertices_dict[c] = np.array([i for i, j in enumerate(labels) if j == c])

    edges = []
    count_between_classes = 0
    for _ in range(E):
        source_class = np.random.binomial(1, 0.5)
        if(np.random.rand() <= prob_edge_between_classes):
            dest_class = 1 - source_class
            count_between_classes += 1
        else:
            dest_class = source_class
        edge = (np.random.choice(class_vertices_dict[source_class]), 
                np.random.choice(class_vertices_dict[dest_class]))
        while edge in edges or (edge[1], edge[0]) in edges or edge[0] == edge[1]:
            edge = (np.random.choice(class_vertices_dict[source_class]), 
                np.random.choice(class_vertices_dict[dest_class]))
        edges.append(edge)

    directory = "data/%s" % cluster_shape
    Path(directory).mkdir(parents=True, exist_ok=True)
    os.chdir(directory)

    with open("%s.cites" % cluster_shape, 'w') as cites:
        for e in edges:
            cites.write("%d %d\n" % e)
    all_x = []
    all_y = []
    classes = []
    with open("%s.content" % cluster_shape, 'w') as content:
        for v, c in enumerate(labels):
            dx = 0.
            dy = 0.
            if cluster_shape == 'halfmoon':
                r = radius1
                side = c * 2 - 1
                dx = - r / 8 * side
                dy = r / 2 * side
            elif cluster_shape == 'filled_circle':
                r = np.random.rand() * radius1
                side = c * 2 - 1
                dx = side * 2 * radius1
                dy = 0
            else:
                if(c == 0):
                    r = radius1
                else:
                    r = radius2
            nx0 = noise * (np.random.rand() - 0.5) * 2
            ny0 = noise * (np.random.rand() - 0.5) * 2
            if cluster_shape in ['circle', 'filled_circle']:
                x0 = (np.random.rand() - 0.5) * 2 * r
                y0 = ((r ** 2) - (x0 ** 2)) ** 0.5 * np.random.choice([-1, 1])
            elif cluster_shape == 'halfmoon':
                x0 = np.random.rand() * r * side
                y0 = ((r ** 2) - (x0 ** 2)) ** 0.5 * np.random.choice([-1, 1])
            else:
                y0 = np.random.rand() * 2 * r
                x0 = r
            px0 = x0 + nx0 + dx
            py0 = y0 + ny0 + dy
            all_x.append(px0)
            all_y.append(py0)
            classes.append(c)
            content.write("%d %f %f %d\n" % (v, px0, py0, c))

    plt.scatter(np.array(all_x), np.array(all_y), c=classes, s=5)
    plt.show()

    for i in ['train', 'test', 'valid']:
        copyfile("%s.content" % cluster_shape, "%s_%s_%.2f.content" % (cluster_shape, i, train_pct))

    train_pivot = int(E * train_pct)
    test_pivot = int(E * test_pct + train_pivot)
    with open("%s_train_%.2f.cites" % (cluster_shape, train_pct), 'w') as cites:
        for e in edges[:train_pivot]:
            cites.write("%d %d\n" % e)
    with open("%s_test_%.2f.cites" % (cluster_shape, train_pct), 'w') as cites:
        for e in edges[train_pivot:test_pivot]:
            cites.write("%d %d\n" % e)
    with open("%s_valid_%.2f.cites" % (cluster_shape, train_pct), 'w') as cites:
        for e in edges[test_pivot:]:
            cites.write("%d %d\n" % e)

    print("%s vertices inn class 0" % len(class_vertices_dict[0]))
    print("%s vertices inn class 1" % len(class_vertices_dict[1]))
    print("%s edges between classes" % count_between_classes)

    print("The generated dataset name is %s" % cluster_shape)

if __name__ == "__main__":
    main(sys.argv[1:])

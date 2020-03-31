"""Script for checking if edges of the graph are cutting edge

This script allows to check if edge is cutting edge. It reads adjacency
graph from .txt file. '1' represents edge, 0 is represented by '-'. User
need to import copy library.

This file contains following functions:
    *list_to_float list - converts '-' in graph to float inf
    *consistency_matrix_to_list - converts graph to list
    *create_vertices_list - creates list of graph's vertices
    *remove_reversed_duplicates - removes duplicate of mirror edges
    *create_edges_list - creates list of graph's edges
    *create_adjacency_dictionary - creates dictionary representing adjacency graph
    *bfs - implementation of BFS algorithm
    *check_if_cutting_edge - check if edge of graph is cutting edge
"""

import copy


def list_to_float_list(list):
    """Converts '-' to float 'inf'

    Parameters
    ----------
    list : list of strings representing graph

    Returns
    -------
    float_list : list of floats representing graph
    """
    float_list = []
    for element in list:
        if element == '-':
            float_list.append(float('inf'))
        else:
            float_list.append(float(element))
    return float_list


def consistency_matrix_to_list(file_name):
    """Reads graph from .txt file, creates matrix and appends it
       with list_to_float function

    Parameters
    ----------
    file_name : str
        The file name containing graph

    Returns
    -------
    consistency_matrix : list
        List of lists representing consistency graph
    """
    consistency_matrix = []
    with open(file_name) as file:
        for line in file:
            list = line.split()
            consistency_matrix.append(list_to_float_list(list))
    return consistency_matrix


def create_vertices_list(consistency_matrix):
    """Creates list of graph's vertices by iterating over
       length of consistensy matrix

    Parameters
    ----------
    consistency_matrix : list
        List representing consistency graph

    Returns
    -------
    vertices_list : list
        List of graph's vertices
    """
    vertices_list = []
    for i in range(len(consistency_matrix)):
        vertices_list.append(i+1)
    return vertices_list


def remove_reversed_duplicates(iterable):
    """Removes mirror duplicates of egdes using tuple

      Parameters
      ----------
      iterable : list
        List representing graph's edges
    """
    seen = set()
    for item in iterable:
        tup = tuple(item)
        if tup not in seen:
            seen.add(tup[::-1])
            yield item


def create_edges_list(consistency_matrix, vertices_list):
    """Creating graph's edges list by iterating over
       consistency matrix

       Parameters
       ----------
       consistency_matrix : list
            List representing consistency graph
       vertices_list : list
            List of graph's vertices

       Returns
       -------
       edge_list : list
            List of graph's edges
    """
    edge_list = []
    for i, weights in enumerate(consistency_matrix):
        for x, weight in enumerate(weights):
            if weight != float('inf'):
                edge = []
                edge.append(vertices_list[i])
                edge.append(vertices_list[x])
                edge_list.append(edge)
    edge_list = list(remove_reversed_duplicates(edge_list))
    return edge_list


def create_adjacency_dictionary(consistency_matrix):
    """Creating adjacency dictionary of graph, adding +1
       to vertice_number and x, because we are numbering
       vertices from 1, not 0

       Parameters
       ----------
       consistency_matrix: list
            List representing consistency graph

       Returns
       -------
       adjacency_dictionary : dict
            Dictionary representing graph's adjacencies
       """
    adjacency_dictionary = {}
    for i, row in enumerate(consistency_matrix):
        vertice_number = i+1
        adjacency_list = []
        for x, vertice in enumerate(row):
            if vertice != float('inf'):
                adjacency_list.append(x+1)
        adjacency_dictionary[vertice_number] = adjacency_list
    return adjacency_dictionary


def bfs(graph, node_v):
    """BFS algorithm starting from given vertice

    Parameters:
    ----------
    graph : dict
        Graph represention by adjacency dictionary
    node_v : int
        Vertice, which is starting point for BFS

    Returns
    -------
    vertices : list
        List of vertices we've visited by BFS algorithm
    """
    visited = []
    queue = []
    vertices = []
    visited.append(node_v)
    queue.append(node_v)
    while queue:
        s = queue.pop(0)
        vertices.append(s)
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return vertices


def check_if_cutting_edge(edges_list, adjacency_dictionary):
    """ Checking if edges of the graph are cutting edges,
        by coping adjacency dictionary, calling BFS and
        comparing vertices. Prints edge, and"YES" if edge is cutting,
        print "NIE" if not.

        Parameters
        ----------
        edges_list : list
            List of graph's edges
        adjacency_dictionary : dict
            Dictionary of graph adjacencies
        """
    for edge in edges_list:
        dict1 = copy.deepcopy(adjacency_dictionary)
        vertice1 = int(edge[0])
        vertice2 = int(edge[1])
        adjacency = dict1[vertice1]
        for vertice in adjacency:
            if vertice == vertice2:
                adjacency.remove(vertice)
                break
        adjacency = dict1[vertice2]
        for vertice in adjacency:
            if vertice == vertice1:
                adjacency.remove(vertice)
                break
        vertices = bfs(dict1, edge[0])
        if vertice2 in vertices:
            print("(", vertice1, vertice2, ")", "NIE")
        else:
            print("(", vertice1, vertice2, ")", "TAK")


filename = 'graph03.txt'
consistency_matrix = consistency_matrix_to_list(filename)
vertices_list = create_vertices_list(consistency_matrix)
edges_list = create_edges_list(consistency_matrix, vertices_list)
adjacency_dictionary = create_adjacency_dictionary(consistency_matrix)
check_if_cutting_edge(edges_list, adjacency_dictionary)

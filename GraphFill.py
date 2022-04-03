#  File: GraphFill.py
#  Description:
#  Student Name:
#  Student UT EID:
#  Partner Name:
#  Partner UT EID:
#  Course Name: CS 313E
#  Unique Number:
#  Date Created:
#  Date Last Modified:

import os
import sys
# this enables printing colors on Windows somehow
os.system("")

# code to reset the terminal color
RESET_CHAR = "\u001b[0m"
# color codes for the terminal
COLOR_DICT = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}
# character code for a block
BLOCK_CHAR = "\u2588"

# Input: text is some string we want to write in a specific color
#   color is the name of a color that is looked up in COLOR_DICT
# Output: returns the string wrapped with the color code
def colored(text, color):
    color = color.strip().lower()
    if not color in COLOR_DICT:
        raise Exception(color + " is not a valid color!")
    return COLOR_DICT[color] + text

# Input: color is the name of a color that is looked up in COLOR_DICT
# prints a block (two characters) in the specified color
def print_block(color):
    print(colored(BLOCK_CHAR, color)*2, end='')

# Stack class; you can use this for your search algorithms
class Stack(object):
  def __init__(self):
    self.stack = []

  # add an item to the top of the stack
  def push(self, item):
    self.stack.append(item)

  # remove an item from the top of the stack
  def pop(self):
    return self.stack.pop()

  # check the item on the top of the stack
  def peek(self):
    return self.stack[-1]

  # check if the stack if empty
  def is_empty(self):
    return len(self.stack) == 0

  # return the number of elements in the stack
  def size(self):
    return len(self.stack)

# Queue class; you can use this for your search algorithms
class Queue(object):
  def __init__(self):
    self.queue = []

  # add an item to the end of the queue
  def enqueue(self, item):
    self.queue.append(item)

  # remove an item from the beginning of the queue
  def dequeue(self):
    return self.queue.pop(0)

  # checks the item at the top of the Queue
  def peek(self):
    return self.queue[0]

  # check if the queue is empty
  def is_empty(self):
    return len(self.queue) == 0

  # return the size of the queue
  def size(self):
    return len(self.queue)

# class for a graph node; contains x and y coordinates, a color, a list of edges and
# a flag signaling if the node has been visited (useful for serach algorithms)
# it also contains a "previous color" attribute. This might be useful for your flood fill implementation.
class ColorNode:
    # Input: x, y are the location of this pixel in the image
    #   color is the name of a color
    def __init__(self, x, y, color):
        self.color = color
        self.prev_color = color
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False

    # Input: node_index is the index of the node we want to create an edge to in the node list
    # adds an edge and sorts the list of edges
    def add_edge(self, node_index):
        self.edges.append(node_index)
        self.edges.sort()

    # Input: color is the name of the color the node should be colored in;
    # the function also saves the previous color (might be useful for your flood fill implementation)
    def set_color(self, color):
        self.prev_color = self.color
        self.color = color

# class that contains the graph
class ImageGraph:
    def __init__(self, image_size):
        self.nodes = []
        self.image_size = image_size
        self.adj_matrix = [[0 for i in range(image_size)]for j in range(image_size)]

    def add_edge(self, start_index, end_index):
         self.nodes[start_index].add_edge(end_index)
         self.nodes[end_index].add_edge(start_index)
         self.adj_matrix[start_index][end_index] = 1
         self.adj_matrix[end_index][start_index] = 1

    # prints the image formed by the nodes on the command line
    def print_image(self):
        img = [["black" for i in range(self.image_size)] for j in range(self.image_size)]

        # fill img array
        for node in self.nodes:
            img[node.y][node.x] = node.color

        for line in img:
            for pixel in line:
                print_block(pixel)
            print()
        # print new line/reset color
        print(RESET_CHAR)

    # sets the visited flag to False for all nodes
    def reset_visited(self):
        for i in range(len(self.nodes)):
            self.nodes[i].visited = False

    # implement your adjacency matrix printing here.
    def print_adjacency_matrix(self):
        print("Adjacency matrix:")

        for item in self.adj_matrix:
            for another in item:
                print(another, end = "")
            print()

        # empty line afterwards
        print()

    # implement your bfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with
    def bfs(self, start_index, color):
        # reset visited status
        self.reset_visited()
        # print initial state
        print("Starting BFS; initial state:")
        self.print_image()

        myQueue = Queue()
        self.nodes[start_index].visited = True
        self.nodes[start_index].set_color(color)
        self.print_image()
        myQueue.enqueue(self.nodes[start_index])
        while myQueue is not None:
            node = myQueue.dequeue()
            for i in node.edges:
                if self.nodes[i].visited is False:
                    self.nodes[i].visited = True
                    self.nodes[i].set_color(color)
                    self.print_image()
                    myQueue.enqueue(self.nodes[i])


    # implement your dfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with
    def dfs(self, start_index, color):
        # reset visited status
        self.reset_visited()
        # print initial state
        print("Starting DFS; initial state:")
        self.print_image()

        myStack = Stack()
        self.nodes[start_index].visited = True
        self.nodes[start_index].set_color(color)
        self.print_image()
        myStack.push(self.nodes[start_index])
        while myStack is not None:
            node = myStack.peek()
            i = -1
            for j in range(len(node.edges)):
                if node.edges[j].visited is False:
                    i = j
                    break
            if i == -1:
                i = myStack.pop()
            else:
                self.nodes[i].visited = True
                self.nodes[i].set_color(color)
                self.print_image()
                myStack.push(self.nodes[i])


def main():
    line = sys.stdin.readline()
    dimensions = line.strip()
    dimensions = int (line)

    # create the Graph object
    graph = ImageGraph(dimensions)

    # read the number of vertices
    line = sys.stdin.readline()
    line = line.strip()
    num_vertices = int (line)

    # read the vertices to the list of Vertices
    for i in range (num_vertices):
      line = sys.stdin.readline()
      node = line.strip()
      node = node.split(",")
      color_node = ColorNode(int(node[0]), int(node[1]), node[2])
      graph.nodes.append(color_node)

    # read the number of edges
    line = sys.stdin.readline()
    line = line.strip()
    num_edges = int (line)

    # read each edge and place it in the adjacency matrix
    for i in range (num_edges):
      line = sys.stdin.readline()
      edge = line.strip()
      edge = edge.split(",")
      start = int (edge[0])
      finish = int (edge[1])
      graph.add_edge(start, finish)

    # read the starting vertex for bfs
    line = sys.stdin.readline()
    bfs = line.strip()
    bfs = bfs.split(",")
    bfs_start = int (bfs[0])
    bfs_color = bfs[1]

    # read the starting vertex for bfs
    line = sys.stdin.readline()
    dfs = line.strip()
    dfs = dfs.split(",")
    dfs_start = int (dfs[0])
    dfs_color = dfs[1]

    print(dfs_color)

    # print matrix
    graph.print_adjacency_matrix()

    # run bfs
    graph.bfs(bfs_start, bfs_color)

    # run dfs
    graph.dfs(dfs_start, dfs_color)


if __name__ == "__main__":
    main()

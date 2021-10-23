import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath

from problem1 import *
from tree import *

def drawTree(tree, robot, obstacles, start, goal, path):
    fig = plt.figure()
    axis = fig.gca()
    axis.spines["top"].set_linewidth(2)
    axis.spines["right"].set_linewidth(2)
    axis.spines["left"].set_linewidth(2)
    axis.spines["bottom"].set_linewidth(2)

    for i in obstacles:
        temp = i
        temp.append(temp[0])
        x, y = zip(*temp)
        plt.fill(x, y, color="black")

    initial = []
    final = []
    for i in range(0, len(robot)):
        initial.append([robot[i][0] + start[0], robot[i][1] + start[1]])
        final.append([robot[i][0] + goal[0], robot[i][1] + goal[1]])
    initial.append(initial[0])
    final.append(final[0])

    xi, yi = zip(*initial)
    xf, yf = zip(*final)

    plt.fill(xi, yi, color="green")
    plt.fill(xf, yf, color="red")

    draw = tree.getAll()

    while(len(draw)>0):
        plt.plot(draw[0].point[0], draw[0].point[1], marker='o', color="blue")
        for i in draw[0].neighbors:
            #print("drawing "+ str(draw[0].point)+ " and "+ str(i.point))
            x = [draw[0].point[0], i.point[0]]
            y = [draw[0].point[1], i.point[1]]
            plt.plot(x, y, 'bo', linestyle='solid')
        draw.pop(0)

    if(path!=False):
        for i in range(len(path)-1):
            x = [path[i][0], path[i+1][0]]
            y = [path[i][1], path[i+1][1]]
            plt.plot(x, y, 'ro', linestyle='solid')

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()

def getPath(tree, start, goal):
    endNode = tree.getNode(goal)
    path = []
    while(endNode!=None):
        path.append(endNode.point)
        endNode = endNode.parent
    temp = list(reversed(path))
    print(temp)
    return temp

def rrt(robot, obstacles, start, goal, iter_n):
    tree = Tree(robot, obstacles, start, goal)
    path = []
    while(iter_n >=0):
        #print(iter_n)
        sampled = sample()
        if(iter_n % 10 ==0):
            sampled = goal
        if(tree.getNode(sampled)!=False):
            continue
        near = tree.nearest(sampled)
        actual = tree.extend(near, sampled)
        if(tree.distance(actual, goal)<=.25):
            attempt = tree.extend(actual, goal)
            if(attempt == goal):
                path = getPath(tree, start, goal)
                drawTree(tree, robot, obstacles, start, goal, path)
                return path
        iter_n-=1
    lastNode = lastResort(tree, robot, obstacles,goal)
    if(lastNode == -1):
        drawTree(tree, robot, obstacles, start, goal, path)
        return False
    attempt = tree.extend(lastNode.point, goal)
    path = getPath(tree, start, goal)
    drawTree(tree, robot, obstacles, start, goal, path)
    return path

def lastResort(tree, robot, obstacles, goal):
    all = tree.getAll()
    distances = []
    far = None
    added = False
    for i in all:
        pointList = tree.getList(i.point, goal)
        for j in pointList:
            if(isCollisionFree(robot, j, obstacles) == False):
                distances.append(-1)
                added = True
                break
        if(added == False):
            distances.append(tree.distance(i.point, goal))
        added = False
    for i in distances:
        if i >= 0:
            added = True
            break
    if(added == True):
        index = distances.index(min([i for i in distances if i > 0]))
        return all[index]
    return -1

def visualize_path(robot, obstacles, path):
    return

def visualize_configuration(robot, obstacles, start, goal):
    return

def visualize_rrt(robot, obstacles, start, goal, iter_n):
    return

temp = parse_problem("robot_env_01.txt","probs_01.txt")
print(rrt(temp[0], temp[1], (3,3), (8.5,8.5), 500))
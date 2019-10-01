# Branch and Bound algorithm with graphical visualization
from graphviz import Digraph
import random
import numpy as np
dot = Digraph(comment='branch and bound')      # graph object

N = int(input("Enter Number of features:"))     # number of total features
b = int(input("Enter Number of features you want to select:"))      # number of required features
k = 0
flag = 0
flag2 = 0
input_set = []           # this list contains the features
print("Enter %d features"%N)
for i in range(N):
    input_set.append(int(input()))
    
def J(x):          # This is the objective function. Here it is 3^||x||, where x is a set
    sum_ = 0
    for i in x:
        sum_ += i**2
    return 3**np.sqrt(sum_)

num_levels = N - b +1       # number of levels of the tree 
# Each node contains a set of features, a set preserved features, level/depth of the node from the root, index of the node which required for making the graph 
class node:
    def __init__(self, set_, pres_set, level, index):
        self.set = set_           # set of features
        self.pres_set = pres_set        # set preserved features
        self.level = level        # level/depth of the node
        self.index = index        # an unique index of the node
    def num_branch(self):       # this returns number of branches from that node
        return (b + 1 - len(self.pres_set))
    # this returns randomly chosen indices(sorted on their J(set_features \ index) value) from the set of features which are not in the set of preserved features
    def choose_sort_features(self):         
        nb = self.num_branch()
        # choose nb features which are in set but not in pres_set 
        cf = []
        for i in range(nb):
            x = random.randint(0 , len(self.set) - 1)
            while (x in cf) or (self.set[x] in self.pres_set):
                x = random.randint(0 , len(self.set) - 1)
            cf.append(x)
        a = []
        for i in cf:
            set1 = [j for j in self.set]
            set1.pop(i)
            a.append(J(set1))
        
        for i in range(nb):
            for j in range(i+1, nb ):
                if a[i] > a[j]:
                    #swap
                    temp = a[i]
                    a[i] = a[j]
                    a[j] = temp
                
                    temp = cf[i]
                    cf[i] = cf[j]
                    cf[j] = temp
        return cf
    

nodes = []        # This is a stack of nodes which keeps track of the next node from where we need to branch
temp_node = node(input_set, [], 1, 0)         # This is the first node which will contain the whole user input set. Here nothing to preserve.
dot.node(str(k), str(input_set)+"\n"+ "%0.1f"%J(input_set))
nodes.append(temp_node)
flag2 = 0 
while len(nodes)>0:
    node1 = nodes.pop(len(nodes) -1)
    ind = node1.index
    nb = node1.num_branch()
    cfs = node1.choose_sort_features()
    temp_pres = [ i for i in node1.pres_set ]
    for i in range(nb):
        set1 = [j for j in node1.set]
        set1.remove(node1.set[cfs[i]])
        if i > 0:
            temp_pres.append(node1.set[cfs[i-1]])
        temp1_pres = [j for j in temp_pres]
        k += 1
        temp_node = node(set1, temp1_pres, node1.level + 1, k)

        dot.node(str(k), str(set1)+"\n"+"%0.1f"%J(set1))          # Adding the node to the graph object
        dot.edge(str(ind), str(k), constraint='1', label = str(node1.set[cfs[i]]))         # Adding the edge to the graph object 
        
        if temp_node.level < num_levels:          # This is to check that the node is the leaf node or not
            nodes.append(temp_node)           # If its not a leaf node we will append the node to the stack for further branching
        else:
            if flag2 == 0:         # This is for initialization of the optimal set of features 
                flag2 = 1
                opt_j = temp_node.set         
            if J(opt_j) < J(temp_node.set):        # This is for updation of the optimal set of features 
                opt_j = temp_node.set
            if len(nodes) > 0 and J(opt_j) >= J(nodes[len(nodes)-1].set):        # This is to truncate the tree
                flag = 1
                break
        if flag == 1:
            break
    if flag == 1:
        break
print("The optimal features are:",opt_j")
from graphviz import Source
dot.render('test-output/round-table.gv', view = "TRUE") 

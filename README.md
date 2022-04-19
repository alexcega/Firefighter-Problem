# Firefighter-Problem
Heuristics and ploting for [the firefighter problem](https://alexcega.notion.site/Proyecto-Sistemas-inteligentes-deb71723e31c432c90c28f70d6069c40). Diferent aproach to this combinatorial optimization problem.

# Description of problem
There is a node on fire in T = 0.
The fire expreads to each adjacent node that it has.
Your job is to extinguish the fire in the minimal amount of time (T), each T you get to protect N nodes acording of how many Firefigthers you have 
![image](https://user-images.githubusercontent.com/43385086/164042323-29e044c6-f414-4d79-a427-e6623fbeab11.png)


# Heurisitcs 
## Degree
Save the node with the highest number of edges
![image](https://user-images.githubusercontent.com/43385086/164041812-412d5bf9-723d-4c6a-a71b-364afa13c217.png)

## Desc
In a graph tree, try to find the biggest sub tree to save
![image](https://user-images.githubusercontent.com/43385086/164042603-965d64df-55d1-4a9f-b98e-5193806d3167.png)

## Threat
Similar to **Degree**, try to save the node with highest number of edges but only from the nodes thretened
![image](https://user-images.githubusercontent.com/43385086/164042817-d1f79580-7cfe-4565-b0ef-20084ed776c0.png)

# More details
The graphs are read from a csv file with a adjacenty matrix read using [numpy](https://numpy.org)
The Graph is plot using the library [networkx](https://networkx.org) and [matplotlib](https://matplotlib.org)

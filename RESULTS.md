# Hw 2 Results CSE 6140
## Author: Sravan Jayanthi
The plots showing the running time as the number of edge increases are shown below:

![](results/static_mst.png)
Figure 1

![](results/dynamic_mst.png)
Figure 2

Where Figure 1 just shows the static MST results and Figure 2 shows the dynamic MST results. The results show that the static MST tracks with the time complexity expected of Kruskal's algorithms which is O(E log V) so there is approximately logarithmic growth. On the other hand, the results for the dynamic MST over 1000 edges shows that empirical scaling tracks with the methods used for cycle detection (Depth first search) which has a runtime of O(E + V) so it has a more linear scaling is of quicker time to calculate compared to the static MST which requires sorting all the edges then performing a Union-find.
# CSE 6140 Group 46 Final Project
## Authors: Aravind Vengarai, Sravan Jayanthi, Alecsander Falc, Collin Hubbard

This codebase contains the solution for the minimum vertex cover problem for some graph file. This method will return a solution file with an MVC and trace showing the algorithm's progress over time.
To run this code, type the command:
```
'python src/run_mvc.py -inst <graph file name> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```
for any `<graph file name>`, `alg` in the list of algorithms,  `<cutoff in seconds>`, and `<random seed>`

The solutions and trace files associated with the run can be found in the `solutions/` folder
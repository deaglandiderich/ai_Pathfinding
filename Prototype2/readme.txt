AI Pathfinding Project:

Description:
This project is meant to demonstrate how different pathfinding AI perform while competing with each other.
Each test case folder consists of an input file, output file, and a log of the actions for each ai (a, b, and c).
The input folder is the only one with text before the program runs; it is a CSV file that represents a grid of nodes for the AI to traverse.
The nodes marked A, B, and C are the start points of the AI A, B, and C respectively.
The numbers represent the cost of traversal of that node for each pathfinding AI. An X means it cannot be traversed.
Each AI is attempting to reach the start point of one of the other AIs.
Once an AI has explored a node, no other AI can explore it.
AI A uses the A* search algorithm, B uses greedy heuristic and C uses Dijkstra's algorithm.
Once the program is run, the files marked a_Data, b_Data and c_Data will have logged the optimal path they took and its cost (if they found one), and the nodes they explored.
The output file will be a visual representation of how the CSV file was explored by each AI.

Running Instructions:
To run the program, simply run the file titled "project".
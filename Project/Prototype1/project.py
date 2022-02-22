import csv

class Node:
  def __init__(self, dataval):
    self.dataval = dataval
    self.a_parent = None
    self.b_parent = None
    self.c_parent = None
    self.a_path_cost = 0
    self.b_path_cost = 0
    self.c_path_cost = 0
    self.a_priority = 0
    self.b_priority = 0
    self.c_priority = 0

def pathfinding(input_filename, a_data_filename, b_data_filename, c_data_filename, final_state_filename):
  # input_filename contains a CSV file with the input grid
  # optimal_path_filename is the name of the file the optimal path should be written to
  # explored_list_filename is the name of the file the list of explored nodes should be written to
  model = [] #internal model of the nodes to be traversed
  
  x_iterator = -1 #used for construction of the internal model
  y_iterator = -1
  
  a_goal_locations = [] #stores the x and y locations of the goals
  b_goal_locations = [] #stores the x and y locations of the goals
  c_goal_locations = [] #stores the x and y locations of the goals
  
  a_closest_goal = 0 #used for construction of the heuristic
  b_closest_goal = 0 #used for construction of the heuristic
  c_closest_goal = 0 #used for construction of the heuristic

  a_optimal_path_list = []
  b_optimal_path_list = []
  c_optimal_path_list = []
  
  a_optimal_path_cost = 0
  b_optimal_path_cost = 0
  c_optimal_path_cost = 0
  
  with open(input_filename, 'r') as file:
    reader = csv.reader(file, skipinitialspace = True)
    for row in reader: #for every row in the csv
      x_iterator = -1
      y_iterator += 1
      model.append([]) #add a new row in the model
      for column in row: #for every column in the csv
        x_iterator += 1
        model[y_iterator].append(Node([])) #add a new column in the current row in the model
        model[y_iterator][x_iterator].dataval.append(column) #add the value stored in the current node being searched
        model[y_iterator][x_iterator].dataval.append(x_iterator) #add the x coordinate
        model[y_iterator][x_iterator].dataval.append(y_iterator) #add the y coordinate
        if column == 'A':
          b_goal_locations.append([x_iterator, y_iterator])
          c_goal_locations.append([x_iterator, y_iterator])
          a_location = [x_iterator, y_iterator]
        elif column == 'B':
          a_goal_locations.append([x_iterator, y_iterator])
          c_goal_locations.append([x_iterator, y_iterator])
          b_location = [x_iterator, y_iterator]
        elif column == 'C':
          a_goal_locations.append([x_iterator, y_iterator])
          b_goal_locations.append([x_iterator, y_iterator])
          c_location = [x_iterator, y_iterator]
          
  a_closest_goal = a_goal_locations[0]
  b_closest_goal = b_goal_locations[0]
  c_closest_goal = c_goal_locations[0]
  
  for i in range(len(model)):  #assign heuristic values based on proximity to goal node
    for j in range(len(model[i])):
      for k in range(len(a_goal_locations)):        
        if (abs(j - a_goal_locations[k][0]) + abs(i - a_goal_locations[k][1])) < (abs(j - a_closest_goal[0]) + abs(i - a_closest_goal[1])):
          a_closest_goal = a_goal_locations[k]
      model[i][j].dataval.append(abs(j - a_closest_goal[0]) + abs(i - a_closest_goal[1]))

  for i in range(len(model)):  #assign heuristic values based on proximity to goal node
    for j in range(len(model[i])):
      for k in range(len(b_goal_locations)):        
        if (abs(j - b_goal_locations[k][0]) + abs(i - b_goal_locations[k][1])) < (abs(j - b_closest_goal[0]) + abs(i - b_closest_goal[1])):
          b_closest_goal = b_goal_locations[k]
      model[i][j].dataval.append(abs(j - b_closest_goal[0]) + abs(i - b_closest_goal[1]))

  for i in range(len(model)):  #assign heuristic values based on proximity to goal node
    for j in range(len(model[i])):
      for k in range(len(c_goal_locations)):        
        if (abs(j - c_goal_locations[k][0]) + abs(i - c_goal_locations[k][1])) < (abs(j - c_closest_goal[0]) + abs(i - c_closest_goal[1])):
          c_closest_goal = c_goal_locations[k]
      model[i][j].dataval.append(abs(j - c_closest_goal[0]) + abs(i - c_closest_goal[1]))


  a_frontier = [model[a_location[1]][a_location[0]]]
  a_goal = False
  a_explored = []

  b_frontier = [model[b_location[1]][b_location[0]]]
  b_goal = False
  b_explored = []

  c_frontier = [model[c_location[1]][c_location[0]]]
  c_goal = False
  c_explored = []

  while True:
    if (a_frontier == [] or a_goal == True) and (b_frontier == [] or b_goal == True) and (c_frontier == [] or c_goal == True): #if frontier is empty
      break     #then the game is over
    
    if (a_frontier != []) and (a_goal == False): 
        a_leaf = a_frontier.pop(0)  #otherwise, take the top priority node

        print("\nA's current node: ")
        print(a_leaf.dataval)

        a_explored.append(a_leaf)
        
        for y in b_frontier:  #check if it is in explored by comparing datavalues
          if (a_leaf.dataval[1] == y.dataval[1] and a_leaf.dataval[2] == y.dataval[2]):
            b_frontier.remove(y)
            break
        for y in c_frontier:  #check if it is in explored by comparing datavalues
          if (a_leaf.dataval[1] == y.dataval[1] and a_leaf.dataval[2] == y.dataval[2]):
            c_frontier.remove(y)
            break        
        
        if a_leaf.dataval[0] == 'B' or a_leaf.dataval[0] == 'C':  #if it is a goal node
          print("A's Goal reached!")
          a_goal = True
          a_optimal_path_cost = a_leaf.a_path_cost  #the optimal path cost is its path cost
          while a_leaf != None:  #trace back its ancestry to the top (parent = none is the top)
            print("Writing " + str(a_leaf.dataval[1]) + ", " + str(a_leaf.dataval[2]) + " back to optimal path list")
            a_optimal_path_list.insert(0, (str(str(a_leaf.dataval[1]) + ", " + str(a_leaf.dataval[2]))))  #add every node along its ancestry to a string
            a_leaf = a_leaf.a_parent  #go to the previous leaf
        else: #if it isnt a goal node
          a_neighbours = [] #look at its neighbours
          if (a_leaf.dataval[1] > 0): #is the x value above 0?
            a_neighbours.append(model[a_leaf.dataval[2]][a_leaf.dataval[1] - 1])  #if it is, then that means the node to the left is a neighbour
          if (a_leaf.dataval[2] > 0):  #is the y value above 0?
            a_neighbours.append(model[a_leaf.dataval[2] - 1][a_leaf.dataval[1]])  #if so, then there must be a neighbour above it
          if (a_leaf.dataval[1] < (len(model[0]) - 1)):  #is the x value below the maximum length?
            a_neighbours.append(model[a_leaf.dataval[2]][a_leaf.dataval[1] + 1])  #if so it must have a neighbour to the right of it
          if (a_leaf.dataval[2] < (len(model) - 1)):  #is the y value below the max length?
            a_neighbours.append(model[a_leaf.dataval[2] + 1][a_leaf.dataval[1]])  #if so, there must be a node below it

          for x in a_neighbours:  #for every neighbour x
            in_frontier = False
            in_explored = False
          
            for y in a_frontier: #check if it is in the frontier by comparing datavalues
              if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                in_frontier = True
                break
            if not(in_frontier):
              for y in a_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
              for y in b_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
              for y in c_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break

            if x.dataval[0] == 'B' or x.dataval[0] == 'C':
              in_explored = False
              
            if not(in_frontier) and not(in_explored) and not(x.dataval[0] == 'X'):  #if the neighbour is not in the frontier, not explored, and not an X value (wall)
              x.a_parent = a_leaf  #its parent is leaf now
              if (x.dataval[0] == 'B' or x.dataval[0] == 'C'):  #if x is a goal node
                x.a_path_cost = a_leaf.a_path_cost  #then its traversal cost is 0 so its path cost is the same as the previous path
                x.a_priority = x.a_path_cost + 0  #and its priority is also 0 meaning it is equal to the path cost
              else:  #otherwise it is a number
                x.a_path_cost = a_leaf.a_path_cost + int(x.dataval[0])  #the path cost is the previous path cost + the traversal cost
                x.a_priority = x.a_path_cost + x.dataval[3]  #the priority is the total path cost + the priority

              if (len(a_frontier) == 0):  #if the frontier was empty
                a_frontier.append(x)  #just add this node to it point blank
              else:  
                for y in range(len(a_frontier)):  #otherwise, check through the frontier
                  if x.a_priority <= a_frontier[y].a_priority:  #if this node's priority is less than the current node being checked in frontier
                    a_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(a_frontier) - 1):
                    a_frontier.append(x)
            elif (in_frontier) and not(in_explored): #otherwise, if it is in the frontier (it cant be a wall cause a wall wouldnt be added so no need to check)
              if x.a_path_cost > (a_leaf.a_path_cost + int(x.dataval[0])):
                a_frontier.remove(x)
                x.a_parent = a_leaf
                x.a_path_cost = a_leaf.a_path_cost + int(x.dataval[0])
                x.a_priority = x.a_path_cost + x.dataval[3]
                for y in range(len(a_frontier)):
                  if x.a_priority <= a_frontier[y].a_priority:
                    a_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(a_frontier) - 1):
                    a_frontier.append(x)
            elif (in_frontier) and (in_explored):
                a_frontier.remove(x)

          #print("A's Current frontier: ")
         # for i in range(len(a_frontier)):
          #  print(str(a_frontier[i].dataval) + " p: " + str(a_frontier[i].a_priority))
         # print("A's Explored: ")
        #  for i in range(len(a_explored)):
         #   print(a_explored[i].dataval)
                          
          a_neighbours = []                      
            
    if (b_frontier != []) and (b_goal == False): 
        b_leaf = b_frontier.pop(0)  #otherwise, take the top priority node

        for y in a_frontier:  #check if it is in explored by comparing datavalues
          if (b_leaf.dataval[1] == y.dataval[1] and b_leaf.dataval[2] == y.dataval[2]):
            a_frontier.remove(y)
            break
        for y in c_frontier:  #check if it is in explored by comparing datavalues
          if (b_leaf.dataval[1] == y.dataval[1] and b_leaf.dataval[2] == y.dataval[2]):
            c_frontier.remove(y)
            break

        print("\nB's current node: ") 
        print(b_leaf.dataval)

        b_explored.append(b_leaf)
        if b_leaf.dataval[0] == 'A' or b_leaf.dataval[0] == 'C':  #if it is a goal node
          print("B's Goal reached!")
          b_goal = True
          b_optimal_path_cost = b_leaf.b_path_cost  #the optimal path cost is its path cost
          while b_leaf != None:  #trace back its ancestry to the top (parent = none is the top)
            b_optimal_path_list.insert(0, (str(str(b_leaf.dataval[1]) + ", " + str(b_leaf.dataval[2]))))  #add every node along its ancestry to a string
            b_leaf = b_leaf.b_parent  #go to the previous leaf
        else: #if it isnt a goal node
          b_neighbours = [] #look at its neighbours
          if (b_leaf.dataval[1] > 0): #is the x value above 0?
            b_neighbours.append(model[b_leaf.dataval[2]][b_leaf.dataval[1] - 1])  #if it is, then that means the node to the left is a neighbour
          if (b_leaf.dataval[2] > 0):  #is the y value above 0?
            b_neighbours.append(model[b_leaf.dataval[2] - 1][b_leaf.dataval[1]])  #if so, then there must be a neighbour above it
          if (b_leaf.dataval[1] < (len(model[0]) - 1)):  #is the x value below the maximum length?
            b_neighbours.append(model[b_leaf.dataval[2]][b_leaf.dataval[1] + 1])  #if so it must have a neighbour to the right of it
          if (b_leaf.dataval[2] < (len(model) - 1)):  #is the y value below the max length?
            b_neighbours.append(model[b_leaf.dataval[2] + 1][b_leaf.dataval[1]])  #if so, there must be a node below it

          for x in b_neighbours:  #for every neighbour x
            in_frontier = False
            in_explored = False
        
            for y in b_frontier: #check if it is in the frontier by comparing datavalues
              if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                in_frontier = True
                break
            if not(in_frontier):
              for y in a_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
              for y in b_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
              for y in c_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break

            if x.dataval[0] == 'A' or x.dataval[0] == 'C':
              in_explored = False
          
            if not(in_frontier) and not(in_explored) and not(x.dataval[0] == 'X'):  #if the neighbour is not in the frontier, not explored, and not an X value (wall)
              x.b_parent = b_leaf  #its parent is leaf now
              if (x.dataval[0] == 'A' or x.dataval[0] == 'C'):  #if x is a goal node
                x.b_path_cost = b_leaf.b_path_cost  #then its traversal cost is 0 so its path cost is the same as the previous path
                x.b_priority = x.b_path_cost + 0  #and its priority is also 0 meaning it is equal to the path cost
              else:  #otherwise it is a number
                x.b_path_cost = b_leaf.b_path_cost + int(x.dataval[0])  #the path cost is the previous path cost + the traversal cost
                x.b_priority = x.b_path_cost + x.dataval[4]  #the priority is the total path cost + the priority

              if (len(b_frontier) == 0):  #if the frontier was empty
                b_frontier.append(x)  #just add this node to it point blank
              else:  
                for y in range(len(b_frontier)):  #otherwise, check through the frontier
                  if x.b_priority <= b_frontier[y].b_priority:  #if this node's priority is less than the current node being checked in frontier
                    b_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(b_frontier) - 1):
                    b_frontier.append(x)
            elif (in_frontier) and not(in_explored): #otherwise, if it is in the frontier (it cant be a wall cause a wall wouldnt be added so no need to check)
              if x.b_path_cost > (b_leaf.b_path_cost + int(x.dataval[0])):
                b_frontier.remove(x)
                x.b_parent = b_leaf
                x.b_path_cost = b_leaf.b_path_cost + int(x.dataval[0])
                x.b_priority = x.b_path_cost + x.dataval[4]
                for y in range(len(b_frontier)):
                  if x.b_priority <= b_frontier[y].b_priority:
                    b_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(b_frontier) - 1):
                    b_frontier.append(x)
            elif (in_frontier) and (in_explored):
              b_frontier.remove(x)
                  
        #  print("B's Current frontier: ")
         # for i in range(len(b_frontier)):
        #    print(str(b_frontier[i].dataval) + " p: " + str(b_frontier[i].b_priority))

        #  print("B's Explored: ")
         # for i in range(len(b_explored)):
         #   print(b_explored[i].dataval)
          
          b_neighbours = []             

    if (c_frontier != []) and (c_goal == False): 
        c_leaf = c_frontier.pop(0)  #otherwise, take the top priority node

        for y in a_frontier:  #check if it is in explored by comparing datavalues
          if (c_leaf.dataval[1] == y.dataval[1] and c_leaf.dataval[2] == y.dataval[2]):
            a_frontier.remove(y)
            break
        for y in b_frontier:  #check if it is in explored by comparing datavalues
          if (c_leaf.dataval[1] == y.dataval[1] and c_leaf.dataval[2] == y.dataval[2]):
            b_frontier.remove(y)
            break
          
        print("\nC's current node: ")
        print(c_leaf.dataval)

        c_explored.append(c_leaf)
        if c_leaf.dataval[0] == 'A' or c_leaf.dataval[0] == 'B':  #if it is a goal node
          print("C's Goal reached!")
          c_goal = True
          c_optimal_path_cost = c_leaf.c_path_cost  #the optimal path cost is its path cost
          while c_leaf != None:  #trace back its ancestry to the top (parent = none is the top)
            c_optimal_path_list.insert(0, (str(str(c_leaf.dataval[1]) + ", " + str(c_leaf.dataval[2]))))  #add every node along its ancestry to a string
            c_leaf = c_leaf.c_parent  #go to the previous leaf
        else: #if it isnt a goal node
          c_neighbours = [] #look at its neighbours
          if (c_leaf.dataval[1] > 0): #is the x value above 0?
            c_neighbours.append(model[c_leaf.dataval[2]][c_leaf.dataval[1] - 1])  #if it is, then that means the node to the left is a neighbour
          if (c_leaf.dataval[2] > 0):  #is the y value above 0?
            c_neighbours.append(model[c_leaf.dataval[2] - 1][c_leaf.dataval[1]])  #if so, then there must be a neighbour above it
          if (c_leaf.dataval[1] < (len(model[0]) - 1)):  #is the x value below the maximum length?
            c_neighbours.append(model[c_leaf.dataval[2]][c_leaf.dataval[1] + 1])  #if so it must have a neighbour to the right of it
          if (c_leaf.dataval[2] < (len(model) - 1)):  #is the y value below the max length?
            c_neighbours.append(model[c_leaf.dataval[2] + 1][c_leaf.dataval[1]])  #if so, there must be a node below it

          for x in c_neighbours:  #for every neighbour x
            in_frontier = False
            in_explored = False
        
            for y in c_frontier: #check if it is in the frontier by comparing datavalues
              if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                in_frontier = True
                break
            if not(in_frontier):
               for y in a_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
               for y in b_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break
               for y in c_explored:  #check if it is in explored by comparing datavalues
                if (x.dataval[1] == y.dataval[1] and x.dataval[2] == y.dataval[2]):
                  in_explored = True
                  break

            if x.dataval[0] == 'A' or x.dataval[0] == 'B':
              in_explored = False
          
            if not(in_frontier) and not(in_explored) and not(x.dataval[0] == 'X'):  #if the neighbour is not in the frontier, not explored, and not an X value (wall)
              x.c_parent = c_leaf  #its parent is leaf now
              if (x.dataval[0] == 'A' or x.dataval[0] == 'C'):  #if x is a goal node
                x.c_path_cost = c_leaf.c_path_cost  #then its traversal cost is 0 so its path cost is the same as the previous path
                x.c_priority = x.c_path_cost + 0  #and its priority is also 0 meaning it is equal to the path cost
              else:  #otherwise it is a number
                x.c_path_cost = c_leaf.c_path_cost + int(x.dataval[0])  #the path cost is the previous path cost + the traversal cost
                x.c_priority = x.c_path_cost + x.dataval[5]  #the priority is the total path cost + the priority

              if (len(c_frontier) == 0):  #if the frontier was empty
                c_frontier.append(x)  #just add this node to it point blank
              else:  
                for y in range(len(c_frontier)):  #otherwise, check through the frontier
                  if x.c_priority <= c_frontier[y].c_priority:  #if this node's priority is less than the current node being checked in frontier
                    c_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(c_frontier) - 1):
                    c_frontier.append(x)
            elif (in_frontier) and not(in_explored): #otherwise, if it is in the frontier (it cant be a wall cause a wall wouldnt be added so no need to check)
              if x.c_path_cost > (c_leaf.c_path_cost + int(x.dataval[0])):
                c_frontier.remove(x)
                x.c_parent = c_leaf
                x.c_path_cost = c_leaf.c_path_cost + int(x.dataval[0])
                x.c_priority = x.c_path_cost + x.dataval[5]
                for y in range(len(c_frontier)):
                  if x.c_priority <= c_frontier[y].c_priority:
                    c_frontier.insert(y, x)  #insert it ahead of the node being checked
                    break  #end check
                  elif y == (len(c_frontier) - 1):
                    c_frontier.append(x)
            elif (in_frontier) and (in_explored):
              c_frontier.remove(x)
                  
        #  print("C's Current frontier: ")
        #  for i in range(len(c_frontier)):
        #    print(str(c_frontier[i].dataval) + " p: " + str(c_frontier[i].c_priority))

         # print("C's Explored: ")
         # for i in range(len(c_explored)):
         #   print(c_explored[i].dataval)
          
          c_neighbours = []             

  a_optimal_path_string = ""
  for i in range(len(a_optimal_path_list)):
    a_optimal_path_string += "(" + a_optimal_path_list[i] + ")\n"
    
  b_optimal_path_string = ""
  for i in range(len(b_optimal_path_list)):
    b_optimal_path_string += "(" + b_optimal_path_list[i] + ")\n"
    
  c_optimal_path_string = ""
  for i in range(len(c_optimal_path_list)):
    c_optimal_path_string += "(" + c_optimal_path_list[i] + ")\n"

  a_explored_list_string = ""
  for i in range(len(a_explored)):
    a_explored_list_string += "(" + str(a_explored[i].dataval[1]) + ", " + str(a_explored[i].dataval[2]) + ")\n"
  
  b_explored_list_string = ""
  for i in range(len(b_explored)):
    b_explored_list_string += "(" + str(b_explored[i].dataval[1]) + ", " + str(b_explored[i].dataval[2]) + ")\n"
  
  c_explored_list_string = ""
  for i in range(len(c_explored)):
    c_explored_list_string += "(" + str(c_explored[i].dataval[1]) + ", " + str(c_explored[i].dataval[2]) + ")\n"
    
  f = open(a_data_filename, "w")
  f.write("A Data:\nOptimal Path:\n")
  f.write(a_optimal_path_string)
  f.write("\nExplored List:\n")
  f.write(a_explored_list_string)
  f.write("\nOptimal Path Cost:\n")
  f.write(str(a_optimal_path_cost))
  f.close()
  
  f = open(b_data_filename, "w")
  f.write("B Data:\nOptimal Path:\n")
  f.write(b_optimal_path_string)
  f.write("\nExplored List:\n")
  f.write(b_explored_list_string)
  f.write("\nOptimal Path Cost:\n")
  f.write(str(b_optimal_path_cost))
  f.close()
  
  f = open(c_data_filename, "w")
  f.write("C Data:\nOptimal Path:\n")
  f.write(c_optimal_path_string)
  f.write("\nExplored List:\n")
  f.write(c_explored_list_string)
  f.write("\nOptimal Path Cost:\n")
  f.write(str(c_optimal_path_cost))
  f.close()

  new_model_string = ""

  for x in a_explored:
    if (model[x.dataval[2]][x.dataval[1]].dataval[0] != 'A' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'B' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'C'):
      model[x.dataval[2]][x.dataval[1]].dataval[0] = 'a'
    
  for x in b_explored:
    if (model[x.dataval[2]][x.dataval[1]].dataval[0] != 'A' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'B' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'C'):
      model[x.dataval[2]][x.dataval[1]].dataval[0] = 'b'
    
  for x in c_explored:
    if (model[x.dataval[2]][x.dataval[1]].dataval[0] != 'A' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'B' and model[x.dataval[2]][x.dataval[1]].dataval[0] != 'C'):
      model[x.dataval[2]][x.dataval[1]].dataval[0] = 'c'

  for i in range(len(model)):  #assign heuristic values based on proximity to goal node
    for j in range(len(model[i])):
      new_model_string = new_model_string + model[i][j].dataval[0] + ", "
    new_model_string = new_model_string + "\n"

  f = open(final_state_filename, "w")
  f.write(new_model_string)
  f.close()


  return 0

pathfinding("Test3/input.txt", "Test3/a_Data.txt", "Test3/b_Data.txt", "Test3/c_Data.txt", "Test3/output.txt")
pathfinding("Test4/input.txt", "Test4/a_Data.txt", "Test4/b_Data.txt", "Test4/c_Data.txt", "Test4/output.txt")


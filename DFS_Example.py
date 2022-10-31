
# IDEA:
# 1) Take cartesian product of nodes and domain to generate an *ordered* list, named key, of every node in the search space.
#    The order will reflect the order provided in the "nodes" parameter. Any order is permissible.
#
#    For example:
#                   nodes = [A,B]
#                   domain = {1,2}
#                   key = [A1, A2, B1, B2]

# 2) It can be said that every node in a set shares an edge with every node in the set directly following it - where a set is
#  defined as a subarray of key which contains all nodes of a certain letter.
#
#    For example (from above):
#                   Set 1: A1, A2
#                   Set 2: B1, B2
#
#                   ** Every node in Set 1 has an edge with every node in Set 2 **
#
#                   Edges: (A1,B1), (A1, B2), (A2, B1), (A2,B2)

# 3) This pattern can be exploited to obtain an equation that given any index of any node in the array key,
#    will return the index of the first node in the following set. This permits a O(variables * domain) space complexity
#    because key contains the entire search space and is of length len(variables) * len(domain)
#
#              domain_size - (index % domain_size) + index = index of first neighbor in next set
#

# -------- Create list key and populate with all nodes of search space --------
key = []


def create_search_space(nodes, domain):
    for node in range(len(nodes)):
        for value in range(len(domain)):
            key.append(nodes[node] + str(domain[value]))


def consistency_check(path):

    # Reads the indices of a given path into a dictionary where a node label and value are stored as key/value pair
    # For example:
    #               [0] --> 'A1' --> 'A' : 1

    value_map = {}
    for node in path:
        temp1 = key[node]
        value_map[temp1[0:1]] = int(temp1[1:2])

    # Checks constraints - False if broken, otherwise True
    if 'A' in value_map.keys() and 'G' in value_map.keys():
        if value_map['G'] >= value_map['A']:
            return False

    if 'G' in value_map.keys() and 'C' in value_map.keys():
        if abs(value_map['G'] - value_map['C']) != 1:
            return False

    if 'D' in value_map.keys() and 'C' in value_map.keys():
        if value_map['D'] == value_map['C']:
            return False

    if 'G' in value_map.keys() and 'F' in value_map.keys():
        if value_map['G'] == value_map['F']:
            return False

    if 'E' in value_map.keys() and 'F' in value_map.keys():
        if abs(value_map['E'] - value_map['F']) % 2 == 0:
            return False

    if 'A' in value_map.keys() and 'H' in value_map.keys():
        if value_map['A'] > value_map['H']:
            return False

    if 'H' in value_map.keys() and 'C' in value_map.keys():
        if abs(value_map['H'] - value_map['C']) % 2 == 1:
            return False

    if 'E' in value_map.keys() and 'C' in value_map.keys():
        if value_map['E'] == value_map['C']:
            return False

    if 'H' in value_map.keys() and 'F' in value_map.keys():
        if value_map['H'] == value_map['F']:
            return False

    if 'F' in value_map.keys() and 'B' in value_map.keys():
        if abs(value_map['F'] - value_map['B']) != 1:
            return False

    if 'H' in value_map.keys() and 'D' in value_map.keys():
        if value_map['H'] == value_map['D']:
            return False

    if 'E' in value_map.keys() and 'D' in value_map.keys():
        if value_map['E'] >= (value_map['D'] - 1):
            return False

    if 'C' in value_map.keys() and 'F' in value_map.keys():
        if value_map['C'] == value_map['F']:
            return False

    if 'G' in value_map.keys() and 'H' in value_map.keys():
        if value_map['G'] >= value_map['H']:
            return False

    if 'D' in value_map.keys() and 'G' in value_map.keys():
        if value_map['D'] < value_map['G']:
            return False

    if 'E' in value_map.keys() and 'H' in value_map.keys():
        if value_map['E'] == (value_map['H'] - 2):
            return False

    if 'D' in value_map.keys() and 'F' in value_map.keys():
        if value_map['D'] == (value_map['F'] - 1):
            return False

    return True


def dfs_with_pruning():
    solutions = []
    frontier = []
    failedBranches = 0

    # Initialize frontier with first set of nodes
    for i in range(len(domain)):
        frontier.append([i])

    while frontier:
        path = frontier.pop()

        if consistency_check(path):
            if len(path) == len(nodes):

                # If path values pass consistency check and path is of correct length, add to solution and print path
                solutions.append(path)
                showBranch(path, status=True)

            else:

                # If no constraints were broken but path is not yet long enough, keep searching
                showBranch(path, status=False)
                failedBranches += 1

                # Get closest neighbor of next set
                mostRecentNode = path[len(path) - 1]
                closestNeighbor = get_nearest_neighbor(
                    mostRecentNode, len(domain))
                counter = 0

                # Add all neighbors to a copy of current path and push expanded path to stack
                while counter < len(domain):
                    temp = list(path)
                    nextNeighbor = closestNeighbor + counter
                    temp.append(nextNeighbor)
                    frontier.append(temp)
                    counter += 1
        else:
            # If path fails consistency check it remains popped from the frontier and is not expanded further (prun)
            failedBranches += 1

    print("FAILING BRANCHES:", failedBranches)
    print("NUMBER OF SOLUTIONS:", len(solutions))
    print("TOTAL BRANCHES:", len(solutions) + failedBranches)
    for soln in solutions:
        showBranch(soln, True)


def get_nearest_neighbor(index, domain_size):
    return domain_size - (index % domain_size) + index


def showBranch(path, status):
    branch = []
    for node in path:
        branch.append(key[node])

    if status:
        print(branch, "SOLUTION")
    else:
        print(branch, "FAILURE")


nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
sedon = (nodes[::-1])
domain = [1, 2, 3, 4]

create_search_space(nodes, domain)
dfs_with_pruning()

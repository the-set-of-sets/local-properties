import itertools
import sys

"""
Given input string, for example 12141218, this program computes local
properties it satisfies.

The config 12141218 corresponds to a set of 9 points, each at the | marker:
|1|2|1|4|1|2|1|8|
The 1, 2, 4, 8, represent Z-linear independent real distances.

For example, consider the following four points x, y, z, w:
|1|2|1|4|1|2|1|8|
x   y     z   w
The distance between x and y is "12" and the distance between z and w is "21".
Note that "12" and "21" are the same, since they correspond to "1" + "2".
The distance between y and z is "141", and so on. The points x, y, z, w
determine 4 distinct distances.

We say a config satisfies the "(k,l) condition" if every subset of k points
determines at least l distinct distances.
"""
def distance_string_to_dict(s):
    """Given distance string s, converts it to a dict.
    For example "141" is converted to { 1: 2, 4: 1 }."""
    d = dict()
    for i in s:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    return d

def distances_of_subset(config, subset):
    """Given config and subset, return the number of disances determined by
    that subset. For example given 1214 and (0, 2, 4), it returns 3.
    In this case, the points in the subset are |12|14| so the distances are
    12, 14, 1214."""
    distances = [] # list of distances
    # distance "141" is represented as a dict with 1: 2, 4: 1
    for p1,p2 in itertools.combinations(subset, 2):
        new_distance = distance_string_to_dict( config[p1:p2] )
        if new_distance not in distances:
            distances.append(new_distance)
    return len(distances)

def count_local_property(config, k):
    """Given config and k, prints the smallest number l of distinct
    distances determined by any subset of k points in config."""
    n = len(config) + 1 # number of points in config
    # We keep track of the minimum number of distances determined by k points,
    # as well as which poins determine this minimum number of distances.
    min_distance = n**k # certainly smaller than this
    min_distance_subset = () # subset which determine min_distance
    for subset in itertools.combinations(range(n), k):
        distance = distances_of_subset(config, subset)
        if min_distance > distance:
            min_distance, min_distance_subset = distance, subset
    print("(",k,",",min_distance,") condition with ",min_distance_subset,sep = '')

def count_local_properties(config, k):
    """Given config and k, prints the smallest number l of distinct
    distances determined by any subset of k points in config.
    If k = 0, does this for all 3 <= k <= len(config) + 1. """
    if k != 0:
        return count_local_property(config, k)
    if k == 0:
        for k in range(3, len(config) + 1):
            count_local_property(config, k)

def is_valid_config(config):
    return config.isalnum()

def is_valid_k(config, k):
    return (3 <= k and k <= len(config) + 1) or (k == 0)

def print_usage():
    print("count_local_properties.py <config> <k (optional)>")
    print("-- <config>: e.g. 12141218")
    print("\tSymbols in config must be single characters in a-z0-9")
    print("-- <k>: any positive integer. Local property to be computed.")
    print("\tk should satisfy 3 <= k <= len(config) + 1")

if __name__ == "__main__":
    should_print_usage = False
    # Make sure first argument <config> is well-formed
    try:
        config = sys.argv[1]
    except IndexError:
        should_print_usage = True
        config = "" # default value
    # Make sure second argument <k> is well-formed
    try:
        k = int(sys.argv[2])
    except ValueError:
        should_print_usage = True
        k = 0 # default value
    except IndexError:
        k = 0 # this means we want to compute for all k
    # Check that <config> and <k> have valid values
    if not (is_valid_config(config) and is_valid_k(config, k) ):
        should_print_usage = True
    # Run actual program
    if should_print_usage:
        print_usage()
    else:
        count_local_properties(config, k)

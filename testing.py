import math

a = 0.1
b = 1.5
g = 5
input_space = set('abc')
trans_func = {
    1: {'a': 'x', 'b': 'x', 'c': 'y'},
    2: {'a': 'x', 'b': 'y'},
    3: {'b': 'x', 'c': 'y'},
    4: {'b': 'x', 'a': 'x'},
    5: {'c': 'z'}
}

def mean(values):
    s = 0
    for v in values:
        s = s + v
        
    return s / len(values)

def same(g1, g2):
    return set(g1) == set(g2)

def split_group(trans_func, group, dister):
    interpart = {}
    for state in group:
        try:
            out = trans_func[state][dister]
            if out in interpart :
                interpart[out].append(state)
            else :
                interpart[out] = [state]
        except:
            pass
        
    return list(interpart.values())
            

def split_partition(trans_func, partition, dister):
    newpart = []
    
    for group in partition:
        # we ignore discreete partitions
        if len(group) == 1:
            continue
        
        group_part = split_group(trans_func, group, dister)
        if group_part and not same(group, group_part[0]):
            newpart = newpart + group_part
    
    return newpart
        
def count_discreete(partition):
    count = 0
    for group in partition:
        count = count + 1 if len(group) == 1 else 0
        
    return count
    
def partial_fitness(a, b, g, xnew, xprev, ynew, yprev, size):
    return a*(xprev*math.exp(xprev + xnew))/math.pow(size, g) + b*(yprev + ynew)/size
    
def sstfitness(trans_func, seq):
    values = []
    
    # x is the number of discreete partitions
    xprev = 0
    # y is the number of groups
    yprev = 0
    partlen = 0
    partition = [list(trans_func.keys())]
    for i in range(len(seq)):
        char = seq[i]
        if char is '#':
            continue
            
        partlen = partlen + 1
        partition = split_partition(trans_func, partition, char)
        xnew = count_discreete(partition)
        ynew = len(partition) - xnew
        f = partial_fitness(a, b, g, xnew, xprev, ynew, yprev, partlen)
        values.append(f)
        
        xprev = xnew
        yprev = ynew
        
    return mean(values)

sstfitness(trans_func, 'aa#caab#c')
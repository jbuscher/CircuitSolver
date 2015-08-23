import collections

def check_closed(ien):
    """Checks if a mesh is closed by checking number of occurences of each node
    Inputs: 
    ien and nx2 int python list
    
    Output:
    Bool True or False
    """
    counter=collections.defaultdict(int)
    for pair in ien:
        for i in pair:
            counter[i]+=1
    if min(counter.values())<2:
        return False
    else: 
        return True


def replace_ms(ms,m_to_s,i,j,v_offset):
    """Makes j slave to i and all of j's slaves also slave to i
    Inputs:
    ms 
    m_to_s
    i
    j
    v_offset: voltage difference between i and j

    Outputs:
    (implicitly passed)
    ms
    m_to_s
    
    """
    ms[j][0]=i              # make j slave to i
    ms[j][1]+=v_offset
    for s in m_to_s[j]:     # make all of j's slaves slaves to i's master
        ms[s][0]=i
        ms[s][1]+=v_offset
    m_to_s[i]+=m_to_s[j]    # give i's master all of j's slaves
    m_to_s[i].append(j)     # give i's master j as slaves
    m_to_s.pop(j)           #j is not longer master 


def simplify_circuit(ien,connection_type,connection_value):

    assert(len(ien)==len(connection_type))                                   
    num_nodes=len(set([i for pair in ien for i in pair]))
    
    ms=[[-1,0] for _ in range(num_nodes)]
    values=[[] for _ in range(num_nodes)]
    node_refs=[[] for _ in range(num_nodes)]
    circuit_type=[[] for _ in range(num_nodes)]

    m_to_s=collections.defaultdict(list)

    for i,pair in enumerate(ien):
        v=connection_value[i]
        if connection_type[i]=='w' or connection_type[i]=='v':
            ms0=ms[pair[0]][0]
            ms1=ms[pair[1]][0]
            #print(pair,ms[pair[0]],ms[pair[1]],v)
            if   ms0==-1 and ms1==-1:
                replace_ms(ms,m_to_s,pair[0],pair[1],v)
            elif ms0>-1  and ms1==-1: # if 0 is slave and 1 is master
                replace_ms(ms,m_to_s,ms[pair[0]][0],pair[1],v+ms[pair[0]][1])
            elif ms0==-1 and ms1>-1 :
                replace_ms(ms,m_to_s,ms[pair[1]][0],pair[0],v+ms[pair[1]][1])
            else:# ms0>-1  and ms1>-1 :
                replace_ms(ms,m_to_s,ms[pair[1]][0],ms[pair[0]][0],v+ms[pair[1]][1])
                
        elif connection_type[i]=='i' or connection_type[i]=='r': 
            for p in range(2):
                values[pair[p]].append(connection_value[i])
                circuit_type[pair[p]].append(connection_type[i])
                node_refs[pair[p]].append(pair[(p+1)%2])
            
            if connection_type=='i':
                values[pair[1]][-1]=-values[pair[1]][-1]
    return node_refs, circuit_type, values, ms
    #print (ms)           
    #print (node_refs)
    #print (circuit_type)
    #print (values)
    #import circuit_solver 
    #circuit_solver.solve(values,circuit_type,node_refs,ms)

def main():
    #Test Case
    ien=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,0],[0,12],[12,13],[13,6]]
    connection_type=['w','w','w','v','v','r','w','w','w','r','v','r','w','w','r']
    connection_value=[0,0,0,10,5,15,0,0,0,5,4,10,0,0,20]
    
    #shuffle test case
    from random import shuffle
    index_shuf=list(range(len(ien)))
    shuffle(index_shuf)
    ien2=[ien[i] for i in index_shuf]
    connection_type2=[connection_type[i] for i in index_shuf]
    connection_value2=[connection_value[i] for i in index_shuf]
    
    print (ien2)
    reduce(ien2,connection_type2,connection_value2)
    

if __name__=='__main__':
    main()


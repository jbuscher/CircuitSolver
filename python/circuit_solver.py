import collections
import numpy as np
from numpy.linalg import inv


def replace_ms(ms, m_to_s, i, j, v_offset):
    """Makes j slave to i and all of j's slaves also slave to i
    Inputs:
    ms 
    m_to_s
    i
    j
    v_offset: voltage difference between i and j

    Outputs:
    (implicitly passed)
    ms, m_to_s
    """
    
    ms[j][0] = i              # make j slave to i
    ms[j][1] += v_offset
    for s in m_to_s[j]:     # make all of j's slaves slaves to i's master
        ms[s][0] = i
        ms[s][1] += v_offset
    m_to_s[i] += m_to_s[j]    # give i's master all of j's slaves
    m_to_s[i].append(j)     # give i's master j as slaves
    m_to_s.pop(j)           # j is not longer master 


class Circuit:
    def __init__(self, ien, connection_type, connection_value):
        self.ien = ien
        self.connection_type = connection_type
        self.connection_value = connection_value

    def check_closed(self):
        """Check if mesh is closed by ensuring each node is listed 2+ times
        Inputs: 
        ien and nx2 int python list
        
        Output:
        Bool True or False
        """
        counter = collections.defaultdict(int)
        for pair in self.ien:
            for i in pair:
                counter[i] += 1
        if min(counter.values()) < 2:
            return False
        else: 
            return True

    def simplify(self):
        connection_type = self.connection_type
        ien = self.ien
        connection_value = self.connection_value

        assert(len(ien) == len(connection_type))                                   
        num_nodes = len(set([i for pair in ien for i in pair]))
        
        ms = [[-1, 0] for _ in range(num_nodes)]
        values = [[] for _ in range(num_nodes)]
        node_refs = [[] for _ in range(num_nodes)]
        circuit_type = [[] for _ in range(num_nodes)]

        m_to_s = collections.defaultdict(list)

        for i, pair in enumerate(ien):
            v = connection_value[i]
            if connection_type[i] == 'w' or connection_type[i] == 'v':
                ms0 = ms[pair[0]][0]
                ms1 = ms[pair[1]][0]
                
                if ms0 == -1 and ms1 == -1:
                    replace_ms(ms, m_to_s, pair[0], pair[1], v)
                elif ms0 > -1 and ms1 == -1:
                    replace_ms(ms, m_to_s, ms[pair[0]][0], pair[1], v+ms[pair[0]][1])
                elif ms0 == -1 and ms1 > -1:
                    replace_ms(ms, m_to_s, ms[pair[1]][0], pair[0], v+ms[pair[1]][1])
                else:  #ms0 > -1  and ms1 > -1
                    replace_ms(ms, m_to_s, ms[pair[1]][0], ms[pair[0]][0], v+ms[pair[1]][1])
                    
            elif connection_type[i] == 'i' or connection_type[i] == 'r': 
                for p in range(2):
                    values[pair[p]].append(connection_value[i])
                    circuit_type[pair[p]].append(connection_type[i])
                    node_refs[pair[p]].append(pair[(p+1)%2])
                
                if connection_type == 'i':
                    values[pair[1]][-1] = -values[pair[1]][-1]
        
        self.node_refs = node_refs
        self.circuit_type = circuit_type
        self.values = values
        self.ms = ms

    def solve(self):
        values = self.values
        circuit_type = self.circuit_type
        node_refs = self.node_refs
        ms = self.ms

        # constants
        GROUND = 0
        
        # this will be used to map masters to their actual values
        num_values = len(values)
        master_location = []
        msmap = {}
        counter = 0
        for i in range(num_values):
            if ms[i][0] == -1:
                master_location.append(i)
                msmap[i] = counter
                counter += 1
        
        num_rows = len(master_location)
        a = np.zeros([num_rows, num_rows])
        lhs = np.zeros([num_rows, 1])

        for i in range(len(values)):
            if i == GROUND or ms[i][0] == GROUND:
                continue
            elif ms[i][0] > -1:
                r = ms[i][0]
            else:
                r = i
            
            for j, k in enumerate((node_refs[i])):
                # r, c are the row and column being changed
                # i is the node being looped, if i is a slave r->ms[i], else r = i
                # k is the column being altered, if k is a slave, c = ms[k], else c = k
                # every time k is a slave we want it v_offset changed 
                
                if ms[k][0] > -1:
                    c = ms[k][0]
                    v_offset = ms[k][1]
                elif ms[i][0] > -1:
                    c = k
                    v_offset = -ms[i][1]
                else:
                    c = k
                    v_offset = 0
        
                r2 = msmap[r] 
                c2 = msmap[c]
                if circuit_type[i][j] == 'r':
                    a[r2, r2] += 1/values[i][j]
                    lhs[r2] += v_offset/values[i][j]
                    #print(v_offset/values[i][j],r2)
                    if c2 > 0:
                        a[r2, c2] -= 1/values[i][j]
                if circuit_type[i][j] == 'i':
                    lhs[r2] += values[i][j]
        
        a = np.delete(a, GROUND, 0)
        a = np.delete(a, GROUND, 1)
        lhs = np.delete(lhs, GROUND, 0)

        #print(a)
        #print(lhs)
        
        b = inv(a).dot(lhs)
        b = b.flatten() 
        b = np.insert(b, 0, 0)
        
        voltages = [0]*num_values
        for i in range(1, num_values):
            if ms[i][0] == -1:
                voltages[i] = b[msmap[i]]
            else:
                voltages[i] = b[msmap[ms[i][0]]]+ms[i][1]  # add voltage offset 
                
        self.voltages = voltages
        
def main():
    ien=[[0,1],[0,3],[0,2],[1,3],[3,2],[1,2]]
    connection_type=['i','v','r','r','r','r']
    connection_value=[1,10,5,2,10,5]
    
    circuit=Circuit(ien,connection_type,connection_value)        
    circuit.simplify()
    circuit.solve()
    print (circuit.voltages)
    
if __name__=='__main__':
    main()
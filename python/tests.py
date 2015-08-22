import unittest
import circuit_solver
import simplify_circuit as sc

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):
    def testOne(self):
        self.assertTrue(IsOdd(1))

    def testTwo(self):
        self.assertFalse(IsOdd(2))

class current_source(unittest.TestCase):
    def testOne(self):
        pass

class voltage_source(unittest.TestCase):
    def test_one(self): 
        values={      0:[20,10],  1:[], 2:[15],  3:[15,20,5],     4:[5],   5:[10]}
        circuit_type={0:['r','r'],1:[], 2:['r'], 3:['r','r','r'], 4:['r'], 5:['r']}
        node_refs={   0:[3,5],    1:[], 2:[3],   3:[2,0,4],       4:[3],   5:[0]}
        ms={0:[-1,0],1:[0,10],2:[0,15],3:[-1,0],4:[-1,0],5:[4,4]} #0 is master
        voltages=circuit_solver.solve(values,circuit_type,node_refs,ms)
    
    def test_two(self):    
        ien=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,0],[0,12],[12,13],[13,6]]
        connection_type=['w','w','w','v','v','r','w','w','w','r','v','r','w','w','r']
        connection_value=[0,0,0,10,5,15,0,0,0,5,4,10,0,0,20]
        node_refs, circuit_type, values, ms=sc.simplify_circuit(ien,connection_type,connection_value)
        voltages=circuit_solver.solve(values,circuit_type,node_refs,ms)
        compare2=[0., 0., 0., 0., 10., 15., 4., 4., 4., 4., 4./3, 16./3, 0., 0.]
        for i in range(len(compare2)): self.assertAlmostEqual(voltages[i],compare2[i])


class current_and_voltage_source(unittest.TestCase):
    pass
"""
    #ms=[-1,0,0,-1,5,-1] 

    solve(values,circuit_type,node_refs,ms)

    #test case 1
    values={0:[5,-10,10],1:[5,10,20],2:[10,10,5],3:[20,10,5]}
    circuit_type={0:['r','i','r'],1:['r','r','r'],2:['r','i','r'],3:['r','r','r']}
    node_refs={0:[1,2,3],1:[0,2,3],2:[1,0,3],3:[1,0,2]}
    ms=[[-1],[-1],[-1],[-1]]


    solve(values,circuit_type,node_refs,ms)

"""


def main():
    unittest.main()

if __name__ == '__main__':
    main()

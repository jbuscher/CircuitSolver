import unittest
import circuit_solver


class current_source_tests(unittest.TestCase):
    def template(self):
        pass
        #ien=[]
        #connection_type=[]
        #connection_value=[]
        #circuit=circuit_solver.Circuit(ien,connection_type,connection_value)        
        #circuit.simplify()
        #circuit.solve()

        #compare2=[]
        #for i in range(len(compare2)): 
        #    self.assertAlmostEqual(circuit.voltages[i],compare2[i])
    
    def test_one(self):
        pass
        ien=[[0,1],[0,2],[0,3],[1,3],[1,2],[3,2]]
        connection_type=['r','i','r','r','r','r']
        connection_value=[10,10,5,20,5,10]
        circuit=circuit_solver.Circuit(ien,connection_type,connection_value)        
        circuit.simplify()
        circuit.solve()

        compare2=[0,45.45454545,72.72727273,27.27272727]
        for i in range(len(compare2)): 
            self.assertAlmostEqual(circuit.voltages[i],compare2[i])


class voltage_source_tests(unittest.TestCase):
    
    def test_one(self): 
        circuit=circuit_solver.Circuit([],[],[])
        circuit.values={      0:[20,10],  1:[], 2:[15],  3:[15,20,5],     4:[5],   5:[10]}
        circuit.circuit_type={0:['r','r'],1:[], 2:['r'], 3:['r','r','r'], 4:['r'], 5:['r']}
        circuit.node_refs={   0:[3,5],    1:[], 2:[3],   3:[2,0,4],       4:[3],   5:[0]}
        circuit.ms={0:[-1,0],1:[0,10],2:[0,15],3:[-1,0],4:[-1,0],5:[4,4]} #0 is master

        circuit.solve()
  
        compare2=[0,10,15,4,4/3,16/3] 
        for i in range(len(compare2)): 
            self.assertAlmostEqual(circuit.voltages[i],compare2[i])

 
    def test_two(self):    
        ien=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],
             [8,9],[9,10],[10,11],[11,0],[0,12],[12,13],[13,6]]
        connection_type=['w','w','w','v','v','r','w','w','w','r','v','r','w','w','r']
        connection_value=[0,0,0,10,5,15,0,0,0,5,4,10,0,0,20]
        
        circuit=circuit_solver.Circuit(ien,connection_type,connection_value)        
        circuit.simplify()
        circuit.solve()

        compare2=[0., 0., 0., 0., 10., 15., 4., 4., 4., 4., 4./3, 16./3, 0., 0.]
        for i in range(len(compare2)): 
            self.assertAlmostEqual(circuit.voltages[i],compare2[i])


class current_and_voltage_source_tests(unittest.TestCase):
    def test_one(self):
        ien=[[0,1],[0,3],[0,2],[1,3],[3,2],[1,2]]
        connection_type=['i','v','r','r','r','r']
        connection_value=[1,10,5,2,10,5]
        
        circuit=circuit_solver.Circuit(ien,connection_type,connection_value)        
        circuit.simplify()
        circuit.solve()
        
        compare2=[0, 10.322580645, 6.12903226, 10.0]
        for i in range(len(compare2)): 
            self.assertAlmostEqual(circuit.voltages[i],compare2[i])


def main():
    unittest.main()

if __name__ == '__main__':
    main()

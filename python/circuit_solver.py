import numpy as np
from numpy.linalg import inv

def solve(values,circuit_type,node_refs,ms):

    #constants
    GROUND=0
    
    
    #this will be used to map masters to their actual values
    num_values=len(values)
    master_location=[]
    msmap={}
    counter=0
    for i in range(num_values):
        if ms[i][0]==-1:
            master_location.append(i)
            msmap[i]=counter
            counter+=1
    
    num_rows=len(master_location)
    a=np.zeros([num_rows,num_rows])
    lhs=np.zeros([num_rows,1])

    for i in range(len(values)):
        if i==GROUND or ms[i][0]==GROUND: continue
        if ms[i][0]>-1:
            r=ms[i][0]
        else:
            r=i
        
        for j,k in enumerate(node_refs[i]):
            k=node_refs[i][j]
            
            #r,c are the row and column being changed
            #i is the node being looped, if i is a slave r->ms[i], else r=i
            # k is the column being alter, if k is a slave, c=ms[k], else c=k
            #every time k is a slave we want it v_offset changed 
            
            if ms[k][0]>-1: 
                c=ms[k][0]
                v_offset=ms[k][1]
            elif ms[i][0]>-1:
                c=k
                v_offset=-ms[i][1]
            else:
                c=k
                v_offset=0
            r2=msmap[r]
            c2=msmap[c]

            if circuit_type[i][j]=='r':
                a[r2,r2]+=1/values[i][j]
                lhs[r2]+=v_offset/values[i][j]
                if c2>0:
                    a[r2,c2]-=1/values[i][j]
            if circuit_type[i][j]=='i':
                lhs[r2]-=values[i][j]

    a=np.delete(a,GROUND,0)
    a=np.delete(a,GROUND,1)
    lhs=np.delete(lhs,GROUND,0)
    
    b=inv(a).dot((lhs))
    b=b.flatten() 
    b=np.insert(b,0,0)
    
    voltages=[0]*num_values
    for i in range(1,num_values):
        if ms[i][0]==-1:
            voltages[i]=b[msmap[i]]
        else:
            voltages[i]=b[msmap[ms[i][0]]]+ms[i][1]
            
    return voltages
def main():

    #values={}
    #circuit_type={}
    #node_refs={}
    #ms={}

    #test case 2
    #values={      0:[10,20,10],    1:[10,5],    2:[5,15],    3:[15,20,5],     4:[5,4],     5:[4,10]}
    #circuit_type={0:['v','r','r'], 1:['v','v'], 2:['v','r'], 3:['r','r','r'], 4:['r','v'], 5:['v','r']}
    #node_refs={   0:[1,3,5],       1:[0,2],     2:[1,3],     3:[2,0,4],       4:[3,5],     5:[4,0]}
    #ms={0:[-1],1:[0,10],2:[0,15],3:[-1],4:[-1],5:[4,-4]} #0 is master
    
    #solver(values,circuit_type,node_refs,ms) 
    
    #print ('\n\n')

    values={      0:[20,10],  1:[], 2:[15],  3:[15,20,5],     4:[5],   5:[10]}
    circuit_type={0:['r','r'],1:[], 2:['r'], 3:['r','r','r'], 4:['r'], 5:['r']}
    node_refs={   0:[3,5],    1:[], 2:[3],   3:[2,0,4],       4:[3],   5:[0]}
    ms={0:[-1,0],1:[0,10],2:[0,15],3:[-1,0],4:[-1,0],5:[4,4]} #0 is master
    #ms=[-1,0,0,-1,5,-1] 
    
    solve(values,circuit_type,node_refs,ms) 
    
    #test case 1
    values={0:[5,-10,10],1:[5,10,20],2:[10,10,5],3:[20,10,5]}
    circuit_type={0:['r','i','r'],1:['r','r','r'],2:['r','i','r'],3:['r','r','r']}
    node_refs={0:[1,2,3],1:[0,2,3],2:[1,0,3],3:[1,0,2]}
    ms=[[-1],[-1],[-1],[-1]]
    
    
    solve(values,circuit_type,node_refs,ms) 

if __name__=='__main__':
    main()




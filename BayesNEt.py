import pandas as pd
import json
import numpy as np
import copy

class BayesNet:
    def __init__(self,file1,file2):
        self.e = self.getE(file2)
        self.parents = {}
        with open(file1) as data_file:
           self.network = json.load(data_file)
        for i in self.network.keys():
            if(self.network[i] != []):
                if i not in self.parents.keys():
                    self.parents[self.network[i][0]]= [i]
                else:
                    self.parents[self.network[i][0]].append(i)

    def enum_ask(self,X):
        q =[]
        e = copy.deepcopy(self.e)
        for x in [False,True]:
            e[X] = x
            variables = self.toposort()
            q.append(self.enum_all(variables,e))
        return self.normalize(q)


    def enum_all(self,vars, e):
        if(len(vars) == 0):
            return 1
        Y= vars[0]
        if Y in e:
            ret = 0


    def normalize(self,probs):
        norm=[]
        total= sum(probs)
        for x in probs:
            norm.append(x/total)
        return norm

    def toposort(self):
        vars = list(self.network.keys())
        vars.sort()
        #print(vars)
        s = set()
        l =[]
        while(len(s) < len(vars)):
            for v in vars:
                if v not in s:
                        if all(x in s for x in self.network[v]):
                            s.add(v)
                            l.append(v)
        l.reverse()
        return l

    def getE(self,file):
        df = pd.read_csv(file)
        matrix_df = df.as_matrix()
        data_count = {}
        for row in matrix_df:
            t = []
            for d in row:
                t.append(int(d))
            if tuple(t) in data_count.keys():
                data_count[tuple(t)] += 1
            else:
                data_count[tuple(t)] = 1

        total = 0
        for i in data_count.keys():
            total += data_count[i]
        #for j in data_count.keys():
         #   data_count[j] = data_count[j] / total
        return data_count

def main():
    net1 = BayesNet('bn1.json','data1.csv')
    print(net1.toposort())
    #print(net1.parents['High Car Value'])
    #print(net1.e)





if __name__ == '__main__':
    main()
import pandas as pd
import json
import numpy as np
import copy

class BayesNet:
    def __init__(self,file1,file2):
        self.e = self.getE(file2)
        self.parents = self.getParents(file1)

    def getParents(self,file):
        parents = {}
        with open(file) as data_file:
            network = json.load(data_file)
        #print(network)
        for i in network.keys():
            parents[i] = []
        for i in network.keys():
            if (network[i] != []):
                #print(i, network[i])
                if i not in parents.keys():
                    for j in network[i]:
                        parents[j] = [i]
                else:
                    for j in network[i]:
                        parents[j] = parents[j] + [i]
       #print(parents)
        return parents


    def getE(self, file):
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
            # for j in data_count.keys():
            #   data_count[j] = data_count[j] / total
        return data_count

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
        vars = list(self.parents.keys())

        vars.sort()
        #print(vars)
        s = set()
        l =[]
        while(len(s) < len(vars)):
            for v in vars:
                if v not in s:
                        if all(x in s for x in self.parents[v]):
                            s.add(v)
                            l.append(v)
        #l.reverse()
        return l


def main():
    net1 = BayesNet('bn1.json','data1.csv')
    print(net1.toposort())
    #print(net1.parents)
    #print(net1.parents['High Car Value'])
    #print(net1.parents['Good Engine'])
    #print(net1.e)





if __name__ == '__main__':
    main()
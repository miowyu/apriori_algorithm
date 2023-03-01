import numpy as np

def first_scan(data):
    table = np.array([[],[]],dtype=int)
    for line in data:
        line2 = np.array(line,dtype=int)
        search = np.searchsorted(table[0], line2)    
        find = search[search != len(table[0])]
        table[1][find] +=1
        new_element = line2[search == len(table[0])]
        new_table = np.array([new_element,np.ones(len(new_element))],dtype=int)
        table = np.concatenate((table,new_table), axis=1)
    return(table)

def first_scan(data):
    table = np.array([[],[]],dtype=int)
    for line in data:
        line2 = np.array(line,dtype=int)
        search = np.searchsorted(table[0], line2)    
        find = search[search != len(table[0])]
        table[1][find] +=1
        new_element = line2[search == len(table[0])]
        new_table = np.array([new_element,np.ones(len(new_element),dtype=int)],dtype=object)
        table = np.concatenate((table,new_table), axis=1)
    for i in range(len(table[0])):
        table[0][i] = [table[0][i]]   
    return(table)

def del_min(table,min_supp_n):
    rowsum = sum(table[1])
    table = np.delete(table, np.where(table[1] <= min_supp_n),axis=1)
    return(table)

def table_plus(table,table1):
    temp_table = []
    for i in table[0]:
        if type(i) == int:
            i = [i] 
        for j in table1[0]:
            templist = 0
            if type(j) != int:
                if j[0] not in i: 
                    templist = i+j
            else:
                if j not in i:
                    templist = i+[j]     
            if (templist != 0) :
                templist.sort()
                if templist not in temp_table:
                    temp_table.append(templist)
    new_table = np.array([temp_table,np.zeros(len(temp_table),dtype=int)],dtype=object)
    return(new_table)
            
def scanplus(table,data):
    for n in range(len(table[0])):
        target = table[0][n]
        count = 0
        for listdata in data:
            temp = True
            for i in target:
                if str(i) not in listdata:
                    temp = False
            if temp:
                count+=1
        table[1][n] = count
    return(table)

def combine_table(table,new_table):
    table = np.concatenate((table,new_table), axis=1)
    return(table)

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    final_list.sort()
    return final_list

def defferent_set(lst1,lst2):
    final_list = set(lst1).difference(set(lst2))
    return final_list

#========main============
#input file
path = 'input.txt'
f = open(path,"r")
text = []
for line in f:
    text.append(line.split(' ')[0:-1])
f.close
#input min_supp&min_conf
min_supp = float(input("please enter your min_supp : "))
min_conf = float(input("please enter your min_conf : "))
min_supp_n = min_supp * len(text)
#scan first time
table = first_scan(text)
table = del_min(table,min_supp_n=min_supp_n)
#scan all possible combination
temp_table = table
output_table = temp_table
n = 1
while (len(temp_table[0]) > n) & (len(table[0]) >= n):
    n+=1
    temp_table = table_plus(temp_table,table)
    temp_table = scanplus(temp_table,text)
    temp_table = del_min(temp_table,min_supp_n=min_supp_n)
    output_table = combine_table(output_table,temp_table)
#output   
outpath = 'output.txt'
f = open(outpath, 'w')
f.write("under min_supp=%s and min_conf=%s\n"%(min_supp,min_conf))
for i in range(len(output_table[0])):
    for j in range(i+1,len(output_table[0])):
        
        if Union(output_table[0][i],output_table[0][j]) == output_table[0][j]:
            if (output_table[1][j]/output_table[1][i]) > min_conf:
                conf = round(output_table[1][j]/output_table[1][i],(len(str(min_conf))-2))
                outstr = "%s -> %s (%s)\n"%(set(output_table[0][i]),defferent_set(output_table[0][j],output_table[0][i]),conf)           
                f.write(outstr)
f.close()
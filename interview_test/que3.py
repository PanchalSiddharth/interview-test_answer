def maxConsOne(ls): 
    count = 0
    lst=[]
    for i in range(len(ls)): 
        if (ls[i] == 0): 
            count = 0
        else: 
            count+= 1 
            lst.append(count)
    return max(lst)

list=[0,0,0,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1]


print("max consecutive one's is:",maxConsOne(list))
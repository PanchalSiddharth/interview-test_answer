def sumList(ls):
    return sum(ls)

ls=[]    
n = int(input('how many elements: '))
for i in range(n):
    numbers = int(input('Enter elements:'))
    ls.append(numbers)
        
print("sum=",sumList(ls))
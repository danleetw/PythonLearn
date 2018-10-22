

f=open("EmailList.csv","r")
count=0

for buffstr in f.readlines():
    count=count+1
    #print(buffstr)
    a=buffstr.split("-")
    print(a[0],a[1])
    #print(a[0],a[1])

print("Totoal=" ,count)
#bufstr=f.readline()
#print(bufstr)
    
#L.rstrip('\n')去掉换行符

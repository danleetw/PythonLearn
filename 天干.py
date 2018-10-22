a="{'甲子':1,'乙丑':2}"
Seq=eval(a)
#print(Seq)

#m=input("請輸入:")

#print(Seq[m])

a="{"
a1="甲,乙,丙,丁,戊,己,庚,辛,壬,癸"
a2="子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥"
a1l=a1.split(",")
a2l=a2.split(",")
print(a1l)
print(a2l)


dict= {} 
i=0
j=0
for gn in range(0,60):
    i+=1
    j+=1
    if i==11:
        i=1
    if j==13:
        j=1     
    r= a1l[i-1]+a2l[j-1] 
    #print(r)
    dict[r]=gn+1
    
m=input("\n請輸入天干地支:")
print(dict[m])
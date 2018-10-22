import requests
from bs4 import BeautifulSoup
import sqlite3

import tkinter as tk
#from pandas.core import window

#from pip._vendor.distlib.locators import Page


#pyinstaller -F BeautifuSoupFrom.py
#pyinstaller -F Tel_Win.py -i Tel.ico --noconsole


PgTitle="歡迎使用,快取查詢電話簿 v20181018a"
TableName="PhoneList"
HistTableName="PhoneList_Hist"



conn=sqlite3.connect('DanSQLLiteDB.db')
cursor=conn.cursor()
maxno=""

keystr=""
global url

global entry_keyword

    
    
    

#--------------------------------------------
def CreateTable():
#-----Create Table -----
    sqlstr='create table if not exists ' + TableName + ' ("num" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"No" text,"Dep1" text,"Dep2" text,"Location" text,"EmployName" text,"Title" Text,"JobDesc" Text,"ShrtCode" Text,"ExtCode" Text,"Tel" Text)'
    cursor.execute(sqlstr)
    sqlstr='create table if not exists ' + HistTableName + ' ("num" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"Keyword" text,"Resu" text)'
    cursor.execute(sqlstr)
#--------------------------------------------
def HistQuery():
    
    global window
    global sqlstr
    sqlstr="Select distinct keyword,Resu from  "+ HistTableName + " order by num desc" 
    cursor.execute(sqlstr)
    histdata=cursor.fetchall()
    histstr=""
    for sh in range(0,len(histdata)):
        if histstr!="":
            histstr=histstr+" , "
        histstr=histstr+histdata[sh][0]
        if histdata[sh][1]!=None:
            histstr=histstr + "(" + histdata[sh][1] +")"    
            if sh>=19:
                break
    print("最近查詢關鍵字:")
    print("-----------")
    print(histstr)
    recent_keyword.delete('1.0',tk.END)
    recent_keyword.insert("end","最近查詢關鍵字:\n"+histstr)
    window.update()
    print("-----------")
    
    
#--------------------------------------------
def WhereStr():
    wherestr=" where ("
    wherestr=wherestr + " Dep1 like '%"+ keystr + "%'"
    wherestr=wherestr + " or Dep2 like '%" + keystr + "%'"
    wherestr=wherestr + " or Location like '%" + keystr + "%'"
    wherestr=wherestr + " or EmployName like '%" + keystr + "%'"
    wherestr=wherestr + " or ShrtCode like '%" + keystr + "%'"
    wherestr=wherestr + " or ExtCode like '%" + keystr + "%'"
    wherestr=wherestr + ") "
    return(wherestr)


def SearchInDB():
    global maxno,cnt
    
    cnt=0
    #----由舊資料中尋找
    sqlstr="Select * from  "+ TableName
    
     
    sqlstr=sqlstr + WhereStr()
    sqlstr=sqlstr + " order by num desc"
        
    cursor.execute(sqlstr)
    retdata=cursor.fetchall()
    
    
    #print(len(retdata))
    #print("-----資料庫快取結果------")
    lb.insert(0,"-----資料庫快取結果------")
    #print(len(retdata))

    if len(retdata)>0:
        maxno=(retdata[0][0])
        
 
        sqlstr="Select * from  "+ TableName 
        sqlstr=sqlstr + WhereStr()
        sqlstr=sqlstr + " order by Dep1,Dep2,EmployName"
        cursor.execute(sqlstr)
        retdata=cursor.fetchall()
        
        for retlist in retdata:
            
            #print(retlist[1],retlist[2],retlist[3],retlist[4],retlist[5],retlist[6],retlist[7],retlist[8],retlist[9],retlist[10])
            r=retlist[1] + retlist[2] + retlist[3] +retlist[4]+retlist[5]+retlist[6]+retlist[7]+retlist[8]+retlist[9]+retlist[10]
            
            #print("--")
            lb.insert(lb.size(),r)
            print("LB Size" ,lb.size())
            cnt=cnt+1
            ResuStr=retlist[7] +" "+ retlist[8]    
    else:
        print("--無資料--")
        lb.insert(lb.size()-1,"--無資料--")
        maxno=""
    #print("DB Maxno=",maxno)
    return(maxno)
#--------------------------------------------
def WebQuery():
    global maxno
    global cnt
    
    cnt=0
    print("-----總務部網站查詢結果------")
    
    lb1.insert(0,"-----總務部網站查詢結果------")
        
    #connectok=True
    
    for page in range(1,11):
        url1=url+str(page)
        #print("Connect Status:", connectok)
        #print(url1)
        #html=requests.get(url1)
        try:
            html=requests.get(url1)
        except:
            print("無法連線網路電話簿!")
            conn.commit()
            connectok=False
            break
        #print("連線正常")
        connectok=True
        #    print("TEST")
        html.encoding='utf8'
        #print(html.text)
        #quit()

        sp=BeautifulSoup(html.text,"html.parser")
        #print(sp)
        #input("wait")

        v=sp.find("table")

        #print(v)
        #quit()

        #v1=v.find_all("tr",class_="column_name")
        v1=v.find_all("tr")


        if len(v1)==1:
            break
        
        #print(v1)
    
        for a in range(1,len(v1)):
            #print(a)
            #print(v1[a])
            
            v2=v1[a].find_all("td")
            #for b in range(0,len(v2)):
            #print(b)
            #print(v2[b].text)
            #print(v2)
            #print(len(v2))
            if len(v2)>2:
                sqlstr="insert into " + TableName + " (No,Dep1,Dep2,Location,EmployName,Title,JobDesc,ShrtCode,ExtCode,Tel) values('"+v2[0].text+"','" +v2[1].text+ "','" + v2[2].text+ "','"+ v2[3].text +"','"+ v2[4].text +"','"+ v2[5].text +"','"+ v2[6].text +"','"+ v2[7].text +"','"+ v2[8].text +"','"+ v2[9].text +"')"
                r=v2[1].text+ "','" + v2[2].text+ "','"+ v2[3].text +"','"+ v2[4].text +"','"+ v2[5].text +"','"+ v2[6].text +"','"+ v2[7].text +"','"+ v2[8].text +"','"+ v2[9].text
                
                lb1.insert(lb1.size(),r)
                
                #print(v2[1].text+ "','" + v2[2].text+ "','"+ v2[3].text +"','"+ v2[4].text +"','"+ v2[5].text +"','"+ v2[6].text +"','"+ v2[7].text +"','"+ v2[8].text +"','"+ v2[9].text)
                #print(sqlstr)
                ResuStr=v2[7].text +" "+ v2[8].text
                print(ResuStr)
                cursor.execute(sqlstr)
                #conn.commit()
                cnt=cnt+1
            else:
                break

                #maxno
        #print("maxno=",maxno,"Cnt=",cnt)
    #print("MaxNo=",maxno,"Cnt=",cnt)
    #quit()        
    if maxno!="" and cnt>0:
        sqlstr="delete from " + TableName
        sqlstr=sqlstr +  WhereStr() 
        sqlstr=sqlstr + " And  num<=" + str(maxno)
        #print(sqlstr)
        cursor.execute(sqlstr)
        #conn.commit()
        
    if cnt>0:
        print("網站查詢到:", cnt , "筆資料.")
    else:
        print("查無資料!")
        
        
    #只查到一筆表示精準命中，更新查詢關鍵字的分機    
    if cnt==1:    
        sqlstr="update " + HistTableName + " set Resu='" + ResuStr + "'"
        sqlstr=sqlstr + "  where Keyword='" + keystr + "'" 
        cursor.execute(sqlstr)
        
          
    conn.commit()
    return(cnt)
    #conn.close()




def Query():

    
    global keystr,window,entry_keyword
    keystr=""
    #keystr=input("受限電話簿一次只能查100筆資料\n若查詢結果太多,請縮小搜索範圍\n請輸入查詢關鍵字(部門/地址/姓名/分機):")
    
    
    keystr=entry_keyword.get()
    if keystr=="":
        return
    
    global url
    url="http://ga.ccc.com.tw/tel/search.asp?key="+keystr+"&Page="

    print("搜詢:",keystr)
    lb.delete(0,lb.size())
    lb1.delete(0,lb1.size())
    
    lb.insert(0,"-----本機資料查詢中---")
    lb1.insert(0,"-----網頁端資料查詢中---")
    window.update()
    
    
    #lb.insert(0,keystr)
    #----寫入最近查詢紀錄
    sqlstr2="insert into " + HistTableName + " (KeyWord) values('"+keystr+"')"
    cursor.execute(sqlstr2)

    sqlstr=""
    
    #------開始顯示
    lb.delete(0,lb.size())
    maxno=SearchInDB()
    window.update()
    
    global cnt
    
    lb1.delete(0,lb1.size())
    cnt=WebQuery()
    HistQuery()
    
    entry_keyword.delete(0,'end')
    window.update()
    
    #print("-------------------")
   

    
def EnterHit(event):
    Query()
    #print("TEST",event)

def MainWindow():
    global window
    
    window=tk.Tk()
    window.title(PgTitle)
    window.geometry("980x680")
    
    global recent_keyword
    recent_keyword=tk.Text(window,width=90,height=5)
    recent_keyword.pack()
    
    
    tk.Label(window,
             text='查詢關鍵字',
             bg='#ffaabb',
             width=15,
             height=2
             ).pack()
    
    global entry_keyword
    entry_keyword=tk.Entry(window,width=20,font='48')
    entry_keyword.pack()
    
    

    tk.Button(window,
              text='查詢',
              width=10,
              height=2,
              command=Query).pack()
    
    tk.Label(window,
             text='本機快取查詢',
             width=15,
             height=1
             ).pack()
    
    global lb
    lb=tk.Listbox(window,width=100)
    lb.pack()

    tk.Label(window,
             text='網站查詢結果',
             width=15,
             height=1
             ).pack()
    
    global lb1
    lb1=tk.Listbox(window,width=100)
    lb1.pack()
    
    HistQuery()
    
    window.bind('<Return>',EnterHit)
    
    entry_keyword.focus()
    window.mainloop()                       
    
    
    
#----------Main Program -----
CreateTable()
MainWindow()

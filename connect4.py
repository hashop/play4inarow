import tkinter as tk
        
root = tk.Tk()

c = tk.Canvas(root, height=1000, width=1000, bg='white')
c.pack()
rect = []
curr = []
circ = []
currstate = [[0 for i in range(6)] for j in range(7)]
currcoins = 0
col = {1:'red', 2:'yellow'}
oppdir = {1:0, 2:5, 3:7, 4:6}
currcol = 1

def validateCoords(x, y):
    return ((x>=0) and (x<7) and (y>=0) and (y<6))
        
def validateState(tag):
    chk4 = [0 for i in range(8)]
    for i in range(3):
        for j in range(3):
            if(i!=0 or j!=0):
                xadd=i%2-i//2
                yadd=j%2-j//2
                x1=tag+xadd
                y1=curr[tag]+yadd
                while(validateCoords(x1,y1) and currstate[x1][y1]==currcol):
                    chk4[3*i+j-1]+=1
                    x1+=xadd
                    y1+=yadd
    for i in range(1,5):
        if((chk4[i]+chk4[oppdir[i]])>=3):
            return currcol
    if(currcoins==42):
        return 0
    else:
        return -1    

def unbindAll():
    for i in circ:
        for j in i:
            c.tag_unbind(j,'<Enter>')
            c.tag_unbind(j,'<Leave>')
            c.tag_unbind(j,'<1>')
    for i in rect:
        c.tag_unbind(i,'<Enter>')
        c.tag_unbind(i,'<Leave>')
        c.tag_unbind(i,'<1>')

def onCircleEnter(event,tag):                
    #print('Got object click', event.x, event.y)
    if(curr[tag]<6):
        c.itemconfig(circ[tag][curr[tag]], outline=col[currcol])
    
def onCircleLeave(event,tag):                
    #print('Got object click', event.x, event.y)
    if(curr[tag]<6):
        c.itemconfig(circ[tag][curr[tag]], outline='blue')
    
def onCircleClick(event,tag):                
    #print('Got object click', event.x, event.y)
    if(curr[tag]<6):
        global currcol, currcoins
        c.itemconfig(circ[tag][curr[tag]], fill=col[currcol])
        currcoins+=1
        ret = validateState(tag)
        currstate[tag][curr[tag]]=currcol
        currcol=3-currcol
        if(ret==-1):
            #print("Player %d's turn"%currcol)
            c.itemconfig(txt, text="Player %d's turn"%currcol)
        elif(ret==0):
            #print("It's a draw!")
            c.itemconfig(txt, text="  It's a draw!")
            unbindAll()
            root.after(2000,root.destroy)
            return
        else:
            #print("Player %d wins!"%ret)
            c.itemconfig(txt, text="Player %d wins!"%ret)
            unbindAll()
            root.after(2000,root.destroy)
            return
        curr[tag]+=1
        if(curr[tag]<6):
            onCircleEnter(event,tag)
    
for i in range(7):
    curr.append(0)
    rect.append(c.create_rectangle(150+100*i, 100, 250+100*i, 700, fill="blue", width=0)) 
    circ.append([])
    for j in range(6):
        circ[i].append(c.create_oval(160+100*i, 610-100*j, 240+100*i, 690-100*j, fill="white", outline="blue", width=8))
        c.tag_bind(circ[i][j], '<Enter>', lambda event, tag=i: onCircleEnter(event, tag))
        c.tag_bind(circ[i][j], '<Leave>', lambda event, tag=i: onCircleLeave(event, tag))
        c.tag_bind(circ[i][j], '<1>', lambda event, tag=i: onCircleClick(event, tag))
    c.tag_bind(rect[i], '<Enter>', lambda event, tag=i: onCircleEnter(event, tag))
    c.tag_bind(rect[i], '<Leave>', lambda event, tag=i: onCircleLeave(event, tag))
    c.tag_bind(rect[i], '<1>', lambda event, tag=i: onCircleClick(event, tag))
txt = c.create_text(350, 800, text="Player 1's turn", font=('Purisa',40), anchor="sw")


root.mainloop()
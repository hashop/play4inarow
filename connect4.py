import tkinter as tk
import copy
import random
        
root = tk.Tk()

INF = 10000000000000
DEPTH = 5

c = tk.Canvas(root, height=1000, width=1200, bg='white')
c.pack()
rect = []
curr = []
circ = []
currstate = [[0 for i in range(6)] for j in range(7)]
currcoins = 0
col = {1:'red', 2:'yellow'}
oppdir = {1:0, 2:5, 3:7, 4:6}
numscores = {0:0, 1:1, 2:2, 3:15, 4:10000000000}
togColor = {0:'gray90', 1:'black'}
togText = {0:'Show Negamax\n      Scores', 1:' Hide Negamax\n      Scores'}
togval = 0
currcol = 1
cheur = 0

def eval4(block):
    cnt = [0,0,0]
    for i in block:
        cnt[i]+=1
    if(cnt[1]*cnt[2]>0):
        return 0
    ret = numscores[cnt[1]+cnt[2]]
    if(cnt[2]>0):
        ret*=-1
    return ret
    
def validateCoords(x, y):
    return ((x>=0) and (x<7) and (y>=0) and (y<6))

def heuristic(state, tag, curr, currcoins, ccol, currheur):
    ret = currheur
    start = max(0,curr[tag]-3)
    end = min(5,curr[tag]+3)
    block = []
    for i in range(4):
        block.append(state[tag][start+i])
    ret-=eval4(block)
    block.remove(0)
    block.append(ccol)
    ret+=eval4(block)
    block.remove(ccol)
    block.append(0)
    for i in range(end-start-3):
        block.remove(state[tag][start+i])
        block.append(state[tag][start+4+i])
        ret-=eval4(block)
        block.remove(0)
        block.append(ccol)
        ret+=eval4(block)
        block.remove(ccol)
        block.append(0)
        
    start = max(0,tag-3)
    end = min(6,tag+3)
    block = []
    for i in range(4):
        block.append(state[start+i][curr[tag]])
    ret-=eval4(block)
    block.remove(0)
    block.append(ccol)
    ret+=eval4(block)
    block.remove(ccol)
    block.append(0)
    for i in range(end-start-3):
        block.remove(state[start+i][curr[tag]])
        block.append(state[start+4+i][curr[tag]])
        ret-=eval4(block)
        block.remove(0)
        block.append(ccol)
        ret+=eval4(block)
        block.remove(ccol)
        block.append(0)
        
    if((tag+curr[tag]) in range(3,9)):
        start = 0
        while(validateCoords(tag-start-1,curr[tag]+start+1) and start<3):
            start+=1
        end = 0
        while(validateCoords(tag+end+1,curr[tag]-end-1) and end<3):
            end+=1
        block = []
        for i in range(4):
            block.append(state[tag-start+i][curr[tag]+start-i])
        ret-=eval4(block)
        block.remove(0)
        block.append(ccol)
        ret+=eval4(block)
        block.remove(ccol)
        block.append(0)
        for i in range(end+start-3):
            block.remove(state[tag-start+i][curr[tag]+start-i])
            block.append(state[tag-start+4+i][curr[tag]+start-4-i])
            ret-=eval4(block)
            block.remove(0)
            block.append(ccol)
            ret+=eval4(block)
            block.remove(ccol)
            block.append(0)
        
    if((tag-curr[tag]) in range(-2,4)):
        start = 0
        while(validateCoords(tag-start-1,curr[tag]-start-1) and start<3):
            start+=1
        end = 0
        while(validateCoords(tag+end+1,curr[tag]+end+1) and end<3):
            end+=1
        block = []
        for i in range(4):
            block.append(state[tag-start+i][curr[tag]-start+i])
        ret-=eval4(block)
        block.remove(0)
        block.append(ccol)
        ret+=eval4(block)
        block.remove(ccol)
        block.append(0)
        for i in range(end+start-3):
            block.remove(state[tag-start+i][curr[tag]-start+i])
            block.append(state[tag-start+4+i][curr[tag]-start+4+i])
            ret-=eval4(block)
            block.remove(0)
            block.append(ccol)
            ret+=eval4(block)
            block.remove(ccol)
            block.append(0)
            
    return ret
        
def validateState(state, tag, curr, currcoins, ccol):
    chk4 = [0 for i in range(8)]
    for i in range(3):
        for j in range(3):
            if(i!=0 or j!=0):
                xadd=i%2-i//2
                yadd=j%2-j//2
                x1=tag+xadd
                y1=curr[tag]+yadd
                while(validateCoords(x1,y1) and state[x1][y1]==ccol):
                    chk4[3*i+j-1]+=1
                    x1+=xadd
                    y1+=yadd
    for i in range(1,5):
        if((chk4[i]+chk4[oppdir[i]])>=3):
            return ccol
    if(currcoins==42):
        return 0
    else:
        return -1 
        
def negamax(state, tag, curr, ccoins, ccol, currheur, depth, alpha, beta):
    newcheur = heuristic(state, tag, curr, ccoins, ccol, currheur)
    if(depth==0 or abs(newcheur)>1000000000 or ccoins==41):
        if(ccol==2):
            newcheur*=-1
        return newcheur
    state[tag][curr[tag]]=ccol
    curr[tag]+=1
    for i in range(7):
        if(curr[i]<6):
            ret = -negamax(copy.deepcopy(state), i, curr[:], ccoins+1, 3-ccol, newcheur, depth-1, -beta, -alpha)
            beta = min(beta,ret)
            if(alpha>beta):
                break
    return beta    

def updatescoreTxt(score):
    for i in range(7):
        if(score[i]!=-INF):
            c.itemconfig(scoreTxt[i], text="%d"%score[i])
        else:
            c.itemconfig(scoreTxt[i], text="Full")

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
    if(curr[tag]<6):
        c.itemconfig(circ[tag][curr[tag]], outline=col[currcol])
    
def onCircleLeave(event,tag):                
    if(curr[tag]<6):
        c.itemconfig(circ[tag][curr[tag]], outline='blue')
    
def onCircleClick(event,tag):                
    if(curr[tag]<6):
        onCircleLeave(event,tag)
        global currcol, currcoins, cheur
        c.itemconfig(circ[tag][curr[tag]], fill=col[currcol])
        cheur = heuristic(currstate,tag,curr,currcoins,currcol,cheur)
        currcoins+=1
        ret = validateState(currstate, tag, curr, currcoins, currcol)
        currstate[tag][curr[tag]]=currcol
        currcol=3-currcol
        curr[tag]+=1
        nextlist = []
        for i in range(7):
            if(curr[i]<6):
                nextlist.append(negamax(copy.deepcopy(currstate),i,curr[:],currcoins,currcol,cheur,DEPTH-1,-INF,INF))
            else:
                nextlist.append(-INF)
        updatescoreTxt(nextlist)
        if(ret==-1):
            if(currcol==1):
                c.itemconfig(txt, text="   Your turn")
            else:
                c.itemconfig(txt, text="   Thinking...")
                root.update()
        elif(ret==0):
            c.itemconfig(txt, text="  It's a draw!")
            unbindAll()
            root.after(2000,root.destroy)
            return
        else:
            if(ret==1):
                c.itemconfig(txt, text="    You win!")
            else:
                c.itemconfig(txt, text="    AI wins!")
            unbindAll()
            root.after(2000,root.destroy)
            return
        if(curr[tag]<6 and currcol==2):
            onCircleEnter(event,tag)
        if(currcol==2):
            m = max(nextlist)
            maxlist = [i for i, j in enumerate(nextlist) if j == m]
            random.shuffle(maxlist)
            onCircleClick(event,maxlist[0])
            onCircleEnter(event,tag)
            
def ToggleClick(event):
    global togval
    for i in scoreTxt:
        c.itemconfig(i, fill=togColor[togval])
    c.itemconfig(hidetxt, text=togText[togval])
    togval = 1-togval
    
for i in range(7):
    curr.append(0)
    rect.append(c.create_rectangle(150+100*i, 100, 250+100*i, 700, fill="blue", width=0)) 
    c.create_rectangle(165+100*i, 60, 245+100*i, 85, fill="gray90", width=1)
    circ.append([])
    for j in range(6):
        circ[i].append(c.create_oval(160+100*i, 610-100*j, 240+100*i, 690-100*j, fill="white", outline="blue", width=8))
        c.tag_bind(circ[i][j], '<Enter>', lambda event, tag=i: onCircleEnter(event, tag))
        c.tag_bind(circ[i][j], '<Leave>', lambda event, tag=i: onCircleLeave(event, tag))
        c.tag_bind(circ[i][j], '<1>', lambda event, tag=i: onCircleClick(event, tag))
    c.tag_bind(rect[i], '<Enter>', lambda event, tag=i: onCircleEnter(event, tag))
    c.tag_bind(rect[i], '<Leave>', lambda event, tag=i: onCircleLeave(event, tag))
    c.tag_bind(rect[i], '<1>', lambda event, tag=i: onCircleClick(event, tag))
txt = c.create_text(350, 800, text="   Your turn", font=('Purisa',40), anchor="sw")

hiderect = c.create_rectangle(895, 55, 1080, 110, fill="gray90", width=1)
hidetxt = c.create_text(918, 107, text=' Hide Negamax\n      Scores', font=('Purisa',15), anchor="sw")
scoreTxt = [(c.create_text(170+100*i, 80, text="0", anchor="sw")) for i in range(7)]
c.tag_bind(hiderect, '<1>', ToggleClick)
c.tag_bind(hidetxt, '<1>', ToggleClick)

root.mainloop()
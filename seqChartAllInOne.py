###
MESSAGE='MSG'
STATE='STA'
COMMENT='#'

import array
class Canvas:
    BLANK=' '
    HLINE='-'
    VLINE='|'
    HLARROW='<'
    HRARROW='>'
    VUARROW='^'
    VDARROW='v'
    INTERSECT='+'
    XINTERSECT='*'
    WAVEVLLINE='('
    WAVEVRLINE=')'
    WAVEHLINE='~'
    
    def __init__(self,col,row):
        self.row=row
        self.column=col
        self.canvas=array.array('b',[ord(self.BLANK)]*(row*col))
    
    def __draw(self,col,row,char):        
        self.canvas[self.column*row+col]=ord(char)
    
    def reset(self):
        for i in range(self.column*self.row):
            self.canvas[i]=self.BLANK
           
    def output(self):
        for i in range(self.row):  
            lineStart=self.column*i  
            line=self.canvas[lineStart:lineStart+self.column].tostring().decode('utf-8')    
            line = line.rstrip()   
            if len(line) > 0:   
                print (line)
        
    def point(self,col,row,char):
        self.__draw(col,row,char)
        
    def hline(self,col,row,length,direction=None,arrow=None,hChar=HLINE):
        start=col
        stop=col+length
        if direction:
            start=col-length+1
            stop=col+1
                    
        for i in range(start,stop):
            self.point(i,row,hChar)
            
        if arrow:
            if direction:
                self.point(start,row,self.HLARROW)
            else:
                self.point(stop-1,row,self.HRARROW)
            
            
    def vline(self,col,row,length,direction=None,arrow=None,vChar=VLINE):
        start=row
        stop=row+length
        if direction:
            start=row-length+1
            stop=row+1
        for i in range(start,stop):
            self.point(col,i,vChar)
        
        if arrow:
            if direction:
                self.point(col,start,Canvas.VUARROW)
            else:
                self.point(col,stop-1,Canvas.VDARROW)
                
    def rect(self,col,row,width,height):                    
        self.vline(col,row,height)
        self.vline(col+width-1,row,height)
        self.hline(col+1,row+height-1,width-2)   
        self.hline(col+1,row,width-2)
    
    def waveRect(self,col,row,width,height):        
        self.vline(col,row,height,vChar=self.WAVEVLLINE)
        self.vline(col+width-1,row,height,vChar=self.WAVEVRLINE)
        self.hline(col+1,row+height-1,width-2,hChar=self.WAVEHLINE) 
        self.hline(col+1,row,width-2,hChar=self.WAVEHLINE)
    
    def text(self,col,row,astr,center=None):
        left=col
        if center:
            left=col-len(astr)//2
        for i in range(len(astr)):
            self.point(left+i,row,astr[i])
        
    def __textRect(self,str,width=None):
        strlen=len(str)
        if not width :
            cols=strlen
            rows=1
        elif strlen<=width:
            cols=width
            rows=1
        else:
            cols=width
            rows=strlen//width
            remain=strlen % width
            if remain:
                rows +=1
        return (cols,rows)
        
    def rectText(self,col,row,astr,width=None,center=None):
        cols,rows=self.__textRect(astr,width)                
        for i in range(rows):
            line=astr[cols*i:cols*i+cols]
            if center:
                self.text(col,row+1+i,line,center)
                
                left=col-cols//2-1
                top=row
                width=cols+2
                height=rows+2
                self.rect(left,top,width,height)
            else:
                self.text(col+1,row+1+i,line,center)
                
                left=col
                top=row
                width=cols+2
                height=rows+2
                self.rect(left,top,width,height)
        return (width,height)
        
    def waveRectText(self,col,row,astr,width=None,center=None):
        cols,rows=self.__textRect(astr,width)                
        for i in range(rows):
            line=astr[cols*i:cols*i+cols]
            if center:
                self.text(col,row+1+i,line,center)
                
                left=col-cols//2-1
                top=row
                width=cols+2
                height=rows+2
                self.waveRect(left,top,width,height)
            else:
                self.text(col+1,row+1+i,line,center)
                
                left=col
                top=row
                width=cols+2
                height=rows+2
                self.waveRect(left,top,width,height)   
        return (width,height)

    def ordAt(self,col,row):
        return self.canvas[self.column*row+col]

    def isRowBlank(self,row):
        for c in range(self.column):
            if self.ordAt(c,row)!=ord(self.BLANK):
                return False 
        return True 

    def isColumnBlank(self,column):
        for r in range(self.row):
            if self.ordAt(column,r)!=ord(self.BLANK):
                return False
        return True         

    def shiftLeft(self,fromColumn, numOfColumn=1):
        for r in range(self.row):
            for c in range(fromColumn,self.column):
                self.point(c - numOfColumn, r, chr(self.ordAt(c,r)))
    def shiftTop(self,fromRow, numOfRow=1):
        for c in range(self.column):
            for r in range(fromRow,self.row):
                self.point(c, r-numOfRow, chr(self.ordAt(c,r)))

    def trimLeftTop(self):
         while self.isColumnBlank(0):
            self.shiftLeft(1)

         while self.isRowBlank(0):
            self.shiftTop(1)

from canvas import *
from constants import *  

class ChartMatrixCanvas(Canvas):
    SPAN=4
    MARGIN=1
    ROWSPAN=2    
    BORDER=1
    
    def __init__(self,process,msgMatrix,alias, aliasList):
        self.process=process
        self.msgMatrix=msgMatrix
        self.alias=alias
        self.aliasList = aliasList 
        self.states=[]        
        self.messages=[]
        self.processInfo={}
        
        for msgLst in self.msgMatrix:
            for msgType,contents in msgLst:
                if msgType==MESSAGE:
                    if contents[2] not in self.messages:
                        self.messages.append(contents[2])
                elif msgType==STATE:
                    if contents[1] not in self.states:
                        self.states.append(contents[1])
                else:
                    raise 'type not supported'
            
        cols,rows=self.initCanvas()
        Canvas.__init__(self,cols,rows)
    
    def initCanvas(self):
        processCount=len(self.process)
        maxTextLen=max([len(l) for l in (self.states+self.messages)])
        self.interval=self.SPAN+maxTextLen
        #self.currow=self.MARGIN

        

        for i in range(len(self.process)):
            p=self.process[i]
            col=self.MARGIN+self.interval*(i+1)
            row=self.MARGIN + self.MARGIN + len(self.alias) 
            currow=row
            #print(" init currow=%d process=%s" % (currow, p) )
            self.processInfo[p]=(col,row,currow)
            #self.processInfo[p]=(col,row)
        
        cols=col+self.interval+self.MARGIN
        rows=(len(self.msgMatrix)+2)*self.ROWSPAN+4*self.MARGIN+len(self.alias)+2*self.BORDER
        return (cols,rows)
    
    def draw(self):
        self.drawHeader()
        self.drawMatrix()
    
    def drawMsgMatrix(self,column, fp,tp,msg):
        fcol,frow,fcurrow=self.processInfo[fp]
        tcol,trow,tcurrow=self.processInfo[tp]
        top=max(fcurrow,tcurrow)
        #print("fcurrow=%d tcurrrow=%d fp=%s tp=%s top=%d msg=%s column=%d" % (fcurrow,tcurrow,fp,tp,top,msg,column))
        left=min(fcol,tcol)
        right=max(fcol,tcol)
        if(fcol<tcol):
            self.hline(left,top,right-left+1,arrow=True)
        else:
            self.hline(right,top,right-left+1,direction=True,arrow=True)        
        
        textLeft=left+((right-left+1)-len(msg))//2
        self.text(textLeft,top,msg)

        if column==0:
            fcurrow=tcurrow=top+self.ROWSPAN
            self.processInfo[fp]=fcol,frow,fcurrow
            self.processInfo[tp]=tcol,trow,tcurrow
            
            for p in self.process:
                col,row,currow=self.processInfo[p]
                if currow<fcurrow:
                    currow=fcurrow
                self.processInfo[p]=(col,row,currow)
        
    def drawStateMatrix(self,column, p,s):        
        col,row,currow=self.processInfo[p]
        width,height=self.waveRectText(col,currow,s,center=True)
        if column == 0:
            currow+=self.ROWSPAN + self.BORDER * 2 
            self.processInfo[p]=(col,row,currow)
            for p in self.process:
                col,row,currow1=self.processInfo[p]
                if currow1<currow:
                    currow1=currow
                self.processInfo[p]=(col,row,currow1)
        

    
    def drawMatrix(self):
        for msgLst in self.msgMatrix:
            column = len(msgLst)
            for msgType,contents in msgLst:
                column -= 1
                if msgType==MESSAGE:
                    fromProcess=contents[0]
                    toProcess=contents[1]
                    message=contents[2]
                    self.drawMsgMatrix(column,fromProcess,toProcess,message)                
                elif msgType==STATE:
                    process=contents[0]
                    state=contents[1]
                    self.drawStateMatrix(column,process,state)
                else:
                    raise 'msgType not supported'
                
    def drawHeader(self):        
                
        col,row,currow = self.processInfo[self.process[0]]
        row = self.MARGIN
        for longName in self.aliasList:
            shortName = self.alias[longName]
            self.text(col,row,"%s = %s" % (shortName,longName))
            row += 1
        for p in self.process:
            col,row,currow=self.processInfo[p]
            #col,row=self.processInfo[p]
            width,height=self.rectText(col,currow,p,center=True)
            bottom=row+height    
            currow+=self.ROWSPAN + 2*self.MARGIN       
            #print("header currow=%d process=%s" % (currow, p) )
            self.processInfo[p]=(col,row,currow)
            #self.processInfo[p]=(col,row)            
            self.vline(col,bottom,self.row-self.MARGIN-bottom,arrow=True)
        #self.currow+=self.ROWSPAN    
 
 
import fileinput
from canvas import *
from constants import *  
from chartMatrixCanvas import * 

#third party import 

gProcesses=[]
gMsgSequence=[]
gCmdMatrix = []
gMsgMatrix = []
gAliasList=[]
gAlias={}

def snd_matrix(column, process,toProcess,message):
    global gProcesses
    global gMsgMatrix
    process=getAbbr(process)
    toProcess=getAbbr(toProcess)
    message=getAbbr(message)
    if process not in gProcesses:
        gProcesses.append(process)
    if toProcess not in gProcesses:
        gProcesses.append(toProcess)
    if column == 0:    
        gMsgMatrix.append([(MESSAGE,(process,toProcess,message))])
    else:
       gMsgMatrix[len(gMsgMatrix)-1].append((MESSAGE,(process,toProcess,message)))
    
def rcv_matrix(column, process,fromProcess,message):
    snd_matrix(column, fromProcess,process,message)
    
def state_matrix(column, process,astate):
    global gProcesses
    process=getAbbr(process)
    astate=getAbbr(astate)    
    if process not in gProcesses:
        gProcesses.append(process)

    if column == 0:  
        gMsgMatrix.append([(STATE,(process,astate))])  
    else:
        gMsgMatrix[len(gMsgMatrix)-1].append((STATE,(process,astate)))




def proc(*processes):
    global gProcesses
    for process in processes:
        process=getAbbr(process)
        if process not in gProcesses:
            gProcesses.append(process)

def alias(shortName, longName):
    global gAlias
    gAlias[longName]=shortName
    if longName not in gAliasList:
        gAliasList.append(longName)
    pass

def getAbbr(longName, dictionary=gAlias):
    if longName in dictionary:
        return dictionary[longName]
    return longName 

def parseLine(line):
    line=line.strip()
    if len(line)==0: 
        return True
    if line.startswith(COMMENT):
        return True
    columns=line.split('|')
    gCmdMatrix.append(columns)

    pass




def parseMatrixCmd(*commands):
    column = 0
    for cmd in commands:        
        cmd=cmd.strip()
        if len(cmd)==0: 
            continue
        if cmd.startswith(COMMENT):
            continue
        cmds=cmd.split()
    
        theFunction=cmds[0].lower()
        theArgs=cmds[1:]
        if theFunction=='snd':
            snd_matrix(column, *theArgs)
        elif theFunction=='rcv':
            rcv_matrix(column, *theArgs)
        elif theFunction=='state':
            state_matrix(column, *theArgs)
        elif theFunction=='proc':  
            proc(*theArgs)  
        elif theFunction=='alias':     
            alias(*theArgs)    
        else:        
            raise 'cmd wrong'
            return False
        column += 1 
    return True




def main():
    global gProcesses
    global gMsgSequence
    global gCmdMatrix
    global gMsgMatrix
    global gAliasList
    for line in fileinput.input():
        parseLine(line)
    #print(gCmdMatrix)    
    for row in gCmdMatrix  :        
            parseMatrixCmd(*row)
    #print(gMsgMatrix)        
    canvas=ChartMatrixCanvas(gProcesses, gMsgMatrix,gAlias,gAliasList)
    #for line in fileinput.input():
    #    parseCmd(line)
    #canvas=ChartCanvas(gProcesses,gMsgSequence)
    canvas.draw()
    canvas.trimLeftTop()
    canvas.output()
    
                     
if '__main__'==__name__:
    main()
    pass


    
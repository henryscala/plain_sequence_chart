from canvas import *
from constants import *  

class ChartMatrixCanvas(Canvas):
    SPAN=4
    MARGIN=1
    ROWSPAN=2    
    BORDER=1
    
    def __init__(self,process,msgMatrix,alias):
        self.process=process
        self.msgMatrix=msgMatrix
        self.alias=alias
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
        
        row = self.MARGIN
        col = self.SPAN
        for longName, shortName in self.alias.items():
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
 
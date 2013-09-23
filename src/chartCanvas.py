from canvas import *
from constants import *  

class ChartCanvas(Canvas):
    BORDER=1
    MARGIN=1
    PADDING=1   
    
    def __init__(self,commandList):
        self.commandList=commandList
        self.labels={}
        self.notes=[]        
        self.messages=[]
        self.instances=[]                
        processCommandList(self.commandList)    
        cols,rows=self.initCanvas()
        Canvas.__init__(self,cols,rows)
    
    def processCommandList(cmdList):
        pass    

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
            self.processInfo[p]=(col,row,currow)
            #self.processInfo[p]=(col,row)
        
        cols=col+self.interval+self.MARGIN
        rows=(len(self.sequence)+1)*self.ROWSPAN+2*self.MARGIN+len(self.alias)
        return (cols,rows)
    
    def draw(self):
        self.drawHeader()
        self.drawSequence()
    
    def drawMsg(self,fp,tp,msg):
        fcol,frow,fcurrow=self.processInfo[fp]
        tcol,trow,tcurrow=self.processInfo[tp]
        top=max(fcurrow,tcurrow)
        left=min(fcol,tcol)
        right=max(fcol,tcol)
        if(fcol<tcol):
            self.hline(left,top,right-left+1,arrow=True)
        else:
            self.hline(right,top,right-left+1,direction=True,arrow=True)        
        
        textLeft=left+((right-left+1)-len(msg))//2
        self.text(textLeft,top,msg)
        fcurrow=tcurrow=top+self.ROWSPAN
        self.processInfo[fp]=fcol,frow,fcurrow
        self.processInfo[tp]=tcol,trow,tcurrow
        
        for p in self.process:
            col,row,currow=self.processInfo[p]
            if currow<fcurrow:
                currow=fcurrow
            self.processInfo[p]=(col,row,currow)
        
    def drawState(self,p,s):
        col,row,currow=self.processInfo[p]
        width,height=self.waveRectText(col,currow,s,center=True)
        currow+=self.ROWSPAN
        self.processInfo[p]=(col,row,currow)
    
    def drawSequence(self):
        for type,contents in self.sequence:
            if type==MESSAGE:
                fromProcess=contents[0]
                toProcess=contents[1]
                message=contents[2]
                self.drawMsg(fromProcess,toProcess,message)                
            elif type==STATE:
                process=contents[0]
                state=contents[1]
                self.drawState(process,state)
            else:
                raise 'type not supported'
    
    def drawHeader(self):        
        
        row = self.MARGIN
        col = self.SPAN
        for longName, shortName in self.alias.items():
            self.text(col,row,"%s = %s" % (shortName,longName))
            row += 1
            pass
        for p in self.process:
            col,row,currow=self.processInfo[p]
            #col,row=self.processInfo[p]
            width,height=self.rectText(col,currow,p,center=True)
            bottom=row+height    
            currow+=self.ROWSPAN        
            self.processInfo[p]=(col,row,currow)
            #self.processInfo[p]=(col,row)            
            self.vline(col,bottom,self.row-self.MARGIN-bottom,arrow=True)
        #self.currow+=self.ROWSPAN    
 
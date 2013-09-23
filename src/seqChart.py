#
#designed by henry 
#
import fileinput
import array

gProcesses=[]
gMsgSequence=[]
gAlias={}
MESSAGE='MSG'
STATE='STA'
COMMENT='#'



def snd(process,toProcess,message):
    global gProcesses
    global gMsgSequence
    process=getAbbr(process)
    toProcess=getAbbr(toProcess)
    message=getAbbr(message)
    if process not in gProcesses:
        gProcesses.append(process)
    if toProcess not in gProcesses:
        gProcesses.append(toProcess)
    gMsgSequence.append((MESSAGE,(process,toProcess,message)))
    
def rcv(process,fromProcess,message):
    snd(fromProcess,process,message)
    
def state(process,astate):
    global gProcesses
    process=getAbbr(process)
    astate=getAbbr(astate)
    if process not in gProcesses:
        gProcesses.append(process)
    gMsgSequence.append((STATE,(process,astate)))

def proc(*processes):
    global gProcesses
    for process in processes:
        process=getAbbr(process)
        if process not in gProcesses:
            gProcesses.append(process)

def alias(shortName, longName):
    global gAlias
    gAlias[longName]=shortName
    pass
    
def lst():
    print ('processes:')
    print (gProcesses)
    print ()   
    print ('chart:')
    for type,content in gMsgSequence:
        print ( type,content )    

def parseCmd(cmd):
    cmd=cmd.strip()
    if len(cmd)==0: 
        return True
    if cmd.startswith(COMMENT):
        return True
    cmds=cmd.split()
    
    theFunction=cmds[0].lower()
    theArgs=cmds[1:]
    if theFunction=='snd':
        snd(*theArgs)
    elif theFunction=='rcv':
        rcv(*theArgs)
    elif theFunction=='state':
        state(*theArgs)
    elif theFunction=='lst':
        lst(*theArgs)
    elif theFunction=='proc':  
        proc(*theArgs)  
    elif theFunction=='alias':     
        alias(*theArgs)
    else:        
        raise 'cmd wrong'
        return False
    return True

def getAbbr(longName, dictionary=gAlias):
    if longName in dictionary:
        return dictionary[longName]
    return longName


def main():
    global gProcesses
    global gMsgSequence
    for line in fileinput.input():
        parseCmd(line)
    canvas=ChartCanvas(gProcesses,gMsgSequence,gAlias)
    canvas.draw()
    canvas.output()
    
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
    
class ChartCanvas(Canvas):
    SPAN=4
    MARGIN=1
    ROWSPAN=3    
    
    def __init__(self,process,sequence, alias):
        self.process=process
        self.sequence=sequence
        self.alias=alias
        self.states=[]        
        self.messages=[]
        self.processInfo={}
        
        for type,contents in self.sequence:
            if type==MESSAGE:
                if contents[2] not in self.messages:
                    self.messages.append(contents[2])
            elif type==STATE:
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
 
                     
if '__main__'==__name__:
    main()
    pass
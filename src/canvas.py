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
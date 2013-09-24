
import fileinput
from canvas import *
from chartCanvas import *
from constants import *  
from chartMatrixCanvas import * 

#third party import 
from pyparsing import *

gProcesses=[]
gMsgSequence=[]
gCmdMatrix = []
gMsgMatrix = []

def snd_matrix(column, process,toProcess,message):
    global gProcesses
    global gMsgMatrix
    
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
        
    if process not in gProcesses:
        gProcesses.append(process)

    if column == 0:  
        gMsgMatrix.append([(STATE,(process,astate))])  
    else:
        gMsgMatrix[len(gMsgMatrix)-1].append((STATE,(process,astate)))


def snd(process,toProcess,message):
    global gProcesses
    global gMsgSequence
 

    
    if process not in gProcesses:
        gProcesses.append(process)
    if toProcess not in gProcesses:
        gProcesses.append(toProcess)
    gMsgSequence.append((MESSAGE,(process,toProcess,message)))
    
def rcv(process,fromProcess,message):
    snd(fromProcess,process,message)
    
def state(process,astate):
    global gProcesses
    
    
    if process not in gProcesses:
        gProcesses.append(process)
    gMsgSequence.append((STATE,(process,astate)))

def proc(*processes):
    global gProcesses
    for process in processes:
        
        if process not in gProcesses:
            gProcesses.append(process)


 

def parseLine(line):
    line=line.strip()
    if len(line)==0: 
        return True
    if line.startswith(COMMENT):
        return True
    columns=line.split('|')
    gCmdMatrix.append(columns)

    pass

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
        snd( *theArgs)
    elif theFunction=='rcv':
        rcv( *theArgs)
    elif theFunction=='state':
        state( *theArgs)
    elif theFunction=='proc':  
        proc(*theArgs)  
    else:        
        raise 'cmd wrong'
        return False
    return True


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
    for line in fileinput.input():
        parseLine(line)
    #print(gCmdMatrix)    
    for row in gCmdMatrix  :        
            parseMatrixCmd(*row)
    #print(gMsgMatrix)        
    canvas=ChartMatrixCanvas(gProcesses, gMsgMatrix)
    #for line in fileinput.input():
    #    parseCmd(line)
    #canvas=ChartCanvas(gProcesses,gMsgSequence)
    canvas.draw()
    canvas.output()
    
                     
if '__main__'==__name__:
    main()
    pass
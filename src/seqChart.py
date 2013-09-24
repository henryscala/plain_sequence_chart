
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
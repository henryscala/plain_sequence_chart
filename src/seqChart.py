
import fileinput
from canvas import *
from chartCanvas import *
from constants import *  

#third party import 
from pyparsing import *

gProcesses=[]
gMsgSequence=[]
gAlias={}




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
    
                     
if '__main__'==__name__:
    main()
    pass
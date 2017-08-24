Plain Sequence Chart
====================

Official Site of Plain Sequence Chart is [https://github.com/henryscala/plain_sequence_chart](https://github.com/henryscala/plain_sequence_chart)

PSC, or Plain Sequence Chart, is a tool to generate MSC , or Message Sequence Chart, in plain text format via commands. 

I developed a skeleton of PSC years ago before I even knew github. Recently, I added new features to it and put it opensourced in github. 

MSC is widely used in software development. There're plenty of tools to draw MSC. Followed a list of them. 

-   [umlet](http://www.umlet.com/)

    umlet is a light weight UML chart drawing tool. MSC is able to be drawn via it manually. There's also way to generate ALL-INE-ONE MSC via sequence of commands. I didn't find this way before I wrote PSC. If I knew this way in advance, I may not choose to implement PSC. 

-   [js-sequence-diagrams](http://bramp.github.io/js-sequence-diagrams/)

    js-sequence-diagrams turns commands into UML sequence diagrams. It is actually what I want to implement in PSC. The good thing is it runs in browser, which is very easy to launch. However, for the time being, it does not support to output diagrams to plain text format. 

-   [asciiflow](http://www.asciiflow.com/)

    asciiflow is able to draw plain text diagrams and it also runs in browser, but we have to draw the diagrams manually. We cannot generate charts via commands. 

umlet, js-sequence-diagrams and asciiflow are all very good softwares. If you find that they fulfill your requirement, go to them without hesitation. I'd not implement PSC years ago if I knew these tools.  PSC has the limitation that you can only run it  in python(3.x) interpreter. I guess it is not a problem if you are a programmer. If you tolerate this limitation, it also has some features that other tools does not support, yet. I list some of them. 

- It generates MSC in plain text format which is easy to be presented and carried. 

- It supports parallel messages. It means messages are able to be sent between different instances(processes) in parallel, not necessarily in sequence.

- It supports abbreviated message names or instance names so as to shorten the width of generated chart. 

Some Terminologies 
-------------------

-   Process

    In MSC, messages go between entities, or instances. I name the entities or instances as processes. 

-   Message
    
    I think it is self-explanatory. Sometimes it is also referted to as primitive. 

-   State 
    
    It represents a process's status at a specific time. It can also be named as note or annotation. 

-   Alias 

    Give another name for messages or processes. 

Supported Commands
-------------------

Currently following commands are supported. Command names and arguments are separated by spaces. A new line character stands for the end of commands. If a line starts with "#", it is a comment line. 

-   SND fromProcess toProcess    message 

-   RCV toProcess   fromProcess  message

-   STATE process stateName 

-   PROC a-list-of-process-names
    
    This command is not mandatory. If you want to control the sequence of processes appeared in the generated chart, you may need it. 

-   ALIAS shortName longName 

Parallel Commands
--------------------

Parallel commands must locate in single line and separated by a "|" character. 

How to run? 
--------------------

Get PSC:

    git clone https://github.com/henryscala/plain_sequence_chart.git

or

[Download ZIP file](https://github.com/henryscala/plain_sequence_chart/archive/master.zip)

In your favorite shell only if it can run python(3.x), run "seqChart.py". Use input redirection operator "<" to specify input command file. Use output redirection operator ">" to specify to which file to generate the chart, otherwise the chart goes to standard output. 

    # python seqChart.py < inputFilePath > outputFilePath

Examples
--------------------

Followed 2 examples. 

###Basic Commands 

In this example, there's only one command on each line. Get your hand wet and get a general idea of PSC. PROC, SND, RCV and STATE commands are concerned. 

Input Commands:

    #specify the sequence of processes
    PROC  ALICE BOB CATHERINE DANIEL

    #messages between ALICE and BOB
    SND ALICE BOB INVITE
    RCV ALICE BOB 200

    #messages between CATHERINE and DANIEL
    SND CATHERINE DANIEL INVITE
    RCV CATHERINE DANIEL 200

    #messages between ALICE and DANIEL 
    SND ALICE DANIEL ACK

    #set state of ALICE
    STATE ALICE MID_SESSION
    STATE DANIEL MID_SESSION

    SND ALICE DANIEL BYE
    RCV ALICE DANIEL 200

Output Chart: 

       |-----|         |---|       |---------|     |------|
       |ALICE|         |BOB|       |CATHERINE|     |DANIEL|
       |-----|         |---|       |---------|     |------|
          |              |              |              |
          -----INVITE---->              |              |
          |              |              |              |
          <-----200-------              |              |
          |              |              |              |
          |              |              -----INVITE---->
          |              |              |              |
          |              |              <-----200-------
          |              |              |              |
          ---------------------ACK--------------------->
          |              |              |              |
    (~~~~~~~~~~~)        |              |              |
    (MID_SESSION)        |              |              |
    (~~~~~~~~~~~)        |              |              |
          |              |              |              |
          |              |              |        (~~~~~~~~~~~)
          |              |              |        (MID_SESSION)
          |              |              |        (~~~~~~~~~~~)
          |              |              |              |
          ---------------------BYE--------------------->
          |              |              |              |
          <--------------------200----------------------


###Parallel Commands  

In this example, there're parallel commands used separated by "|". Compare the differences with the first example(The two INVITEs are in the same line). PROC, SND, RCV, ALIAS and STATE commands are concerned. 

Input Commands:

    #specify alias first 
    ALIAS CAT CATHERINE 

    #specify the sequence of processes
    PROC  ALICE BOB CATHERINE DANIEL

    #messages between ALICE and BOB | #messages between CATHERINE and DANIEL     
    SND ALICE BOB INVITE            | SND CATHERINE DANIEL INVITE      
    RCV ALICE BOB 200               | RCV CATHERINE DANIEL 200       

    #messages between ALICE and DANIEL 
    SND ALICE DANIEL ACK

    #set state of ALICE
    STATE ALICE MID_SESSION
    STATE DANIEL MID_SESSION

    SND ALICE DANIEL BYE
    RCV ALICE DANIEL 200

Output Chart: 

          CAT = CATHERINE
       |-----|         |---|          |---|        |------|
       |ALICE|         |BOB|          |CAT|        |DANIEL|
       |-----|         |---|          |---|        |------|
          |              |              |              |
          -----INVITE---->              -----INVITE---->
          |              |              |              |
          <-----200-------              <-----200-------
          |              |              |              |
          ---------------------ACK--------------------->
          |              |              |              |
    (~~~~~~~~~~~)        |              |              |
    (MID_SESSION)        |              |              |
    (~~~~~~~~~~~)        |              |              |
          |              |              |              |
          |              |              |        (~~~~~~~~~~~)
          |              |              |        (MID_SESSION)
          |              |              |        (~~~~~~~~~~~)
          |              |              |              |
          ---------------------BYE--------------------->
          |              |              |              |
          <--------------------200----------------------

Note
-------------------

PSC is a opensourced software without any guarantee, and it may destroy the planet. It is up to you to determine whether use it or not. If you like and trust it, feel free to use it. 





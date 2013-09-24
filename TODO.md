Currently, each message occupies a line. It should be possible that multiple messages occupies a line only if they locate between different processes. 

https://github.com/bramp/js-sequence-diagrams/tree/master/src
instance C="C inst", A="A inst" B="B inst" D="D inst"

block AB_INIT { //optional 
A->B [: msg] //optional 
B<-A : ack
note right of A
note left of A
note over A
}

block CD_INIT {
	C->D : msg
	D<-C : ack
	note right of C
	note left of D
	note over C
}

parallel AB_INIT CD_INIT EF_INIT

or

parallel [
	[
A->B : hello 
B<-A : ack
	]

	[
C->D : hello 
C<-D : ack
	]

]

consider using solely  json format to construct the message sequence chart 


dont't need to copy others, just support keyword like implementations

title 
send
receive
state 
note
alias
instance


define func_name1
begin
	send argument[1] argument[2]
	receive
	state 
end 

function func_name2
begin
	send
	receive
	state 
end

parallel func_name1 func_name2

or support lisp like solution
[
sequence main
title 
send
receive
state 
note
]

(sequence
(title)
(instance)
(send from to msg)
(receive from to msg)
(state inst astate)
(parallel 
(sequence (send from to msg))
(sequence (send from to msg))
)
)

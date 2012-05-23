import sys
import socket
import string

HOST="irc.entropynet.net"
PORT=6667
NICK="SubnetBot"
IDENT="SubnetBot"
REALNAME="Subnet_ZerosBot"
CHAN="#compsci"
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))



while 1:
    readbuffer=readbuffer+s.recv(1024)
    print readbuffer
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[2])
        elif (line[1] == "NOTICE") :
           if (line[3] == ":Welcome") :
               s.send("JOIN %s\r\n" % CHAN)
           if (line[3] == ":This nickname is regestered") :
               s.send("PRIVMSG NickServ :ID subnetsoftware21")
        elif (line[1] == "PRIVMSG") :
            if (line[0] == ":jordanmkasla2009!jordanmkasla2@ceo.subnetsoftware") :
                if (line[3] == ":&quit" ) :
                    print "Attempting to Quit"
                    s.send("QUIT :killed \r\n")
                    s.close()
                    raise SystemExit
                

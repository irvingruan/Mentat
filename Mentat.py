#!/usr/bin/env python

"""

Copyright (c) 2012 Irving Y. Ruan <irvingruan@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

__author__ = 'Irving Y. Ruan <irvingruan@gmail.com>'
__version__ = '0.1b'

import sys
import socket
import os

class MentatError(Exception):
    """ TO DO """
    pass

class Mentat(object):
    """
        Representation of an IRC bot. Documentation will be added as progress is made.
        
        Methods:
            connect()
            disconnect()
            listen()
    
    """
    
    def __init__(self, host, port, nickname, botowner, identification=None, password=None, realname=None, defaultchannel=None):
        
        """ Must specify host, port, nickname, and bot owner.
        
            The rest is optional.
            
            Examples:
                host : irc.freenode.net
                port : 6667
                nickname : mentatbot
                botowner : iruan
                identification : mentatbot
                password : password
                realname : Mentat
                defaultchannel : ##python
        """
        
        self.__host = host
        self.__port = port
        self.__nickname = nickname
        self.__botowner = botowner
        self.__identification = identification
        self.__password = password
        self.__realname = realname
        self.__defaultchannel = defaultchannel
        
        self.__socket = 0
        
    def __str__(self):
        return '\nMentat : ' + __version__ + '\n\nBot nick: ' + self.nickname + '\nBot owner: ' + self.botowner + '\n\nHost: ' + self.host + '\n'
        
    def connect(self):
        """  
            Attempts to establish a connection with the IRC server.
            
            Returns : 
                True or False, depending on success of connection.
        """
        
        try:
            sys.stdout.write("Attempting to connect to...\nHost: " + self.host + "\nPort: " + str(self.port) + "\nNickname: " + self.nickname + "\n")
            
            self.__socket = socket.socket()
            self.__socket.connect( (self.host, self.port) )
            self.__socket.send('NICK ' + self.nickname + '\n')
            self.__socket.send('USER ' + self.identification + ' ' + self.host + ' bla :' + self.realname + '\n') # Identify to the server
            
            self.__socket.send('JOIN '+ self.defaultchannel + '\n')
            sys.stdout.write("\nSuccessfully connected!\n")
            
            return True
        except socket.error:
            sys.stdout.write("Failed to connect.\n")
            raise socket.error
            
    def disconnect(self):
        
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except socket.error:
            raise socket.error
            
    def listen(self):
        """
            Sits on the server and listens for messages.
        """
        
        while True: 
            server_message = self.__socket.recv(500)
            
            print server_message
            
            if server_message.find('PRIVMSG') !=- 1:
                self.__parse(server_message) 
                
                server_message = server_message.rstrip()
                server_message = server_message.split() 
                
                # Test custom command
                if (server_message[0] == 'PING'):
                    self.__socket.send('PONG ' + server_message[1] + '\n')
                    
    def __parse(self, message):
        complete = message[1:].split(':', 1)
        
        info = complete[0].split(' ') 
        msgpart = complete[1] 
        sender = info[0].split('!') 
        if msgpart[0] == '`' and sender[0] == self.botowner:
            # Messages starting with ` are commands
            command = msgpart[1:].split(' ') 
            if command[0] == 'op': 
                self.__socket.send('MODE ' + info[2] + ' +o ' + command[1] + '\n') 
            if command[0] == 'deop': 
                self.__socket.send('MODE ' + info[2] + ' -o ' + command[1] + '\n') 
            if command[0] == 'voice': 
                self.__socket.send('MODE ' + info[2] + ' +v ' + command[1] + '\n') 
            if command[0] == 'devoice': 
                self.__socket.send('MODE ' + info[2] + ' -v ' + command[1] + '\n') 
            if command[0] == 'sys': 
                syscmd(msgpart[1:], info[2]) 

        if msgpart[0]=='-' and sender[0] == self.botowner:
            # Treat msgs with - as explicit command to send to server 
            command = msgpart[1:] 
            self.__socket.send(command + '\n') 
            print 'cmd=' + command
            
    host = property(lambda self: self.__host)
    port = property(lambda self: self.__port)
    nickname = property(lambda self: self.__nickname)
    botowner = property(lambda self: self.__botowner)
    identification = property(lambda self: self.__identification)
    realname = property(lambda self: self.__realname)
    defaultchannel = property(lambda self: self.__defaultchannel)

def main():
    
    bot = Mentat('irc.freenode.net', 6667, 'mentatbot', 'iruan', 'mentatbot', 'password', 'Mentat', '##iruan')
    
    print bot
    
    if (bot.connect()):
        bot.listen()
        bot.disconnect()
    else:
        print "Failed to connect."
        
          
if __name__ == "__main__":
    main()
    sys.exit(0)
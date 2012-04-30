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
            self.__socket.send('USER ' + self.nickname + ' 0 * :' + self.realname + '\n') # Identify to the server
            
            self.__socket.send('JOIN '+ self.defaultchannel + '\n')
            sys.stdout.write("\nYou have successfully connected!\n\n")
            
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
            Sits on the server and listens for incoming messages.
        """
        
        while True: 
            server_message = self.__socket.recv(500)
            
            print server_message
            
            if server_message.find('PRIVMSG') != -1:    
                self.__parse(server_message) 
            
    
    def send_to_channel(self, channel, message):
        """
            Socket wrapper method for outputting text in the channel.
        """
        
        self.__socket.send('PRIVMSG ' + channel + " :" + message + '\n')

    def send_to_nickname(self, nickname, message):
        """
            Socket wrapper method for outputting text to a specific nickname.
        """
        self.__socket.send('PRIVMSG ' + channel + " :" + message + '\n')
                    
    def __parse(self, message):
        """
            Strips the message received on the server, NOTICE or PRIVMSG. Checks
            for commands detected in channel and via private message, and writes
            to the respective source.
            
            Arguments:
                message : The server message received, with server metadata and
                    content.            
        """
        
        complete_text = message.rstrip().split(':')[1::]
        
        if complete_text[0].find('#') != -1:
            channel = complete_text[0].rstrip().split(' ')[-1]
            message = complete_text[1].rstrip().split(' ')
            
            command = message[0]
            
            print "Channel: " + channel
            print "Command: " + command
            print "Message: " + ' '.join(message)
            
            # Just mimic command
            if command[0] == "!":
                self.send_to_channel(channel, ' '.join(message[1::]))
                     
            
    host = property(lambda self: self.__host)
    port = property(lambda self: self.__port)
    nickname = property(lambda self: self.__nickname)
    botowner = property(lambda self: self.__botowner)
    identification = property(lambda self: self.__identification)
    realname = property(lambda self: self.__realname)
    defaultchannel = property(lambda self: self.__defaultchannel)

def get_login_credentials(filepath):
    """
        Opens up config.txt to read in user-defined bot login.
        
        Arguments:
            filepath = The filepath of config.txt
        Returns:
            A dictionary with login info and values.

            Keys: host, port, nickname, botowner, identification, password, defaultchannel
    
    """
    
    login_data = {} 
    try:
        login_file = open(filepath, "r")
    except IOError as error:
        sys.stderr.write(error.errno + "\n")
        sys.stderr.write(error + "\n")
     
    for line in login_file:
        credential_data = line.rstrip().split('=')
        login_data[credential_data[0]] = credential_data[1]
        
    return login_data

def main():
    
    login_data = get_login_credentials("config.txt")
    
    bot = Mentat(login_data['host'], int(login_data['port']), login_data['nickname'], login_data['botowner'], login_data['identification'], login_data['password'], 'Realname', login_data['defaultchannel'])
    
    print bot
    
    if (bot.connect()):
        bot.listen()
            
    bot.disconnect()
        
if __name__ == "__main__":
    main()
    sys.exit(0)
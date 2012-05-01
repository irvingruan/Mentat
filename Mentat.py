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
        
        Mentat Connection and Data Transmission Methods:
            connect()
            disconnect()
            listen()
            send_to_channel()
            send_to_nickname()
        
        Mentat Bot Command Methods:
            help()
            ping()
            join()
            leave()            
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
        self.__currentchannel = defaultchannel
        
        self.__commands = {'help':self.help, 'ping':self.ping, 'join':self.join_channel, 'leave':self.leave_channel}
        
        self.__timer = 0
        
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
        timer = 0
        
        while True: 
            server_message = self.__socket.recv(500)
            print server_message
            
            self.__time()
            
            if server_message.find('PRIVMSG') != -1:    
                self.__parse(server_message) 
            
            timer += 1
            
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
        
    def help(self, current_channel):
        """
            Displays a list of Mentat commands to the current channel's users.
        """
        
        self.send_to_channel(current_channel, "Mentat " + __version__ + " Commands:\n")
        self.send_to_channel(current_channel, "\t!ping <target>\n")
        self.send_to_channel(current_channel, "\t!join <#channel>\n")
        self.send_to_channel(current_channel, "\t!leave <#channel>\n")
    
    def ping(self, current_channel, target):
        """
            Test command to make sure Mentat can reponse to a user.
            
            Args:
                current_channel : The current channel when receiving command.
                target : The message string to respond with PONG.
        """
        
        if len(target) > 0:
            self.send_to_channel(current_channel, "PONG " + target)
        
    def join_channel(self, channel_to_join, current_channel):
        """
            Makes Mentat join a channel, while remaining in the current one.
            
            Args:
                channel_to_join : The channel to join, should have # or ## chars
                current_channel : The current channel when receiving join command
        """
        
        if channel_to_join.find('#') != -1:
            self.__console("Joining channel " + channel_to_join)
            self.send_to_channel(current_channel, "Joining channel: " + channel_to_join + " ...")
            self.__socket.send('JOIN ' + channel_to_join + '\n')
        else:
            self.send_to_channel(current_channel, "Invalid channel: " + channel_to_join)
            
    def leave_channel(self, channel_to_leave, current_channel):
        """
            Makes Mentat leave a channel.
            
            Args:
                current_channel : The current channel when receiving join command
                channel_to_leave : The channel to leave, should have # or ## chars
        """
        
        if channel_to_leave.find('#') != -1:
            self.__console("Leaving channel " + channel_to_leave)
            self.send_to_channel(current_channel, "Leaving channel: " + channel_to_leave + " ...")
            self.__socket.send('PART ' + channel_to_leave + '\n')
        else:
            self.send_to_channel(current_channel, "Invalid channel: " + channel_to_leave)
                       
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
        
        # Text from channel, since it has # char prefix
        if complete_text[0].find('#') != -1:
            user = complete_text[0].rstrip().split('!')[0]
            current_channel = complete_text[0].rstrip().split(' ')[-1]
            message = complete_text[1].rstrip().split(' ')
            
            possible_command = message[0]
            
            self.__console("User = " + user)
            self.__console("Current Channel = " + current_channel)
            self.__console("Possible Command = " + possible_command)
            if len(message) > 1:
                self.__console("Message = " + message[1])
            
            # Only process commands if it originates from bot owner
            if user == self.botowner:
                self.__console("Message read from bot's owner, " + user)
                if possible_command[0] == "!":
                    command = possible_command[1::]
                    if command == "help":
                        self.commands[command](current_channel)
                    elif command == "ping":
                        self.commands[command](current_channel, target=message[1])
                    elif command == "join":
                        self.commands[command](message[1], current_channel)
                    elif command == "leave":
                        self.commands[command](message[1], current_channel)
            else:
                self.send_to_channel(self.currentchannel, user + ": You have insufficient privileges.")
        else:
            pass
            
    def __time(self):
        """
            Queries server for local time.
        """
        
        self.__socket.send("TIME\n")
    
    def __console(self, message):
        sys.stderr.write("Console Output: " + message + "\n")
                 
            
    host = property(lambda self: self.__host)
    port = property(lambda self: self.__port)
    nickname = property(lambda self: self.__nickname)
    botowner = property(lambda self: self.__botowner)
    identification = property(lambda self: self.__identification)
    realname = property(lambda self: self.__realname)
    defaultchannel = property(lambda self: self.__defaultchannel)
    currentchannel = property(lambda self: self.__currentchannel)
    commands = property(lambda self: self.__commands)

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
    
    login_data = get_login_credentials("login.txt")
    
    bot = Mentat(login_data['host'], int(login_data['port']), login_data['nickname'], login_data['botowner'], login_data['identification'], login_data['password'], 'Realname', login_data['defaultchannel'])
    
    print bot
    
    if (bot.connect()):
        bot.listen()
            
    bot.disconnect()
        
if __name__ == "__main__":
    main()
    sys.exit(0)
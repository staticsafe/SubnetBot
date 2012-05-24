#! /usr/bin/env python

from connect import Connection
from parse import *
import time

## Load Settings
settings = settings_load()

## Create Connection
connection = Connection(settings)

## Connect to Server
connection.connect()

## Register on Server
connection.register()

## Create modules array
modules = []

while 1:
    if connection.ssl ==-True:
        buffer = connection.sock.read(4096)
    else:
        buffer = connection.sock.recv(4096)
    print buffer
    lines = splitline(buffer)
    for line in lines:
        message = parse(line)
        if message.type == "NOTICE":
            if connection.logged_in == False:
                if message.source == "NickServ":
                    if connection.botpass != '':
                        print 'Logging in...'
                        login = connection.identify()
                        if login == True:
                            connection.logged_in = True
                            print 'Login successful!'
                        elif login == False:
                            print 'Login failed, check your password an try again.'
                            raise SystemExit
                        time.sleep(2)
                        connection.join_channel("#compsci")
                        connection.join_channel("#subnetsoftware")
                for channel in connection.channel:
                    connection.join_channel(channel)
                    connection.logged_in == True
        if message.type == "PRIVMSG":
            module_results = command_parser(message, connection)
            if module_results != None:
                connection.write('PRIVMSG {0} :{1}'.format(message.args[0], module_results))
            else:
                pass
        if message.type == "PING":
            connection.write("PONG {0}".format(message.source))

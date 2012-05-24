import json
import urllib
import urllib2
from xml.etree import ElementTree
from events import MessageObj as Message
from modules.twitter import TwitterWrapper as Twitter
from modules.stock import GoogleFinanceAPI as Stock

def settings_load():
    ''' try loading settings from json, if failed recreate them'''
    try:
        print 'Loading Settings...'
        with open('settings.json', 'rb') as f:
            settings = json.load(f, encoding='utf-8')
            print 'Load Successful!'
            return settings
    except:
        print 'Load Failed, recreating...'
        settings = dict()
        settings['server'] = 'irc.entropynet.net'
        settings['servername'] = 'EntropyNetIRC'
        settings['port'] = 6697
        settings['botnick'] = 'SubnetBot'
        settings['botpass'] = 'subnetsoftware21'
        settings['botowner'] = 'jordanmkasla2009'
        settings['channel'] = '#compsci'
        settings['SSL'] = True
        with open('settings.json', 'wb') as f:
            json.dump(settings, f)

        return settings

def splitline(data):
    ''' Splits the lines we got back and fixes any cut-off messages '''
    lines = data.split("\r\n")
        #if the last line is not terminated buffer it
    if lines[len(lines)-1][:-2] != "\r\n":
        buf = lines[len(lines)-1]
        del lines[-1:]
    return lines

def parse(line):
    ''' Parses a line and converts it into a Message object '''
    source = None
    parts = line.split(' ')
    if parts[0].startswith(':'):
        # Nick!ident@host
        source = parts.pop(0)[1:]

    # command (such as PRIVMSG)
    command = parts.pop(0)

    # arguments (such as #channel)

    args = []

    # the actual "message" (such as "Hello" in a PRIVMSG)
    message = ''

    # Loop through the remaining splits and add them to the proper place
    while len(parts) > 0:
        # If we encounter a : we have hit the "message" part
        if parts[0].startswith(':'):
            # add it to the variable and jump out of the loop
            message = ' '.join(parts)[1:]
            break
        else:
            # Everything else will be treated as arguments to the command
            args.append(parts.pop(0))
    #return the message object
    message = message.split(' ')
    return Message(nih_to_user(source), command, args, message)

def nih_to_user(nih):
    ''' Converts a standard Nick!Ident@Host to an User object '''
    if nih is None:
        return None

    identind = nih.find('!')
    hostind = nih.find('@')

    return nih[:identind]

def command_parser(message_object, connection):
    message = message_object
    twitter = Twitter()
    stock = Stock()

    if message.msg[0] == '&quit':
        if message.source == 'staticsafe' or message.source == 'fox' or message.source == 'jordanmkasla2009' or message.source == 'Subnet_Zero' or message.source == 'Jupdown' or message.source == 'cafejunkie':
            connection.write("QUIT :I have been killed by my owner.")
            connection.disconnect()
            raise SystemExit
        else:
            connection.write("PRIVMSG {} : Permission denied. Your actions have been reported.".format(message.source))
            print '{} tried and failed to force me to quit'.format(message.source)
    elif message.msg[0] == '&join':
        if message.source == 'staticsafe' or message.source == 'fox' or message.source == 'jordanmkasla2009' or message.source == 'Subnet_Zero' or message.source == 'Jupdown' or message.source == 'cafejunkie':
            connection.join_channel(message.msg[1])
        else:
            connection.write("PRIVMSG {} : Permission denied. Your actions have been reported.".format(message.source))
            print '{0} tried and failed to force me to join channel {1}'.format(message.source, message.msg[1])                         
    elif message.msg[0] == '&help':
        connection.write("PRIVMSG {0} : {1}, Available Commands are: join, part, quit".format(message.args[0], message.source))
    elif message.msg[0] == '&twitnick':
        results = twitter.register_user(message.source, message.msg[1])
        return results
    elif message.msg[0] == '&twitter':
        try:
            twitter_user = message.msg[1]
        except IndexError:
            twitter_user = message.source
        results = twitter.get_status(twitter_user)
        return results
    elif message.msg[0] == '&tweetid':
        try:
            results = twitter.id_lookup(message.msg[1])
        except IndexError:
            return 'Not enough arguments, please add a twitter id.'
        return results
    elif message.msg[0] == '&stock':
        try:
            stock.get(message.msg[1], message.msg[2])
            results = stock.parse()
        except:
            results = "an error has occurred while getting data"
        return results
    elif message.msg[0] == '&part':
        if message.source == 'staticsafe' or message.source == 'fox' or message.source == 'jordanmkasla2009' or message.source == 'Subnet_Zero' or message.source == 'Jupdown' or message.source == 'cafejunkie':
            connection.part_channel(message.msg[1])
        else:
            connection.write("PRIVMSG {} : Permission denied. Your actions have been reported.".format(message.source))
            print '{0} tried and failed to force me to part channel {1}'.format(message.source, message.msg[1])
    else:
        pass

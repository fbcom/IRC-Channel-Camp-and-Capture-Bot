# -*- coding: utf-8 -*-
import time
from pprint import pprint
import socket


class Bot():

    def __init__(self, cfg):
        self.cfg = cfg
        self.readbuffer = ''
        self.joined_channels_flag = True

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.cfg.get('host'), self.cfg.get('port')))
        self.sock.send("NICK %s\r\n" % self.cfg.get('nick'))
        self.sock.send("USER %s %s bla :%s\r\n" % (self.cfg.get('ident'), self.cfg.get('host'), self.cfg.get('realname')))
        self.sock.send("MODE %s +B\r\n" % (self.cfg.get('ident')))
        for channel in self.cfg.get('channels'):
            self.sock.send("JOIN %s\r\n" % channel)

        time.sleep(3)

        while True:
            for line in self.receive_messages(1024):
                print "IN: %s" % line
                line = line.rstrip()
                line_segments = line.split()

                # respond to server pings
                if self.respond_to_ping(line_segments):
                    self.join_channels_lazy()
                    self.cycle_empty_channels()
                    continue

                if self.is_part_channel(line_segments):
                    continue

                if self.is_join_channel(line_segments):
                    continue

                if self.is_invite_channel(line_segments):
                    continue

                #TODO: respond to channel kicks
                #TODO: respond to messages from admin (relay them to a channel)
                #TODO: respond to ppl getting kicked/banned/disconnected/leaving

    def is_part_channel(self,  line_segments):
        if len(line_segments) >= 3:
            if line_segments[1].upper() == "PART":
                user = line_segments[0]
                channel = line_segments[2]
                self.send_message("user %s parted %s " % (user, channel))

    def is_join_channel(self,  line_segments):
        if len(line_segments) >= 3:
            if line_segments[1].upper() == "JOIN":
                user = line_segments[0]
                channel = line_segments[2][1:]
                self.send_message("user %s joined %s " % (user, channel))

    def is_invite_channel(self, line_segments):
        if len(line_segments) >= 4:
            if line_segments[1].upper() == "INVITE":
                inviter = line_segments[0]
                invited = line_segments[2]
                channel = line_segments[3][1:]
                self.send_message("user %s invited %s to %s" % (inviter, invited, channel))

                if invited == self.cfg.get('nick'):
                    self.send_message("JOIN %s" % channel)
                    self.add_channel_to_joinlist(channel)
                    self.get_users_in_channel(channel)

    def add_channel_to_joinlist(self, channel):
        channels = cfg.get('channels')
        channels.append(channel)
        channels = list(set(channel))
        cfg.set('channels', channels)
        cfg.save()

    def remove_channel_from_joinlist(self, channel):
        channels = cfg.get('channels')
        if channel in channels:
            del channels[channels.index(channel)]
            cfg.set('channels', channels)
            cfg.save()

    def get_users_in_channel(self, channel):
        self.send_message("WHO %s" % channel)
        #TODO: parse answer in different method

    def is_kicked_channel(self, line_segments):
        if len(line_segments) >= 4:
            if line_segments[1].upper() == "KICK":
                channel = line_segments[2]
                kicked = line_segments[3]
                kicker = line_segments[4][1:]
                #self.send_message_to("user %s kicked %s from %s" % (kicker, kicked, channel), "TODO")
                if kicked == self.cfg.get('nick'):
                    print " GOT KICKED "
                    self.remove_channel_from_joinlist(channel)

    def cycle_empty_channels(self):
        #TODO:
        # get list of all channels
        # check how many ppl are in these channels
        # check if bot is op
        #   recycle channel if not op
        #       flag channel where no op on recycling
        pass

    def receive_messages(self, buffersize):
        self.readbuffer = self.readbuffer + self.sock.recv(buffersize)
        messages = self.readbuffer.split("\n")
        self.readbuffer = messages.pop()  # keep chars in the buffer that are not yet followed by a newline
        return messages

    def send_message(self, message):
        print "OUT: %s" % message
        self.sock.send("%s\r\n" % message)

    def send_message_to(self, message, to):
        print "OUT: %s" % message
        self.sock.send("PRIVMSG %s %s\r\n" % (to, message))

    def respond_to_ping(self, line_segments):
        if(line_segments[0] == "PING"):
            self.send_message("PONG %s" % line_segments[1])
            return True
        return False

    def join_channels_lazy(self):
        if not self.joined_channels_flag:
            self.join_channels()
            self.joined_channels_flag = True

    def join_channels(self):
        for channel in self.cfg.get('channels'):
            self.send_message("JOIN %s" % channel)
            time.sleep(1)

    def cycle_channel
(self, channel):
        send_message("PART %s" % channel)
        time.sleep(1)
        send_message("JOIN %s" % channel)

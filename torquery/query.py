#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os, sys
import urllib
import urllib2
import time, re

import socks #SocksiPy
import socket

import stem
import stem.process

from random import choice

def print_bootstrap_lines(line):
    if "Bootstrapped " in line:
        sys.stdout.write("%s\n" % line)

class Query(object):
    """
        This class handle the query.
    """
    def __init__(self, url, verbose=True, request_data={}, method="GET", socketPort=None, tor_cmd="/usr/bin/tor"):
        if not method in ["GET","POST","PUT","DELETE"]: 
            raise Exception("The method could be GET, POST, PUT or DELETE")
        
        self.url = url
        self.method = method
        self.request_data = request_data

        if not socketPort:
            for port in range(9050,9100):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(("127.0.0.1", port))
                if result == 0:
                    socketPort = port
                sock.close()
            if not socketPort:
                socketPort = 9050

        if verbose:
            sys.stdout.write("using port: %s\n" % socketPort)
            sys.stdout.flush()

        # Saving the old socket
        self.__old_socket = socket.socket
        # Initializing the tor external process
        self.tor_process = stem.process.launch_tor_with_config(
            config = {
                'SocksPort': str(socketPort),
                'ControlPort': str(socketPort+1)
                },
            tor_cmd=tor_cmd,
            init_msg_handler=print_bootstrap_lines
        )

        # is_query_working is a function to verify if the query is working.
        self.is_query_working = None

        # Installing the proxy
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', socketPort)
        socket.socket = socks.socksocket
        
        self.__socketPort = socketPort
        self.__controlPort = socketPort+1
        self.user_agents = [
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                'Opera/9.25 (Windows NT 5.1; U; en)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
            ]

    def perform(self):
        """
            Perform the query: call the URL using TOR proxy.
        """
        if socket.socket == self.__old_socket:
            raise Exception("Using old socket")

        if self.request_data != {}:
            data = urllib.urlencode( self.request_data )
            req = urllib2.Request(self.url, data)
        else:
            req = urllib2.Request(self.url)

        req.add_header('User-Agent', choice(self.user_agents) )
        conn = urllib2.urlopen(req)
        return conn.read()

    def new_identity(self):
        """
            Send to tor process the NEWNYM signal and wait 5 seconds 
        """
        tor_ctrl = self.__old_socket(socket.AF_INET,socket.SOCK_STREAM)
        tor_ctrl.connect(("127.0.0.1", self.__controlPort))
        tor_ctrl.send('AUTHENTICATE "{}"\r\nSIGNAL NEWNYM\r\n'.format(None))
        response = tor_ctrl.recv(1024)
        if response != '250 OK\r\n250 OK\r\n':
            sys.stderr.write('Unexpected response from Tor control port: {}\n'.format(response))
        time.sleep(5)

    def check_ip(self):
        """
            Return the IP address using http://checkip.dyndns.org
        """
        html = urllib2.urlopen("http://checkip.dyndns.org").read()
        ricerca = re.search("\d+\.\d+\.\d+\.\d+", html)
        return ricerca.group(0)

    def single_cycle(self, wait_time=1, verbose=True):
        """
            Execute a single "query" cycle:
               1. Get a new identity from TOR
               2. Perform the query
               3. Check the URL content to understand if the query made is ok
        """
        self.new_identity()
        time.sleep(wait_time)

        output = self.perform()
        if self.is_query_working != None:
            is_going = self.is_query_working(self, output)
            if not is_going:
                time.sleep(30)
                return

        if verbose:
            sys.stdout.write("[ %s ] IP: %s - %s\n" % (time.ctime(), self.check_ip(), volte))
            sys.stdout.flush()

    def start_loop(self, wait=[15,6,4,3,8], verbose=True):
        """
            Start an infinite loop of self.single_cycle
        """
        volte = 0
        while 1:
            try:
                self.single_cycle( wait_time=choice(wait), verbose=verbose)
                volte += 1
            except KeyboardInterrupt:
                sys.stdout.flush()
                if verbose:
                    sys.stdout.write("Queries made: %s\n" % volte)
                return volte

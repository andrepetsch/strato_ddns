#import httplib
#import daemon
from encodings import utf_8
import ipaddress
import argparse
from unittest import result
import dns.resolver as resolver
import urllib.request
import time
import base64

class strato_ddns:

    def __init__(self, config_path = "./strato_ddns.conf", debug = False):

        self.debug = debug
        # init variables
        self.daemon = 3600
        self.server = "dyndns.strato.com"
        self.query_url = "/nic/update?"
        self.login = ""
        self.password = ""
        self.domain = []
        self.ipv4 = "" # web?

        self.ipv4_dns = ""
        self.ipv4_real = ""
        self.ipv6 = "" # web?
        self.ipv6_dns = ""
        self.ipv6_real = ""

        # read config
        self.read_config(config_path=config_path)

        if self.login=="" or self.password=="" or self.domain == []:
            raise Exception("Missing information (login/pwd/domain) in .conf")
        if self.ipv4=="" or self.ipv6=="":
            raise Exception("Missing information (IPv4/IPv6) in .conf")

        # prepare resolver
        self.resolver = resolver.Resolver()
        self.resolver.nameservers=['8.8.8.8', '8.8.4.4', '2001:4860:4860::8888', '2001:4860:4860::8844'] # TODO: make changeble

        # prepare urllib
        # create a password manager
        self.password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        top_level_url = "https://"+self.server
        self.password_mgr.add_password(None, top_level_url, self.login, self.password)

        self.handler = urllib.request.HTTPBasicAuthHandler(self.password_mgr)

        # create "opener" (OpenerDirector instance)
        self.opener = urllib.request.build_opener(self.handler)

    def read_config(self, config_path):
        if self.debug: print("reading and processing debug file")
        
        f = open(config_path)
        try:
            lines = f.readlines()
            for l in lines:
                l = l.strip()
                if l.startswith('#'):
                    # exclude comments
                    pass
                elif l == "":
                    # pass empty lines
                    pass
                else:
                    c = l.split('=')
                    option = str(c[0]).strip()
                    value = c[1]
                    
                    if self.debug: print("option:", option, "\tvalue:", value)

                    if option == "daemon":
                        self.daemon = int(value)
                    elif option == "server":
                        self.server = str(value).strip()
                    elif option == "query_url":
                        self.query_url = str(value).strip()
                    elif option == "login":
                        self.login = str(value).strip()
                    elif option == "password":
                        self.password = str(value).strip()
                    elif option == "domain":
                        self.domain= str(value).strip().split(',')
                    elif option == "ipv4":
                        value = str(value).strip()
                        if value == "web":
                            self.ipv4 = value
                        else:
                            # parses to ip, throws error if no ip given
                            ip = ipaddress.ip_address(value)
                            self.ipv4 = value                            
                    elif option == "ipv6":
                        value = str(value).strip()
                        if value == "web":
                            self.ipv6 = value
                        else:
                            # parses to ip, throws error if no ip given
                            ip = ipaddress.ip_address(value)
                            self.ipv6 = value
                    else:
                        # unexpected arguments in configuration
                        raise Exception("invalid configuration")

        except Exception as e:
            print("Could not process .conf: ", str(e))
            exit()

        finally:
            f.close()
            if self.debug: print("FINISHED .config\n")
        
    def run(self):
        
        for d in self.domain:
            # form updatestring
            if self.debug: print("\nSTART: update run for", d)    
            change = False
            # prepare IPv4
            if self.ipv4 != "":
                self.ipv4_dns = self.resolver.query(d, 'A')
                if len(self.ipv4_dns) < 0: self.ipv4_dns = 'none'
                #elif len(self.ipv4_dns) >= 1: self.ipv4_dns = self.ipv4_dns[0]
                else: self.ipv4_dns = self.ipv4_dns[0] 
                if self.debug: print("Resolved domain",d,"to IPv4", self.ipv4_dns)
                if self.ipv4 == "web":
                    self.ipv4_real = urllib.request.urlopen('http://ipv4.ident.me').read().decode('utf8')
                    if self.ipv4_dns != self.ipv4_real: change=True
                    if self.debug: print("Real external IPv4 is",self.ipv4_real)
                else:
                    if self.ipv4 != self.ipv4_dns:
                        self.ipv4_real=self.ipv4
                        change=True
                        if self.debug: print("Static external IPv4 is",self.ipv4_real)
                    else:
                        self.ipv4_real=self.ipv4
                        if self.debug: print("Static external IPv4 is up to date! -",self.ipv4_real)
            # prepare IPv6
            if self.ipv6 != "":
                self.ipv6_dns = self.resolver.query(d, 'AAAA')
                if len(self.ipv6_dns) < 0: self.ipv6_dns = 'none'
                #elif len(self.ipv6_dns) >= 1: self.ipv6_dns = self.ipv6_dns[0]
                else: self.ipv6_dns = self.ipv6_dns[0] 
                if self.debug: print("Resolved domain",d,"to IPv6", self.ipv6_dns)
                if self.ipv6 == "web":
                    self.ipv6_real = urllib.request.urlopen('http://ipv6.ident.me').read().decode('utf8')
                    if self.ipv6_dns != self.ipv6_real: change=True
                    if self.debug: print("Real external IPv6 is",self.ipv6_real)
                else:
                    if self.ipv6 != self.ipv6_dns:
                        self.ipv6_real=self.ipv6
                        change=True
                        if self.debug: print("Static external IPv6 is",self.ipv6_real)
                    else:
                        self.ipv6_real=self.ipv6
                        if self.debug: print("Static external IPv6 is up to date! -",self.ipv6_real)
            
            # if change is True, a update is necessary
            if change:
                if self.debug: print("\nUPDATE NECESSARY")
                update_string = "https://" +self.server+self.query_url
                update_string = update_string + "hostname=" + d + "&"
                update_string = update_string + "myip=" + self.ipv4_real + "," + self.ipv6_real #
                if self.debug: print("\nUPDATESTRING:",update_string)

                # use the opener to fetch a URL
                self.opener.open(update_string)

                # Install the opener.
                # Now all calls to urllib.request.urlopen use our opener.
                urllib.request.install_opener(self.opener)

                update_response = urllib.request.urlopen(update_string)
                code= update_response.code
                if str(code) != "200":
                    print("Error-Code:", code)

                update_response = update_response.read().decode('utf_8')
                if update_response.startswith("abuse"):
                    print("ABUSE:", update_response)
                else:
                    print("whatever:", update_response)
                # TODO: log response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Updates ip on strato dyndns")
    parser.add_argument(
        '--config',
        '-c',
        help="configuration file",
        type=str,
        default="../strato_ddns.conf",
        required=False
        )
    parser.add_argument(
        '--debug',
        '-d',
        help="turn on debug information",
        action="store_true"
    )

    args = parser.parse_args()

    debug = False
    if args.debug: debug = True

    s = strato_ddns(config_path=args.config, debug=debug)
    while True:
        s.run()
        time.sleep(1800)

    
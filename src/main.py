#import httplib
#import daemon
import ipaddress
import argparse

from sqlalchemy import true

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
        
    def run(self):
        # form updatestring
        
        change = False

        if self.ipv4 != "":
            # TODO: lookup dns ipv4
            if self.ipv4 == "web":
                # TODO: lookup real ipv4
                # TODO: write to self.ipv4_real
                pass
            else:
                if self.ipv4 != self.ipv4_dns:
                    self.ipv4_real=self.ipv4

        # TODO: IPv6
        # TODO: complete updatestring
        # TODO: send updatestring
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
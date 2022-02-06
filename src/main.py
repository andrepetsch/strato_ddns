import httplib, daemon

class strato_ddns:
    def __init__(self):
        self.daemon = 3600
        self.server = "dyndns.strato.com"
        self.query_url = "/nic/update?"
        self.login = ""
        self.password = ""
        self.domain = []
        self.ipv4 = "web"
        self.ipv6 = "web"

    def __init__(self, config_path = "./strato_ddns.conf"):
        self.__init__()
        self.read_config(config_path=config_path)

    def read_config(self, config_path):
        f = open(config_path)
        try:
            lines = f.readlines()
            for l in lines:
                l = l.strip()
                if l.startswith('#'):
                    # exclude comments
                    pass
                else:
                    c = l.split('=')
                    option = str(c[0])
                    value = c[1]
                    if option == "daemon":
                        self.daemon = int(value)
                    elif option == "server":
                        self.server = str(value)
                    elif option == "query_url":
                        self.query_url = str(value)
                    elif option == "login":
                        self.login = str(value)
                    elif option == "password":
                        self.password = str(value)
                    elif option == "domain":
                        self.domain= str(value).split(',')
                    elif option == "ipv4":
                        # TODO: check for 'web' or valid ip-address
                        self.ipv4 = str(value)
                    elif option == "ipv6":
                        # TODO: check for 'web' or valid ip-address
                        self.ipv6 = str(value)

        except Exception as e:
            print("Could not read .conf: ", str(e))
        

if __name__ == '__main__':
    pass
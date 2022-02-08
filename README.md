# Strato DDNS
Helps setting dynamic DNS with Strato. Works for IPv4 and IPv6.

***This all referes to dyndns with Strato. It's not testet with other providers nor checked for compatibility with any rfc!***

## Motivation
I wanted to use my webserver with IPv4 and IPv6 simultaneously. No problem with Apache. Worked with my Fritz!Box and my ISP. But somehow I couldn't manage to set it up with the dyndns-update-client I used. It was either IPv4 or IPv6, although [Strato supports setting both at the same time](https://www.strato.de/faq/hosting/so-einfach-richten-sie-dyndns-fuer-ihre-domains-ein/). I was looking for an alternative client, but the way Strato describes seemed to be quiet simple, so I tried my self.

## Configuration

A sample configuration is given.

- `server`: holds the provider's update server (*dyndns.strato.com*)
- `query_url`: holds the update path of the server (*/nic/update?*)
- `login`: your login, in case of Strato it's your domain (*yourdomain.de*)
- `password`: the password you have set for your domain to update your dyndns ([look here for help](https://www.strato.de/faq/hosting/so-einfach-richten-sie-dyndns-fuer-ihre-domains-ein/))
- `domain`: the domain you want to update, use "`,`" to seperate multiple domains
- `ipv4`: use `web` for automatic lookup, use static IP if available
- `ipv6`: see `ipv4`, ***if `web` is used, `ipv6_suffix` must be set***
- `ipv6_suffix`: your router might give your host a stativ IPv6 suffix. You must use this, your public IPv6 ***won't work*** with port forwarding only! If the Network changes the software will use the new Network but the same IPv6 suffix.
- `nameserver`: optionaly set your own nameservers to lookup the acually used IP-Addresses seperated by "`,`". Standard is: *8.8.8.8,8.8.4.4, 2001:4860:4860::8888, 2001:4860:4860::8844*

## Commandline arguments
- `-h`: help
- `--config/-c <path>`: set a path to your own configurationfile, default is `../stato_ddns.conf`
- `--debug/-d`: get detailed information to find errors
- `--dryrun/-t`: doesn't do any change, best use with `-d` to find errors without triggering the abuseblocker

## What is next?
Until now this tool runs as a program only, in a crontab e.g.. Next step will be to make it useable as a daemon.
# Eero Client - Starter client for Eero API Interactions

![badge](https://img.shields.io/github/workflow/status/bruskiza/eero-client/Python%20package)
[![Coverage Status](https://coveralls.io/repos/github/bruskiza/eero-client/badge.svg?branch=develop)](https://coveralls.io/github/bruskiza/eero-client?branch=develop)

Having seen 343max/eero-client's excellent starter project, I went ahead and forked it.

This is a very simple client lib to access information about your eero home network. I got this API by intercepting the traffic of the eero app.

Right now it support the following features:
- login/login verification
- user_token refreshing
- account (all information about an account, most importantly a list of your networks)
- networks (information about a particular network)
- devices (a list of devices connected to a network)
- reboot

The API is pretty nice and it should be kind of easy to extend it from here if you miss something. There are a lot of URLs in the response json that will help you explore the API further.

There is a sample client that you might use for your experiments. On first launch it will ask you for the phone number you used to create your eero account. Afterwards you've been asked for the verfication code that you got via SMS. From here on you are logged in - running the command again will dump a ton of information about your network(s).

# Usage:

After cloning: 

```
workstation: eero-client $ virtualenv ve
workstation: eero-client $ . ve/bin/activate
(ve) workstation: eero-client $ pip install -r requirements.txt
(ve) workstation: eero-client $ ./sample.py
Usage: sample.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  device    Prints out the information for a specific device
  devices   Show all the devices connected to your network
  eeros     Shows all the eeros on your network
  log       TODO: Not implemented
  login     Login to eero API
  networks  Shows available networks.
  reboot    Reboot an eero
  summary   Summary of your network (This contains the most information)
(ve) workstation:eero-client $ 
```
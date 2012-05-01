Mentat
=====

**Your friendly neighborhood IRC bot**

Written by Irving Y. Ruan — [irvingruan@gmail.com](irvingruan@gmail.com)

## About

Mentat is a lightweight IRC bot written in Python. It can be used as a standalone program or integrated with other code as an object-oriented IRC bot. Mentat is designed to be small, lightweight, and easily extendable.

## Requirements

Mentat will run on any *nix system with Python >= 2.4 installed.

## Usage

**Standalone Mode**

To run Mentat as a standalone IRC bot on your server or computer:

`$ ./Mentat.py`

Mentat will then launch and attempt to connect to the IRC server with the information you provided in `login.txt`. Upon successful connection, Mentat will idle and listen for valid commands received in the channel.

**Mentat as a Module**

To use Mentat as a module:

	import Mentat

	mentat = Mentat("irc.example.com", 6667, nickname="mentat",
		botowner="mentatowner", identification="mentat", password="password", 
		realname="piter", defaultchannel="##dune")

	if (mentat.connect()):
		mentat.listen()
		
And replace the fields with the login credentials you have created for that server.

**Mentat Commands**

Mentat currently supports the following list of basic commands:

* **!help** — Displays available list of commands in the channel
* **!ping \<target\>** — Responds with PONG [target]
* **!join \<channel\>** — Joins the specified channel
* **!leave \<channel\>** — Leaves the specified channel

## Legal

Mentat is Copyright (c) 2012 Irving Y. Ruan and MIT licensed. The full text of the license can be found in LICENSE.
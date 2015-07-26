#!/usr/bin/env python

import irc.bot
import irc.strings
import subprocess # Oh god.
import io

class DoorBot(irc.bot.SingleServerIRCBot):
    """A bot for handling commands to the door. Obviously.

    Common method arguments
        conn - IRC connection
        ev - irc.client.Event
    """
    def __init__(self, channel, nickname, server, port=6667):
        """Initialize connection

        Args
            channel - Channel to join
            nickname - Nickname to use; also used as the real name
            server - Server to connect to
            port - Server port
        """
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname,
            nickname)
        self.channel = channel

        self.door = Door()

    def on_nicknameinuse(self, conn, ev):
        """Append _ until we get a nickname that's not in use"""
        conn.nick(conn.get_nickname() + "_")

    def on_welcome(self, conn, ev):
        """Hop in a channel after full connection is done"""
        conn.join(self.channel)

    def on_privmsg(self, conn, ev):
        """Execute commands received via private message"""
        self.do_command(ev, ev.arguments[0])

    def on_pubmsg(self, conn, ev):
        """Execute commands if prefixed with the bot's name"""
        args = ev.arguments[0].split(" ", 1)

        if len(args) > 0 and args[0][0] == "~":
            cmd = irc.strings.lower(args[0][1:])
            submitted_args = args[1:]

            self.do_command(ev, cmd, submitted_args)

        return

    def do_command(self, ev, cmd, submitted_args):
        """So not done"""
        nick = ev.source.nick

        if cmd == "die":
            self.die()
        elif cmd == "say":
            if len(submitted_args) > 0:
                self.door.say(submitted_args[0])
        elif cmd == "play":
            pass
        elif cmd == "read":
            pass
        elif cmd == "license":
            self.connection.privmsg(
                self.channel,
                "AGPL; please ask NegativeK for my source."
            )

class Door(object):
    def __init__(self):
        pass

    def say(self, thing_to_say):
        process = subprocess.Popen(
                ["festival", "--tts"],
                stdin=subprocess.PIPE,
        )
        process.stdin.write(bytes(thing_to_say, "ascii"))
        process.stdin.close()

def main():
    config = {
        "channel": "#pumpingstationone",
        "nickname": "doormon",
        "server": "irc.freenode.net",
        "port": 6667,
    }

    bot = DoorBot(
            config["channel"],
            config["nickname"],
            config["server"],
            config["port"],
    )
    bot.start()

if __name__ == "__main__":
    main()

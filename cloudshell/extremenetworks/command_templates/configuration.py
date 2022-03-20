# !/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate


# UPLOAD = CommandTemplate(
#     "upload configuration {address} {filename}"
# )

# MOVE = CommandTemplate("mv {src} {dst}")

# DEBUG_TRIGGER = CommandTemplate("mkdir dummy_dir")

SAVE_CONFIGURATION = CommandTemplate(
    "save configuration {local_filename}",
    action_map=OrderedDict(
        {  # todo test this map
            r"and overwrite it\? \(y\/N\)": lambda session, logger: session.send_line("y", logger),
            r"Do you want to save configuration": lambda session, logger: session.send_line("y", logger),
            r"the default database\?": lambda session, logger: session.send_line("n", logger),
        }
    )
)

LS = CommandTemplate(
    "ls {path}",
)

SHOW_SWITCH = CommandTemplate(
    "show switch",
    action_map=OrderedDict(
        {
            r"Press .SPACE. to continue or .+ to quit": lambda session, logger: session.send_line("", logger)
        }
    )
)

TFTP_PUT = CommandTemplate(
    "tftp put {remote_server_ip} [vr {vr}] {local_filepath} {remote_filepath}",
    action_map=OrderedDict(
        {
            r"Uploading .+ done!": lambda session, logger: logger.info("Uploading success"),
        }
    ),
    error_map=OrderedDict(
        {
            r"No such file or directory": "no such file message in error map",
            r"bad address": "bad addr message in error map",
            r"Could not connect with": "not connect error msg",
        }
    )
)

TFTP_GET = CommandTemplate(
    "tftp get {remote_server_ip} [vr {vr}] {remote_filepath} force-overwrite {local_filepath}",
)

RM = CommandTemplate(
    "rm {filepath}",
    action_map=OrderedDict(
        {
            r"[Rr]emove .+\?": lambda session, logger: session.send_line("y", logger),
        }
    ),
)

COPY = CommandTemplate(
    "cp {src} {dst}",
    action_map=OrderedDict(
        {
            # Copy 'primary.cfg' from '/usr/local/cfg' to '/usr/local/cfg/secondary.cfg'? (y/N) Yes
            r"Copy .+from .+to": lambda session, logger: session.send_line("y", logger),
            # todo add overwrite handling
        }
    )
)

REBOOT = CommandTemplate(
    "reboot",
    action_map=OrderedDict(
        {
            r"Do you want to save configuration changes .+\?":
                lambda session, logger: session.send_line("n", logger),
            r"you sure you want to reboot the switch\?":
                lambda session, logger: session.send_line("y", logger),
        }
    ),
    error_map=OrderedDict({})
)

USE_CONFIGURATION = CommandTemplate(
    "use configuration {filepath}"
)

#######

CONFIGURE_REPLACE = CommandTemplate(
    "configure replace {path} [{vrf}]",
    action_map=OrderedDict(
        {
            r"[\[\(][Yy]es/[Nn]o[\)\]]": lambda session, logger: session.send_line(
                "yes", logger
            ),
            r"\[confirm\]": lambda session, logger: session.send_line("", logger),
            r"\(y\/n\)": lambda session, logger: session.send_line("y", logger),
            r"[\[\(][Nn]o[\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]es[\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]/[Nn][\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"overwrit+e": lambda session, logger: session.send_line("yes", logger),
        }
    ),
    error_map=OrderedDict(
        {
            r"[Aa]borting\s*[Rr]ollback|"
            r"[Rr]ollback\s*[Aa]borted|"
            r"(?<=%).*(not.*|in)valid.*(?=\n)": Exception(
                "Configure replace completed with error"
            ),
            r"[Ii]nvalid\s*([Ii]nput|[Cc]ommand)|[Cc]ommand rejected": Exception(
                "Restore override mode is not supported"
            ),
        }
    ),
)

WRITE_ERASE = CommandTemplate(
    "write erase",
    action_map=OrderedDict(
        {
            r"[\[\(][Yy]es/[Nn]o[\)\]]": lambda session, logger: session.send_line(
                "yes", logger
            ),
            r"\[confirm\]": lambda session, logger: session.send_line("", logger),
            r"\(y\/n\)": lambda session, logger: session.send_line("y", logger),
            r"[\[\(][Nn]o[\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]es[\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]/[Nn][\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
        }
    ),
)



REDUNDANCY_PEER_SHELF = CommandTemplate(
    "redundancy reload shelf",
    action_map=OrderedDict(
        {
            r"[\[\(][Yy]es/[Nn]o[\)\]]": lambda session, logger: session.send_line(
                "yes", logger
            ),
            r"\[confirm\]": lambda session, logger: session.send_line("", logger),
            r"\(y\/n\)|continue": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]/[Nn][\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
        }
    ),
)

REDUNDANCY_SWITCHOVER = CommandTemplate(
    "redundancy force-switchover",
    action_map=OrderedDict(
        {
            r"[\[\(][Yy]es/[Nn]o[\)\]]": lambda session, logger: session.send_line(
                "yes", logger
            ),
            r"\[confirm\]": lambda session, logger: session.send_line("", logger),
            r"\(y\/n\)|continue": lambda session, logger: session.send_line(
                "y", logger
            ),
            r"[\[\(][Yy]/[Nn][\)\]]": lambda session, logger: session.send_line(
                "y", logger
            ),
        }
    ),
)

SHOW_VERSION_WITH_FILTERS = CommandTemplate(
    "[do{do}] show version [| include {filter}]"
)

CONSOLE_RELOAD = CommandTemplate("reload")

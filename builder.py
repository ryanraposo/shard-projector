import os
import json
import configparser

cluster_json = {
    "MISC": {
        "max_snapshots": {
            "default": "6",
            "value": None
        },
        "console_enabled": {
            "default": "true",
            "value": None
        }
    },
    "SHARD": {
        "shard_enabled": {
            "default": "false",
            "value": None
        },
        "bind_ip": {
            "default": "127.0.0.1",
            "value": None
        },
        "master_ip": {
            "default": "none",
            "value": None
        },
        "master_port": {
            "default": "10888",
            "value": None
        },
        "cluster_key": {
            "default": "none",
            "value": None
        }
    },
    "STEAM": {
        "steam_group_only": {
            "default": "false",
            "value": None
        },
        "steam_group_id": {
            "default": "0",
            "value": None
        },
        "steam_group_admins": {
            "default": "false",
            "value": None
        }
    },
    "NETWORK": {
        "offline_cluster": {
            "default": "false",
            "value": None
        },
        "tick_rate": {
            "default": "15",
            "value": None
        },
        "whitelist_slots": {
            "default": "0",
            "value": None
        },
        "cluster_password": {
            "default": "",
            "value": None
        },
        "cluster_name": {
            "default": "New World",
            "value": None
        },
        "cluster_description": {
            "default": "",
            "value": None
        },
        "lan_only_cluster": {
            "default": "false",
            "value": None
        },
        "cluster_intention": {
            "default": "cooperative",
            "value": None
        },
        "autosaver_enabled": {
            "default": "true",
            "value": None
        }
    },
    "GAMEPLAY": {
        "max_players": {
            "default": "16",
            "value": None
        },
        "pvp": {
            "default": "false",
            "value": None
        },
        "game_mode": {
            "default": "survival",
            "value": None
        },
        "pause_when_empty": {
            "default": "false",
            "value": None
        },
        "vote_enabled": {
            "default": "true",
            "value": None
        }
    }
}


def add_info_field():

    for key, value in cluster_json.items():
        for k, v in value.items():
            cluster_json[key][k]["info"] = ""

def add_info_to_json():

    with open('data/ini/default_cluster.ini', 'r',encoding='utf-8') as ini_file:
        current_section = ""
        current_option = ""
        for line in ini_file:
            line = str(line).rstrip("\n")
            if line.startswith("["):
                current_section = line[1:-1]
            elif not line=="" and len(line) > 0 and line[0].isalpha():
                current_option = line.split("=")[0]
            elif line == "":
                continue
            elif not line.startswith("    ; Default:") and not line.startswith("\n") and not line.startswith("    ; Req"):
                cluster_json[current_section][current_option]["info"] += line + " "


    for value in cluster_json.values():
        for v in value.values():
            v["info"] = v['info'].replace("    ; ", " ")

    print(json.dumps(cluster_json, indent=4))

add_info_field()
add_info_to_json()
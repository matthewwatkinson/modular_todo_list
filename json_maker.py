#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

master_dict = {}
master_dict["current_list"] = ""
master_dict["existing_lists"] = {}
master_dict["modules"] = {}

print(master_dict)

with open("list_storage.json", "w") as file:
    json.dump(master_dict, file, indent=2)

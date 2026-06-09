#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

# no JSON loading should be necessary in final form, should be handled on startup in list script

json_dictionary = data_load()

#but only use json if we don't have a session state
if "json_data" not in st.session_state:
    st.session_state["json_data"] = json_dictionary
else:
    # otherwise we need to save the latest state to json
    data_save()

# using a passed key (hardcoded for now)
# get the list name, title it with an edit button
# for each item in the list, write it and have an edit or delete button (steal from module menu)

list_key = "Camping gear"
list_title = list_key
list_contents = st.session_state["json_data"]["modules"][list_key]

# put in a container with two columns, one for edit
st.title(list_title)

for item in list_contents:
    st.write(item)
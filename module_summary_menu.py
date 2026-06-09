#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
from dictionary_scratchpad import *

# no JSON loading should be necessary in final form, should be handled on startup in list script

# json_dictionary = data_load()

# #but only use json if we don't have a session state
# if "json_data" not in st.session_state:
#     st.session_state["json_data"] = json_dictionary
# else:
#     # otherwise we need to save the latest state to json
#     data_save()


if "module_edit_button_input" not in st.session_state:
    st.session_state.module_edit_button_input = False


def module_list_sorter():
    module_list_to_sort = st.session_state["json_data"]["modules"]
    sorted_dict = dict(sorted(module_list_to_sort.items(), key=lambda item: item[0].lower()))
    st.session_state["json_data"]["modules"] = sorted_dict

def module_list_draw():
    for key in st.session_state["json_data"]["modules"]:

        @st.dialog(title="Are you sure you want to delete this module?", dismissible=False)
        def delete_confirm(name=key):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("OK", type="primary", use_container_width=True):
                    delete_update(name)
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        def delete_update(name=key):
            
            del st.session_state["json_data"]["modules"][name]
            del st.session_state[f"{name}_delete_button"]
    
        col1, col2, col3, col4 =st.columns([8, 2, 1, 1])

        with col1:
            st.write(f"{key}")

        with col2:
            st.write(f"({len(st.session_state["json_data"]["modules"][key])} items)")

        with col3:
             if st.button(
                label="✏️",
                key=f"{key}_edit_button",
            ):
                # record the module to be edited
                st.session_state.module_to_edit = key
                # switch to edit page
                st.switch_page("module_edit_menu.py")

        with col4:
            st.button(
                label="🗑️",
                key=f"{key}_delete_button",
                on_click=delete_confirm
            )

module_list_sorter()

# use all thise code in module edit menu
# if st.session_state.module_edit_button_input:
#     # retrieve module to be edited
#     module_name = st.session_state["module_to_be_edited"]
#     with st.form(key="edit_module_name_input"):
#         user_input = st.text_input(f"Edit name for '{module_name}':")
#         edit_form_button_container = st.container(horizontal=True) 
#         with edit_form_button_container:
#             submit_button = st.form_submit_button(label="Confirm", type="primary")
#             cancel_button = st.form_submit_button(label="Cancel")

#         if submit_button:
#             if user_input:
#                 # test to see if it already exists in the session_state
#                 if user_input in st.session_state["json_data"]["modules"]:
#                     # don't add it
#                     st.warning("A module with this name already exists")
#                 else:
#                     # replace it, and delete the now unneeded key
#                     content_dict = st.session_state["json_data"]["modules"]
#                     # retrive the old list to be passed
#                     old_list = content_dict[module_name]
#                     # delete old edit button keys
#                     del st.session_state[f"{module_name}_edit_button"]
#                     # now add the new module key and value
#                     content_dict[user_input] = old_list
#                     # delete the old one
#                     del content_dict[module_name]
#                     # and replace into session state
#                     st.session_state["json_data"]["modules"] = content_dict
#                     st.session_state.module_edit_button_input = False
#                     #refresh
#                     st.rerun()
#             else:
#                 st.warning("Module name can not be blank")
#         if cancel_button:
#             st.session_state.module_edit_button_input = False
#             st.rerun()


st.title("Modules")
module_list_draw()

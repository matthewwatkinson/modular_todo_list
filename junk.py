#new_module_button =  st.button("➕", key="new_module_button")  

# if new_module_button:
#     # trigger popup with new module name input. check if it exists, then switch page
#     st.session_state.new_module_button_input = True

# if st.session_state.new_module_button_input:
#     with st.form(key="new_module_input"):
#         user_input = st.text_input("Add a new module:")
#         form_button_container = st.container(horizontal=True) 
#         with form_button_container:
#             submit_button = st.form_submit_button(label="Add", type="primary")
#             cancel_button = st.form_submit_button(label="Cancel")

#         if submit_button:
#             if user_input:
#                 # test to see if a module with this name exists
#                 if user_input not in st.session_state["json_data"]["modules"]:
#                     # add it as an empty list and reset input key
#                     st.session_state["json_data"]["modules"][user_input] = []
#                     st.session_state.new_module_button_input = False
#                     # jump to edit page
#                     st.session_state.module_to_edit = user_input
#                     st.switch_page("module_edit_menu.py")

#                 else:
#                     # don't add it
#                     st.warning("Module with this name already exists")
#             else:
#                 st.warning("Please enter some text before submitting.")
#         if cancel_button:
#             st.session_state.new_module_button_input = False
#             st.rerun()

#############


#new_list_button =  st.button("➕", key="new_list_button")  

#if new_list_button:
    # trigger popup with new list name input. check if it exists, then switch page
#     st.session_state.new_list_button_input = True

# if st.session_state.new_list_button_input:
#     with st.form(key="new_list_name_input"):
#         user_input = st.text_input("Input name for new list")
#         form_button_container = st.container(horizontal=True) 
#         with form_button_container:
#             submit_button = st.form_submit_button(label="Confirm", type="primary")
#             cancel_button = st.form_submit_button(label="Cancel")

#         if submit_button:
#             if user_input:
#                 # test to see if a list with this name exists
#                 if user_input not in st.session_state["json_data"]["existing_lists"]:
#                     # add it as an empty dict, make it the current_list, and reset input key
#                     st.session_state["json_data"]["existing_lists"][user_input]= {}
#                     st.session_state["json_data"]["existing_lists"][user_input]["tier_0_list"] = list_builder(user_input, [], 0)
#                     st.session_state["json_data"]["current_list"] = user_input
#                     st.session_state.new_list_button_input = False
#                     # jump to edit page
#                     st.switch_page("current_list.py")

#                 else:
#                     # don't add it
#                     st.warning("List with this name already exists")
#             else:
#                 st.warning("Please enter some text before submitting.")
#         if cancel_button:
#             st.session_state.new_list_button_input = False
#             st.rerun()

###############



# if st.session_state.add_button_input:
#     with st.form(key="new_item_input"):
#         user_input = st.text_input("Add an item:")
#         form_button_container = st.container(horizontal=True) 
#         with form_button_container:
#             submit_button = st.form_submit_button(label="Add", type="primary")
#             cancel_button = st.form_submit_button(label="Cancel")

#         if submit_button:
#             if user_input:
#                 # test to see if it already exists in any sub_dicts
#                 current_key = st.session_state["json_data"]["current_list"]
#                 if not item_crosschecker(user_input, 0, st.session_state["json_data"]["existing_lists"][current_key]):
#                     # add it
#                     st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"][user_input] = False
#                     st.session_state.add_button_input = False
#                     st.rerun()  # Instantly refreshes to show updated state
#                 else:
#                     # don't add it
#                     st.warning("Item already exists")
#             else:
#                 st.warning("Please enter some text before submitting.")
#         if cancel_button:
#             st.session_state.add_button_input = False
#             st.rerun()  # Instantly refreshes to show updated state
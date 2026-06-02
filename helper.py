#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import jsonpickle

with open("module_list_storage.json", "r") as f:
    module_dictionary_pickled = json.load(f)

module_dictionary = jsonpickle.decode(module_dictionary_pickled)


class ListItem:
    # each list item belongs to an owner_list, has a name and a done/not_done state

    def __init__(self, item_name, state=False, owner_list="unknown"):
        self.item_name = item_name
        self.state = state
        self.owner_list = owner_list

    def __str__(self):
        # print all the info we know about this item
        return f"task: {self.item_name} belongs to {self.owner_list} and is {self.state}"
    
    def __eq__(self, other):
        return self.item_name == other

    def status_change(self):
        # toggles between done and not done
        if self.state == False:
            self.state = True
        else:
            self.state = False

    def name_change(self, new_name: str):
        # edit the item name
        self.item_name = new_name

class ListModule:

    def __init__(self, list_name):
        # create a new to-do list
        self.list_name = list_name
        self.item_list = []

    def add_item(self, new_item_name: str):
        # add a new item, put in list if does not already exists and is valid input
        if not new_item_name:
            print("\nPlease provide a valid task name in order to add to list")
            return
        if new_item_name in self.item_list:
            print(f"\nThe to-do item '{new_item_name}' already exists.")
        else:
            self.item_list.append(ListItem(new_item_name, "not_done", self.list_name))
            print(f"\n{new_item_name} added successfully.")

    def remove_item(self, existing_item: str):
        # remove an item, if it exists and is valid input, and list not empty
        if not self.item_list:
            print("\nThere are no items in this list")
            list_modifier_menu(self)
        if not existing_item:
            print("\nPlease provide a valid task name in order to remove from list")
            return
        if existing_item in self.item_list:
            self.item_list.remove(existing_item)
            print(f"\n{existing_item} removed successfully.")
        else:
            print(f"\nThe to-do item '{existing_item}' does not exist.")

    def item_toggle(self, target):
        #toggle an item, if it exists
        if target not in self.item_list:
            print(f"{target} is not an item in this list")
        else:
            target_index = self.item_list.index(target)
            self.item_list[target_index].status_change()

    def all_done(self, message):
        for item in self.item_list:
            item.state = "done"
        if message == 1:
            print(f"All items in {self.list_name} set to 'done'")
    
    def all_undone(self, message):
        for item in self.item_list:
            item.state = "not_done"
        if message == 1:
            print(f"All items in {self.list_name} set to 'not_done'")

    def __str__(self):
        print_string = "\n"
        if not self.item_list:
            return "\nYour list does not have any items yet"
        for item in self.item_list:
            done = "x"
            if item.state == "done":
                done = "o"
            print_string += f" {done} | {item.item_name} belongs to {item.owner_list} and is {item.state}\n"
        return print_string
    
    def display_as_line(self):
        list_length = len(self.item_list)
        name_length = len(self.list_name)
        spaces = " " * (20 - name_length)
        #print 20 total name and spaces
        print(f"{self.list_name}{spaces}contains {list_length} items")

    def display_as_module(self):
        print(f"\nThe module {self.list_name} contains the following items:\n")
        for i in self.item_list:
            print(i.item_name)
    
    def save_as_module(self):
        # add the currently displayed list to the module dictionary after setting all items to "undone"
        # unless already exists or empty
        if self.list_name in module_dictionary:
            overwrite_choice = input("\nA module with this name already exists. Would you like to overwrite the existing module y/n? ")
            if overwrite_choice == "n":
                print("You can rename the list and save as a new module\n")
                list_modifier_menu(self)
        else:
            if not self:
                print("Can not save empty list as module")
                list_modifier_menu(self)
            self.all_undone(0)
            module_dictionary[self.list_name] = self
            #save to json
            json_compatible_module_dict = jsonpickle.encode(module_dictionary)
            with open("module_list_storage.json", "w") as f:
                json.dump(json_compatible_module_dict, f, indent=2, )
            print(f"Added to modules as {self.list_name}")
            list_modifier_menu(self)

    def module_delete(self):
            are_you_sure = input(f"\nAre you sure you wish to permanently delete '{self.list_name}'?  y/n: ")
            if are_you_sure == "y":
                del module_dictionary[self.list_name]
                print(f"\n'{self.list_name}' successfully deleted")
                #save to json
                json_compatible_module_dict = jsonpickle.encode(module_dictionary)
                with open("module_list_storage.json", "w") as f:
                    json.dump(json_compatible_module_dict, f, indent=2, )
                module_display_menu()
            else:
                module_display_menu()



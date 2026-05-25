#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### need to make data persistent between sessions

### need to make a list addable to a list

### need to make the starting interface

class ListItem:
    # each list item belongs to an owner_list, has a name and a done/not_done state

    def __init__(self, item_name, state="not_done", owner_list="unknown"):
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
        if self.state == "not_done":
            self.state = "done"
        else:
            self.state = "not_done"

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
            print("Please provide a valid task name in order to add to list")
            return
        if new_item_name in self.item_list:
            print(f"The to-do item '{new_item_name}' already exists.")
        else:
            self.item_list.append(ListItem(new_item_name, "not_done", self.list_name))
            print(f"{new_item_name} added successfully.")

    def remove_item(self, existing_item: str):
        # remove an item, if it exists and is valid input
        if not existing_item:
            print("Please provide a valid task name in order to remove from list")
            return
 
        if existing_item in self.item_list:
            self.item_list.remove(existing_item)
            print(f"{existing_item} removed successfully.")
        else:
            print(f"The to-do item '{existing_item}' does not exist.")

    def item_toggle(self, target):
        #toggle an item, if it exists
        if target not in self.item_list:
            print(f"{target} is not an item in this list")
        else:
            target_index = self.item_list.index(target)
            self.item_list[target_index].status_change()

    def __str__(self):
        print_string = ""
        for item in self.item_list:
            done = "x"
            if item.state == "done":
                done = "o"
            print_string += f" {done} | {item.item_name} belongs to {item.owner_list} and is {item.state}\n"
        return print_string


test_list = ListModule("test_list")
test_list.add_item("cooking")
test_list.add_item("cleaning")
test_list.add_item("cleaning")
input_test = input("Input the task that you would like to add to the list: ")
test_list.add_item(input_test)

print(test_list)
test_list.remove_item("polishing")
test_list.remove_item("cleaning")

print(test_list)



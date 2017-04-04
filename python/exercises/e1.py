# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:03:35 2017

@author: ntelford
"""


def tips(bill, rate):
    ''' Return the total payable amount from a bill and tip rate'''
    
    tip = round((bill * rate),2)

    return bill + tip
    
def go():
    bill = input("What's the bill total?")
    rate = input("What's the tip rate?")
    print(tips(float(bill), float(rate)))

if __name__ == "__main__":
    go()
#!/usr/bin/python2
from getchar import getchar
from feedline import feedline
from feedline import return_counter
import sys
import os
import cPickle as pickle
def prompt():
    """
    Initiates a basic python interface.
        Args:
            None.
        Returns:
            None.
    Note: Written and tested on Mac OSX. The strings returned by getchar on other systems may differ.
    """
    outstring=""
    history=[]
    counter=0
    while True:
        new_char=getchar()
        if new_char=="\r" or new_char=="\n": # Sends outstring to feedline, saves to history and resets if user presses newline
            feed = feedline(str(outstring))
            sys.stdout.write("\n" + str(feed))
            history.append(outstring)
            counter=len(history)
            outstring=""
        elif new_char=='\x04': # Resets outstring if user presses ctrl-d. Exits if outstring is already empty
            if len(outstring)>0:
                outstring=""
                sys.stdout.write("\nKeyboardInterupt")
                sys.stdout.write("\n" + feedline(str(outstring)))
            else:
                print "\nkthnxbai!"
                break;
        elif new_char=='\x1b' and len(history)>0: # moves up or down in history if user presses the up or down keys, respectively.
            updown=sys.stdin.read(2)
            if updown=='[A':
                if counter>0:
                    counter-=1
                outstring=history[counter]
                sys.stdout.write("\nIn [{0}]: ".format(return_counter())+outstring)
            elif updown=='[B':
                if counter<len(history)-1:
                    counter+=1
                if len(history)>counter:
                    outstring=history[counter]
                sys.stdout.write("\nIn [{0}]: ".format(return_counter())+outstring)
        else:
            if new_char=='\x7f': # Erase last character if user hits backspace (not a requirement for INF3331, it turns out, but convenient nonetheless). I think this might only works on Mac, as a co-student informed me that getchar returns a different string for backspace on linux/windows. I haven't tested this, but I have been told getchar returns '\x7f' for ctrl + backspace on windows/linux, so if you review this on a different system and want to use backspace, it might work if you hold down ctrl simultaneously.
                outstring=outstring[:-1]
                sys.stdout.write("\b \b")
            else: # adds new character to outstring and prints to screen
                outstring=outstring+new_char
                sys.stdout.write(new_char)
                

if __name__ == "__main__":
    print "Welcome to mypython!"
    sys.stdout.write("In [0]: ")
    prompt()
    
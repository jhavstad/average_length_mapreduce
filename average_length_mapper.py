#! /usr/bin/env python

import sys # Used for sys.stdin and sys.stdout
import csv # Used for csv.reader and csv.writer

def mapper():
    # The input reader breaks the input line into tokens delimited by tabs
    reader = csv.reader(sys.stdin, delimiter='\t')
    # The output writer that places the input tokens into an output formated by delimited tabs
    writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # Iterate over each line of input
    for line in reader:
        # Attempt to parse the input, catching any errors that may occur
        try:
            key      = line[0] # The node ID is the first token from the input
            posttype = line[5] # The post type is the sixth token from the input
            txt      = line[4] # The body text of the post is the fifth token from the input
            parent   = line[6] # The parent ID of this post
            
            # If the length of the text is 0 then continue on, the post is irrelevant to this problem
            if len(txt) == 0:
                continue
            
            # If the post type is a question, then flag the data type with a 1
            if posttype == 'question':
                posttype = 1
            # If the post type is a comment, then flag the data type with a 2 (ignore in reducer)
            elif posttype == 'comment':
                posttype = 2
            # If the post type is an answer, then flag the data type with a 3
            else:
                posttype = 3
                
            # If the parent key is not an integer value then replace it with a '-1' to be kind
            # to the reducer when it attempts to read an integer
            if not parent.isdigit():
                parent = '-1'
                
            # Populate the output tokens with the node ID (key), the posttype flag, and the length of the text
            output = [key, posttype, len(txt), parent]
            # Write out the tokens to the output to send to the reducer
            writer.writerow(output)
            
        # Caught an error, which is probably due to an unexpected result fromt the input
        # so, continue on
        except:
            continue

def main():
    mapper()
    
if __name__ == '__main__':
    main()
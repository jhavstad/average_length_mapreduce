#! /usr/bin/env python

import sys # Used for sys.stdin and sys.stdout
import csv # Used for csv.reader and csv.writer

# This function takes in all the parameters and prints out a formatted output
def writeOutput(key, post_length, answer_length_sum, num_answers, writer):
    answer_avg_length = 0 # The average answer length of a post
    # If the number of answers is 0 then then the average answer length is 0
    # (also avoid division by 0 when calculating the average)
    if num_answers == 0:
        answer_avg_length = 0
    else:
        answer_avg_length = answer_length_sum / num_answers
    # Place the node ID (key), the post (question) length, and the average
    # answer length into a list of output tokens and then write out to the output
    output = [key, post_length, answer_avg_length]
    writer.writerow(output)

def reducer():
    # The input reader breaks the input line into tokens delimited by tabs
    reader = csv.reader(sys.stdin, delimiter='\t')
    # The output writer that places the input tokens into an output formated by delimited tabs
    writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # A dictionary that will store a dictionary for each question in the following format
    # ['question_length':n, 'answer_length_sum':m, 'num_answers':l]
    # The question node ID is used as the key for the dictionary elements
    # question_length is the text length of the question body on the forum
    # answer_length_sum is the summation of all the lengths of all the answers posted to this question
    # num_answers is the number of answer posts to this question
    # With answer_length_sum and num_answers the average answer post length can be determined
    question_posts = dict()
    
    # Iterate over each line of input
    for line in reader:
        # Attempt to parse the input, catching any errors that may occur
        try:
            key        = int(line[0]) # The key is first token from the input
            posttype   = int(line[1]) # The post type is the second token from the input
            length     = int(line[2]) # The length is the third token from the input
            parent_key = int(line[3]) # The parent ID is the fourth token from the input
                
            # The post is a question (encoding sent from the mapper)
            if posttype == 1:
                if key not in question_posts:
                    question_posts[key] = dict()
                    # Populate keys with default values in new dictionary
                    question_posts[key]['question_length']   = length
                    question_posts[key]['answer_length_sum'] = 0
                    question_posts[key]['num_answers']       = 0

            # The post is an answer (encoding sent from the mapper)
            elif posttype == 3:
                # If the parent key is -1 and this an answer post then there must be a problem
                # with the data so ignore this line and continue to the next line
                if parent_key == -1:
                    continue
                if parent_key not in question_posts:
                    question_posts[parent_key] = dict()
                    # Populate keys with default values in new dictionary
                    question_posts[parent_key]['question_length']   = 0
                    question_posts[parent_key]['answer_length_sum'] = 0
                    question_posts[parent_key]['num_answers']       = 0
                # Add length of answer post to running sum
                question_posts[parent_key]['answer_length_sum'] += length
                # Increment count of number answers for post
                question_posts[parent_key]['num_answers'] += 1
            # Ignore comments
            
        # Caught an error, which is probably due to an unexpected result fromt the input
        # so, continue on
        except:
            continue
    
    # Write out the values for all the question nodes
    for question_post in question_posts:
        key               = question_post
        post_length       = question_posts[key]['question_length']
        answer_length_sum = question_posts[key]['answer_length_sum']
        num_answers       = question_posts[key]['num_answers']
        writeOutput(key, post_length, answer_length_sum, num_answers, writer)

def main():
    reducer()
    
if __name__ == '__main__':
    main()
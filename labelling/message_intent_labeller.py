import json
import os

chat_dir = os.path.expanduser('~/adla/data/NLP/whatsapp')
chat_fps = [os.path.join(chat_dir, fn) for fn in os.listdir(chat_dir)]
save_dir = os.path.expanduser('~/adla/data/NLP/whatsapp/intents')

key_intent_dict = {
    's': 'my size is',
    #'o': 'other',                                       # use this to request a new intent
    't': 'return',
    'r': 'new request',
    'i': 'add more info to request',
    'q': 'question about process',
    't': 'confirm to try something on',
    'x': 'confirm DON\'T want to try something on',
    'c': 'adjust item',
    'd': 'offer a delivery time',
    'c': 'confirm delivery time',
    'a': 'acknowledge message',
    'u': 'unknown intent',
    'g': 'greeting',
    'p': 'addition to previous',
    'k': 'question about a product'
}

'''
# MAKE JSON FILE FOR FRTHER OPTIONS ONCE EACH INTENT IS CLASSIFIED
templ = ['option1']
further_options_fp = os.path.join(save_dir, 'further_options.json')
with open(further_options_fp, 'w') as f:
    d = {value: templ for _, value in key_intent_dict.items()}
    print(d)
    json.dump(d, f)

k
'''

# LABELLING THE INTENT OF EACH MESSAGE
for chat_idx, chat_fp in enumerate(chat_fps):                               # for each chat file
    with open(chat_fp, 'r') as f:                                           # open a new file
        messages = f.readlines()[1:]                                            # get lines (messages) of file
        msg_intent_pairs = []                                               # init empty list to store msg-intent pairs
        other_ops = []
        for msg_idx, message in enumerate(messages):                        # for each message (each one of those lines)

            user = message.split(' ')[2][:-1]

            message = message.strip('\r\n')
            message = message[23:]
            print(message)                                                  # print the message

            if user != 'Adla':
                intent_key = input('INTENT: ')                                  # get the key indicating the msg intent
                while intent_key not in key_intent_dict:                        # if that's not a valid key (from the dict)
                    print('Are you sure that\'s a valid intent key? Check the legend')
                    intent_key = input('Intent: ')  # collect the intent again

                print()
                if intent_key == 'o':
                    other_op = input('What would be a better intent classification for this message?')

                intent = key_intent_dict[intent_key]                            # find the class corresponging to button pressed
                msg_intent_pair = {'message': message, 'intent': intent}        # make dict of {msg: intent} pair
                #messages[idx] = message.split(' ')
                msg_intent_pairs.append(msg_intent_pair)                        # add this msg-intent pair to list for this chat

            if msg_idx == 0:
                pass
                #break

        save_fp = os.path.join(save_dir, chat_fp.split('.')[0].split('/')[-1] + '.json')        # take name of chat to save json in adjacent folder
        with open(save_fp, 'w') as outfile:                                 # open output file for writing to
            json.dump(msg_intent_pairs, outfile)                            # dump list of msg-intent
            print(save_fp)
        if len(other_ops) != 0:
            print('other ops were present')
        #messages = [msg for msg in messages]

    if chat_idx == 0:
        pass
        #break

example = json.load(open(save_fp))
print(type(example))


'''
END GOAL
create a labeller
have a file for each chat, which is a list of {message: intent} 
'''
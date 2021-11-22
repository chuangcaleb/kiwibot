import json

data_file = open('intents.json').read()
intents_file = json.loads(data_file)

# On startup, set context to prompt name
context_filter = 'hi'
filter_list = {}

for intent in intents_file['intents']:
    if ('context' in intent):
        filter_list[intent['tag']] = intent.get('context').get('filter')
    # if (intent['context']['filter'] == context_filter):z
    #     print(intent['context'])
print(filter_list)
#         if context['filter'] == context_filter:
#             filtered_intents = intent['tag']

# print(filtered_intents)

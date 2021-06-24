import json
import ijson
from ijson.common import ObjectBuilder
from os import path
from GroundedScan.dataset import GroundedScan

#load_dataset_from = "/home/czw/Documents/2021/groundedSCAN/data/demo_dataset/dataset.txt"
load_dataset_from = "/home/czw/Documents/2021/compositional_splits_ids/compositional_splits/dataset.txt"
output_directory = "/home/czw/Documents/2021/groundedSCAN/output/"

#grounded_scan = GroundedScan.load_dataset_from_file(load_dataset_from,
#                                                    output_directory)
#
example = {}
ex_path = "/home/czw/Documents/2021/jan_portal/data/adverb_1/557819"

summary = ["intransitive_verbs", "transitive_verbs", "adverbs",
           "nouns", "color_adjectives", "size_adjectives",
           "grid_size", "min_object_size", "max_object_size",
           "type_grammar", "max_recursion",] # "percentage_train"]

all_data = {}
#with open(load_dataset_from, "r") as f:
#    objs = ijson.kvitems(f, 'item')
#    key_values = ((k,v) for k, v in objs if k in summary)
#    #key_values = ((k,v) for k, v in objs)
#    for k,v in key_values:
#        print(k)
#        all_data[k] = v

def objects(file):
    key = '-'
    start = False
    for prefix, event, value in ijson.parse(file):
        #print(prefix, event, value)
        if 'start' in event:
            start = True
        if prefix == '' and event == 'map_key' and value in summary:  # found new object at the root
            #import pdb; pdb.set_trace()
            key = value  # mark the key value
            builder = ObjectBuilder()
            start = False
        elif prefix.startswith(key):  # while at this key, build the object
            builder.event(event, value)
            if start and 'end' in event:  # found the end of an object at the current key, yield
                yield key, builder.value
            elif not start:# not an object, just a plain old value
                yield key, value


summary_data_path = "summary_data.json"

if path.exists(summary_data_path):
    with open(summary_data_path, "r") as f:
        all_data = json.load(f)
else:
    with open(load_dataset_from, "r") as f:
        for key, value in objects(f):
            print(key, value)
            all_data[key] = value

    with open(summary_data_path, "w") as f:
        json.dump(all_data, f)

with open(ex_path, "r") as f:
    example = json.load(f)

dataset = GroundedScan(all_data["intransitive_verbs"], all_data["transitive_verbs"], all_data["adverbs"],
                       all_data["nouns"], all_data["color_adjectives"], all_data["size_adjectives"],
                       all_data["grid_size"], all_data["min_object_size"], all_data["max_object_size"],
                       type_grammar=all_data["type_grammar"], save_directory=output_directory,
                       percentage_train=0.9,#note hardcode
                       max_recursion=all_data["max_recursion"], sample_vocabulary='load')

save_dir = dataset.visualize_data_example(example)

#command = example["command"]
#meaning = example["meaning"]
#derivation = example["derivation"]
#situation = example["situation"]
#import pdb; pdb.set_trace()
#actual_target_commands = example["target_commands"]
#target_demonstration = example["target_demonstration"]
#mission = ' '.join(["Command:", ' '.join(command), "\nMeaning: ", ' '.join(meaning),
#                    "\nTarget:"] + actual_target_commands)
#save_dir = grounded_scan.visualize_command(situation, command, target_demonstration,
#                                           mission=mission)

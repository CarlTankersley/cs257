import csv
import re
from itertools import count, filterfalse

event_speaker_talk = {''}
talk_info = {''}
speaker_job = {''}
related_talks = {''}
ratings = {''}
counter = 0
id_dict = {}
id_set = set()
rating_dict = {}

with open('data/ted_main.csv') as original_data:
    reader = csv.DictReader(original_data)
    for row in reader:
        counter += 1
        if counter == 0:
            continue
        string_to_process = row['related_talks']
        regex_id = re.compile('\'id\': ([^,]*),')
        id_list = [int(id) for id in regex_id.findall(string_to_process)]
        regex_title = re.compile('\'title\': [\'\"](.+?)[\'\"],')
        title_list = [re.sub('^"+|"+$', '', re.sub('\\\\\\\'', "'", title))
                      for title in regex_title.findall(string_to_process)]
        for i in range(len(title_list)):
            if not title_list[i] in id_dict:
                id_dict[title_list[i]] = id_list[i]
                id_set.add(id_list[i])

        string_to_process = row['ratings']
        regex_reaction_id = re.compile('\'id\': ([^,]*),')
        reaction_id_list = [int(id)
                            for id in regex_reaction_id.findall(string_to_process)]
        regex_rating = re.compile('\'name\': ([^,]*),')
        rating_list = regex_rating.findall(string_to_process)
        for i in range(len(rating_list)):
            if not rating_list[i] in id_dict:
                rating_dict[rating_list[i]] = reaction_id_list[i]
                rating_dict[reaction_id_list[i]] = rating_list[i]


with open('data/ted_main.csv') as original_data:
    reader = csv.DictReader(original_data)
    for row in reader:
        title = re.sub('^"+|"+$', '', row['title'])
        if title in id_dict.keys():
            id = id_dict[title]
        else:
            id = next(filterfalse(id_set.__contains__, count(1)))
            id_dict[title] = id
            id_set.add(id)
        related_input = row['related_talks']
        regex_id = re.compile('\'id\': ([^,]*),')
        related_ids = (id, *[int(rid)
                       for rid in regex_id.findall(related_input)])

        rating_input = row['ratings']
        regex_reaction_id = re.compile('\'id\': ([^,]*),')
        reaction_id_list = [int(rid)
                            for rid in regex_reaction_id.findall(rating_input)]
        regex_num = re.compile('\'count\': ([^,]*)}')
        rating_list = [int(rid) for rid in regex_num.findall(rating_input)]

        rating_overall = []
        for i in range(round(len(rating_dict)/2)):
            if i in reaction_id_list:
                rating_overall.append(rating_list[reaction_id_list.index(i)])
            else:
                rating_overall.append(0)
        rating_overall = (id, *rating_overall)

        event_speaker_talk.add(
            (id, row['event'], row['main_speaker'], row['title']))
        talk_info.add((id, row['comments'], row['description'], row['duration'], row['film_date'], row['languages'],
                      row['name'], row['num_speaker'], row['published_date'], row['tags'], row['url'], row['views']))
        speaker_job.add((row['main_speaker'], row['speaker_occupation']))
        related_talks.add(related_ids)
        ratings.add(rating_overall)
        rating_dict = list(rating_dict)

import csv
import re
from itertools import count, filterfalse

event_speaker_talk = {''}  # contains talk_id, event, main_speaker, title
talk_info = {''}  # contains pretty much whatever
speaker_job = {''}  # contains speaker, occupation
related_talks = {''}  # contains talk_id, followed by 5 other talk_ids
# contains talk_id, followed by the number of each of the 15 possible ratings, in order
ratings = {''}
rating_link = {''}  # contains rating types and rating ids, going both ways
counter = 0
id_dict = {}
image_dict = {}
id_set = set()
rating_dict = {}

with open('data/ted_main.csv') as original_data:
    reader = csv.DictReader(original_data)
    regex_id = re.compile('\'id\': ([^,]*),')
    regex_title = re.compile('\'title\': [\'\"](.+?)[\'\"],')
    regex_image = re.compile('\'hero\': \'(.+?)\',')
    regex_reaction_id = re.compile('\'id\': ([^,]*),')
    regex_rating = re.compile('\'name\': ([^,]*),')
    for row in reader:
        string_to_process = row['related_talks']
        id_list = [int(id) for id in regex_id.findall(string_to_process)]
        image_list = [
            image for image in regex_image.findall(string_to_process)]
        title_list = [re.sub('^"+|"+$', '', re.sub('\\\\\\\'', "'", title))
                      for title in regex_title.findall(string_to_process)]
        for i in range(len(title_list)):
            if not title_list[i] in id_dict:
                id_dict[title_list[i]] = id_list[i]
                id_set.add(id_list[i])
                image_dict[title_list[i]] = image_list[i]

        string_to_process = row['ratings']
        reaction_id_list = [int(id)
                            for id in regex_reaction_id.findall(string_to_process)]
        rating_list = regex_rating.findall(string_to_process)
        for i in range(len(rating_list)):
            if not rating_list[i] in rating_dict:
                rating_dict[rating_list[i]] = reaction_id_list[i]
                rating_dict[reaction_id_list[i]] = rating_list[i]


with open('data/ted_main.csv') as original_data:
    reader = csv.DictReader(original_data)
    for row in reader:
        title = re.sub('^"+|"+$', '', row['title'])
        if title in id_dict.keys():
            id = id_dict[title]
            image = image_dict[title]
        else:
            id = next(filterfalse(id_set.__contains__, count(1)))
            image = "https://commons.wikimedia.org/wiki/File:Ted_Cruz,_official_portrait,_113th_Congress_(cropped_4).jpg"
            id_dict[title] = id
            id_set.add(id)
        related_input = row['related_talks']
        regex_id = re.compile('\'id\': ([^,]*),')
        related_list = [int(rid) for rid in regex_id.findall(related_input)]
        while(len(related_list) < 6):
            related_list.append(-1)
        related_ids = (id, *related_list)

        rating_input = row['ratings']
        regex_reaction_id = re.compile('\'id\': ([^,]*),')
        reaction_id_list = [int(rid)
                            for rid in regex_reaction_id.findall(rating_input)]
        regex_num = re.compile('\'count\': ([^,]*)}')
        rating_list = [int(rid) for rid in regex_num.findall(rating_input)]

        rating_overall = []
        for i in range(26):
            if i in reaction_id_list:
                rating_overall.append(rating_list[reaction_id_list.index(i)])
            else:
                rating_overall.append(0)
        rating_overall = (id, *rating_overall)

        event_speaker_talk.add(
            (id, row['event'], row['main_speaker'].strip(), row['title']))
        talk_info.add((id, row['comments'], row['description'], row['duration'], row['film_date'],
                      row['name'], row['num_speaker'], row['published_date'], row['tags'], row['url'], row['views'], image))
        speaker_job.add((row['main_speaker'].strip(),
                        row['speaker_occupation']))
        related_talks.add(related_ids)
        ratings.add(rating_overall)
        for i in rating_dict.keys():
            rating_link.add((i, rating_dict[i]))

with open('output/event_speaker_talk.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in event_speaker_talk:
        links.writerow(link)

with open('output/talk_info.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in talk_info:
        links.writerow(link)

with open('output/speaker_job.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in speaker_job:
        links.writerow(link)

with open('output/related_talks.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in related_talks:
        links.writerow(link)

with open('output/ratings.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in ratings:
        links.writerow(link)

with open('output/rating_link.csv', 'w') as output_file:
    links = csv.writer(output_file)
    for link in rating_link:
        links.writerow(link)

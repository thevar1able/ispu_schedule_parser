#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml
import lxml.html
import json
import sys

types = { "background:#FFFFCC": 0    #лекция
		, "background:#E5FFE5": 1 	 #семинар
		, "background:#FFEFFD": 2	 #лабораторная
		, "background:#FDE9D9": 3    #военная подготовка
		, "background:#D9FFFF": 4    #физкультура
		, "background:#FFFFFF": 5    #пусто
}

def event_generator(day, time, week, html_line):
	event = {}
	event_type = types[html_line.attrib['style']]
	event_text = html_line.text

	if event_type in [0, 1, 2, 4]:
		event['day'] = day
		event['time'] = time
		event['week'] = week
		event['type'] = event_type
		event['place'] = ""
		event['name'] = ""
		event['event'] = event_text.split()[0]
		if event_type != 4:
			event['place'] = event_text.split()[-1]
			event['name'] = " ".join(event_text.split()[-3:-1])
			event['event'] = " ".join(event_text.split()[:-3])
	return event

if __name__ == '__main__':
	parser = lxml.html.HTMLParser(encoding="utf-8")
	page = lxml.html.parse(sys.argv[1], parser)
	metadata = page.xpath("//select/option[@selected='selected']/text()")
	metadata_subgroup = page.xpath("//table[@id='ContentPlaceHolder1_rblSubGroup']//input")
	schedule = {'department': metadata[1]
			   , 'year': metadata[2]
			   , 'group': metadata[3]
			   , 'subgroup': 0 if "checked" in metadata_subgroup[0].values() else 1
			   , 'schedule': []
	}
	schedule_tables = page.xpath("//table[@id='sheduleTable']/tr")[2:16]

	for i, table in enumerate(schedule_tables):
		events = table.xpath('td')
		if i == 0 or i == 7: events = events[1:]
		for j, event in enumerate(events[1:]):
			x = event_generator(j, events[0].text, 1 if i < 7 else 2, event)
			if x != {}: schedule['schedule'].append(x)

	json_schedule = json.dumps(schedule, ensure_ascii=False)
	print(json_schedule)
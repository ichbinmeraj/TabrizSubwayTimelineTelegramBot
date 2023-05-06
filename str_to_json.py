import json

text = '''12:01
,12:17
,12:33
,12:49
,13:05
,13:21
,13:37
,13:53
,14:09
,14:25
,14:41
,14:57'''
clean_text = text.replace("\n", "")
my_list = clean_text.split(",")
my_list_str = json.dumps(my_list)
print(my_list_str)




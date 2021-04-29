from underthesea import ner

text = 'anh cần trợ giúp ngay lập tức'
chunked = ner(text)
print(chunked)

verbs = []
nouns = []
locations = []
person = []

current_loc = ''

for chunk in chunked:
    if chunk[1] == 'V':
        verbs.append(chunk[0])
    if chunk[1] == 'N':
        nouns.append(chunk[0])
    if 'LOC' in chunk[3]:
        if chunk[3] == 'B-LOC':
            if not len(current_loc):
                current_loc += f'{chunk[0]}'
            else:
                locations.append(current_loc)
                current_loc = ''
        else:
            current_loc += f' {chunk[0]}'
    if 'PER' in chunk[3]:
        person.append(chunk[0])

if len(current_loc):
    locations.append(current_loc)

print(verbs)
print(nouns)
print(locations)
print(person)

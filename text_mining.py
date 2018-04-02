#!/usr/local/bin/python
# coding: utf-8
import nltk
import wikipedia

text = None
with open('news.txt', 'r') as f:
    text = f.read()
sentences = nltk.sent_tokenize(text)
print(len(sentences))
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
ne_chunked = nltk.ne_chunk(tagged, binary=True)


def extractEntities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


nerEntity = extractEntities(ne_chunked)
# print(nltk.help.upenn_tagset())
# We want NNP, NNPS and JJ

nerCustom = []
for tagged_entry in tagged:
    if(tagged_entry[1].startswith("JJ") or tagged_entry[1].startswith("NNP")):
        nerCustom.append((tagged_entry))
print("nerEntity: %s" % len(nerEntity))
print("nerCustom: %s" % len(nerCustom))
# Determining top 10 Entities


def countTab(tuple, tagged):
    tab = []
    for value in tuple:
        counter = 0
        for tag in tagged:
            if(value[0] == tag[0]):
                counter += 1
        if((value[0], value[1], counter) not in tab):
            tab.append((value[0], value[1], counter))
    return tab


def countTabDict(list, tagged):
    tab = []
    for value in list:
        counter = 0
        for tag in tagged:
            if(value == tag[0]):
                counter += 1
        if((value, list[value], counter) not in tab):
            tab.append((value, list[value], counter))
    return tab


counterPOS = countTab(tagged, tagged)
counterTabEntity = countTabDict(nerEntity, tagged)
counterTabCustom = countTab(nerCustom, tagged)
counterPOS = sorted(counterPOS, key=lambda count: count[2],
                    reverse=True)[:10]
counterTabEntity = sorted(counterTabEntity, key=lambda count: count[2],
                          reverse=True)[:10]
counterTabCustom = sorted(counterTabCustom, key=lambda count: count[2],
                          reverse=True)[:10]
print(counterPOS)
print(counterTabEntity)
print(counterTabCustom)
fileWriting = open("result.txt", "w")
for tuple in counterPOS:
    line = ','.join('"'+str(x)+'"' for x in tuple)
    fileWriting.write('(' + line + '), ')
fileWriting.write("\n")
for tuple in counterTabEntity:
    line = ','.join('"'+str(x)+'"' for x in tuple)
    fileWriting.write('(' + line + '), ')
fileWriting.write("\n")
for tuple in counterTabCustom:
    line = ','.join('"'+str(x)+'"' for x in tuple)
    fileWriting.write('(' + line + '), ')

# results = wikipedia.search("Wikipedia")
# print(results)
name = "Google"
page = wikipedia.page(name)
# print(page.summary.encode('utf-8'))
pageSummary = page.summary
firstSentence = nltk.sent_tokenize(pageSummary)[0]
print(firstSentence.encode('utf-8'))
tokens = nltk.word_tokenize(firstSentence.encode('utf-8'))
tagged = nltk.pos_tag(tokens)
# print(tagged)
ne_chunked = nltk.ne_chunk(tagged, binary=False)
nerEntity = extractEntities(ne_chunked)
nerCustom = []
for tagged_entry in tagged:
    if(tagged_entry[1].startswith("JJ") or tagged_entry[1].startswith("NNP")):
        nerCustom.append(tagged_entry)
print(nerEntity)
print(nerCustom)
# Extracting the short description
pattern = []
trigger = False
for tagged_entry in tagged:
    if(tagged_entry[1].startswith("VBZ") or tagged_entry[1].startswith("VBD")):
        trigger = True
    if(trigger):
        if(tagged_entry[1].startswith("JJ") or
           tagged_entry[1].startswith("NN")):
            pattern.append(tagged_entry)
        if(tagged_entry[1].startswith("IN")
           or (tagged_entry[1].startswith("VBN") or
           tagged_entry[1].startswith("VBZ")
           or tagged_entry[1].startswith("VBD")) and len(pattern) != 0):
            print(tagged_entry[0])
            break
if(len(pattern) == 0):
    pattern.append(("Thing", "NN"))
# adding comma and blankspace
newPattern = []
for i in range(0, len(pattern)-1):
    newPattern.append(pattern[i])
    if("JJ" in pattern[i][1] and "JJ" in pattern[i+1][1]):
        newPattern.append((', ', ', '))
    if("NN" in pattern[i][1] and "JJ" in pattern[i+1][1]):
        newPattern.append((', ', ', '))
    if("JJ" in pattern[i][1] and "NN" in pattern[i+1][1]
       or "NN" in pattern[i][1] and "NN" in pattern[i+1][1]):
        if("NN" in pattern[i][1] and "NNP" in pattern[i+1][1]):
            newPattern.append(",")
        newPattern.append(" ")
newPattern.append(pattern[len(pattern)-1])
# Output
sentence = ""
for word in newPattern:
    sentence += word[0]
print(name + ": " + sentence)
print(newPattern)

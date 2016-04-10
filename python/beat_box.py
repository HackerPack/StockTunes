
from __future__ import division
import collections
import itertools
from random import choice
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
import midi_convert
from pydub import AudioSegment
import json


def read_file():
	data = open("sample.dat", "r").read()
	return convert_to_num(data.split())


def convert_to_num(lis):
	data = [int(float(x)) for x in lis]
	return data

def choice_if_list(item):
    if isinstance(item, collections.Iterable):
        return choice(item)
    else:
        return item

def change_range(val, oldMin, oldMax, newMin, newMax):
	oldRange = (oldMax - oldMin)
	newRange = (newMax - newMin)
	res = None
	if isinstance(val, list):
		res = [((((oldValue - oldMin) * newRange) / oldRange) + newMin) for oldValue in val]
	else:
		res = (((val - oldMin) * newRange) / oldRange) + newMin
	return res

def play_list(pitch_list, octave_list, duration,
              volume=120):
    result = NoteSeq()
    durl = [1/8, 1/8, 1/16, 1/16]
    cc = [choice([0,1,2,3,4,5,6,7,8,9,10,11]), choice([0,1,2,3,4,5,6,7,8,9,10,11]), choice([0,1,2,3,4,5,6,7,8,9,10,11]), choice([0,1,2,3,4,5,6,7,8,9,10,11])]
    st = 0
    for pitch in pitch_list:
        note1 = pitch
        note = cc[st%4]
        #octave = choice_if_list(octave_list)
        octave = change_range(note1, 0, 11, 1, 7)
        #dur = choice_if_list(duration)
        dur = durl[st%4]
        st += 1
        vol = choice_if_list(volume)
        result.append(Note(note, octave, dur, vol))
    return result

def gen_midi(filename, note_list):
    midi = Midi(tempo=120)
    midi.seq_notes(note_list)
    midi.write(filename)

SF2 = "soundfont/FarfisaGrandPiano_S1.sf2"
OUTPUT = "output"
INTER = "intermediate"

def generate(FILENAME, dt=None):
    octave = range(5, 7)
    gg = None
    if not dt:
    	gg = read_file()
    else:
    	gg = convert_to_num(dt)
    gg = change_range(gg, min(gg), max(gg), 0, 11)
    n1 = play_list(gg, octave, 1/8)
    midi_path = "midi/"+FILENAME+".mid"
    gen_midi(midi_path, n1)
    midi_convert.to_audio(SF2, midi_path, INTER)
    sound1 = AudioSegment.from_mp3(INTER+"/"+FILENAME+".wav")
    sound1 = sound1 + 15
    sound2 = AudioSegment.from_mp3("soundfont/beats.mp3")
    sound2 = sound2 - 10
    output = sound1.overlay(sound2, loop=True)
    output.export(OUTPUT+"/"+FILENAME+".mp3", format="mp3",tags={'artist': 'HackerPack', 'album': 'Stocks', 'comments': FILENAME +' stock data'})
    res = {"name": FILENAME, "data": dt}
    open("json/"+FILENAME+".json", "w").write(json.dumps(res))
    

if __name__ == "__main__":
    generate("yhoo")
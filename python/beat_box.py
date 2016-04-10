
from __future__ import division
import collections
import itertools
from random import choice
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
import midi_convert
from pydub import AudioSegment


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
    st = 0
    for pitch in pitch_list:
        note = pitch
        #octave = choice_if_list(octave_list)
        octave = change_range(note, 0, 11, 1, 7)
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

def generate(FILENAME, gg=None):
    octave = range(5, 7)
    if not gg:
    	gg = read_file()
    else:
    	gg = convert_to_num(gg)
    gg = change_range(gg, min(gg), max(gg), 0, 11)
    n1 = play_list(gg, octave, 1/8)
    midi_path = "midi/"+FILENAME+".mid"
    gen_midi(midi_path, n1)
    midi_convert.to_audio(SF2, midi_path, INTER)
    sound1 = AudioSegment.from_mp3(INTER+"/"+FILENAME+".wav")
    sound1 = sound1 + 10
    sound2 = AudioSegment.from_mp3("soundfont/beats.mp3")
    output = sound1.overlay(sound2, loop=True)
    output.export(OUTPUT+"/"+FILENAME+".mp3", format="mp3",tags={'artist': 'HackerPack', 'album': 'Stocks', 'comments': FILENAME +' stock data'})
    

if __name__ == "__main__":
    generate("yhoo")
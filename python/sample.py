
from __future__ import division
import collections
import itertools
from random import choice
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest


def flatten(iterable):
    return list(itertools.chain.from_iterable(iterable))


def fibonacci(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


# http://blog.yjl.im/2011/01/generating-pascals-triangle-using.html
def pascals_triangle(n):
    x = [1]
    yield x
    for i in range(n - 1):
        x = [sum(i) for i in zip([0] + x, x + [0])]
        yield x


def choice_if_list(item):
    if isinstance(item, collections.Iterable):
        return choice(item)
    else:
        return item


def random_notes(pitch_list, octave, duration,
                 number_of_notes, volume=120):
    result = NoteSeq()
    for x in range(0, number_of_notes):
        pitch = choice(pitch_list)
        octave = choice_if_list(octave)
        dur = choice_if_list(duration)
        vol = choice_if_list(volume)
        result.append(Note(pitch, octave, dur, vol))
    return result


def play_list(pitch_list, octave_list, duration,
              volume=120):
    result = NoteSeq()
    for pitch in pitch_list:
        note = pitch % 12
        octave = choice_if_list(octave_list)
        dur = choice_if_list(duration)
        vol = choice_if_list(volume)
        result.append(Note(note, octave, dur, vol))
    return result


def gen_midi(filename, note_list):
    midi = Midi(tempo=120)
    midi.seq_notes(note_list)
    midi.write("midi/" + filename)


def random1():
    chromatic = range(0, 12)
    durations = [1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1]
    notes1 = random_notes(chromatic,
                          range(0, 9),
                          durations,
                          100,
                          range(0, 128, 20))
    gen_midi("random1.mid", notes1)


def random2():
    chromatic = range(0, 12)
    notes2 = random_notes(chromatic,
                          range(3, 7),
                          [1/16, 1/8],
                          100)
    gen_midi("random2.mid", notes2)


def random3():
    pentatonic = [0, 2, 4, 7, 9]
    notes = random_notes(pentatonic,
                         range(5, 7),
                         1/16,
                         100)
    gen_midi("random3.mid", notes)


def random_fib():
    octave = range(5, 7)
    fib = fibonacci(100000000000)
    pascal = flatten(pascals_triangle(30))

    n1 = play_list(fib, octave, 1/16)
    n2 = play_list(pascal, 4, 1/16)
    n3 = play_list(pascal, octave, 1/16)

    gen_midi("fibonnacci.mid", n1)
    gen_midi("pascal.mid", n2)
    gen_midi("pascal_octaves.mid", n3)


if __name__ == "__main__":
    random1()
    random2()
    random3()
    random_fib()
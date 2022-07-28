#!/usr/bin/env python3

from .osc import dirt
import operator as opps


class ChainedMethods():

    def __init__(self):
        pass

    def addOrChange(self, names, values):

        if isinstance(values, (float, int)):
            values = [values]
        if isinstance(names, str):
            names = [names]

        for name, value in zip(names,values):
            if not self.query_existing_value(name):
                self.content = self.content + [name, value]
            else:
                self.change_existing_value(name, value)

    def amp(self, amount):
        self.addOrChange("amp", amount)
        return self

    def squiz(self, amount):
        self.addOrChange("squiz", amount)
        return self

    def sound(self, amount):
        self.addOrChange("sound", amount)
        return self

    def n(self, amount):
        self.addOrChange("n", amount)
        return self

    def accelerate(self, amount):
        self.addOrChange("accelerate", amount)
        return self

    def distort(self, amount):
        self.addOrChange("distort", amount)
        return self

    def comb(self, amount):
        self.addOrChange("comb", amount)
        return self

    def smear(self, amount):
        self.addOrChange("smear", amount)
        return self

    def room(self, amount):
        self.addOrChange("room", amount)
        return self

    def size(self, amount):
        self.addOrChange("size", amount)
        return self

    def dry(self, amount):
        self.addOrChange("dry", amount)
        return self

    def cut(self, amount):
        self.addOrChange("cut", amount)
        return self

    def ccn(self, amount):
        self.addOrChange("ccn", amount)
        return self

    def ccv(self, amount):
        self.addOrChange("ccv", amount)
        return self

    def portamento(self, amount):
        self.addOrChange("portamento", amount)
        return self

    def nudge(self, amount):
        self.addOrChange("nudge", amount)
        return self

    def loop(self, amount):
        self.addOrChange("loop", amount)
        return self

    def octer(self, amount):
        self.addOrChange("octer", amount)
        return self

    def octersub(self, amount):
        self.addOrChange("octersub", amount)
        return self

    def octersubsub(self, amount):
        self.addOrChange("octersubsub", amount)
        return self

    def ring(self, amount):
        self.addOrChange("ring", amount)
        return self

    def gain(self, amount):
        self.addOrChange("gain", amount)
        return self

    def krush(self, amount):
        self.addOrChange("krush", amount)
        return self

    def sDelay(self, xsdelay, tsdelay):
        self.content = self.content + ["xsdelay", xsdelay,
                                       "tsdelay", tsdelay]
        return self

    def ring(self, ring, ringf, ringdf):
        self.content = self.content + ["ring", ring,
                                       "ringf", ringdf,
                                       "ringdf", ringdf]
        return self

    def leslie(self, leslie=0.5, lrate=0.5, lsize=0.5):
        self.content = self.content + ["leslie", leslie,
                                       "lrate",  lrate,
                                       "lsize",  lsize]
        return self

    def tremolo(self, tremolorate, tremolodepth):
        self.content = self.content + ["tredp", tremolodepth,
                                       "tremr", tremolorate]
        return self

    def phaser(self, phaserrate, phaserdepth):
        self.content = self.content + ["phaserrate", phaserrate,
                                       "phasdp", phaserdepth]
        return self

    def vowel(self, vowel):
        if not isinstance(vowel, str):
            return self
        else:
            self.content = self.content + ["vowel", vowel]
            return self

    def hpf(self, cutoff=10000, resonance=0.1):
        self.content = self.content + ["cutoff", cutoff,
                                       "hpq", resonance]
        return self

    def bpf(self, cutoff=5000, resonance=0.5):
        self.content = self.content + ["bandf", cutoff,
                                       "bpq", resonance]
        return self

    def lpf(self, cutoff=2000, resonance=0.1):
        self.content = self.content + ["cutoff", cutoff, "resonance", resonance]
        return self

    def djf(self, djf):
        self.content = self.content + ["djf", djf]
        return self

    def adsr(self, attack=0.01, decay=0.5, sustain=0.2, release=0.5):
        self.content = self.content + ["attack", attack,
                                       "decay", decay,
                                       "sustain", sustain,
                                       "release", release]
        return self

    def n(self, number=0):
        """Change the number of the selected sample"""
        if isinstance(number, float): number = int(number)
        if not isinstance(number, (int, float, list)): return

        self.change_existing_value(
            "sound",
            self.query_existing_value("sound") + str(":{}".format(number)))

    def reverb(self, room, size, dry):
        self.content = self.content + ["room", room,
                                       "size", size,
                                       "dry",  dry]
        return self


class Sound(ChainedMethods):

    def __init__(self, sound, *args, **kwargs):

        # Default message when triggering soundfile/synth
        self.content = ["orbit", 0, "trig", 1, "sound", sound]

        # Searching through a large list of Monovalue Parameters.
        # If the parameter is found, we simply set it.
        for key, value in kwargs.items():


            if key in ["sound", "squiz", "cut", "ccn", "ccv", "portamento", "nudge",
                      "loop", "octer", "octersub", "octersubsub","ring",
                      "ringf", "ringdf", "accelerate", "gain", "midichan",
                      "djf", "orbit", "begin", "amp", "attack", "decay",
                      "sustain", "release", "fshift", "fshiftphase", "trig",
                      "fshifnote", "time", "delay", "delayfb",
                      "delaytime", "end", "pan", "distort", "krush", "kcutoff",
                      "freeze", "comb", "tredp", "tremr", "speed", "comb",
                      "smear", "real", "imag", "hbrick", "lbrick", "scram",
                      "triode", "shape", "binshift", "crush", "legato", "coarse",
                      "lrate", "lsize", "midinote", "room", "dry", "size", "enhance",
                      "vowel", "phaserrate", "phasdp", "cutoff", "hpq", "bpq",
                      "bandf"]:
                self.setorChangeMonoParam(key, value)
            # if the key isn’t found in the preceding list, there might be a method that
            # we can call (This method will add parameters to self.content).
            else:
                method = getattr(self, key, None)
                if callable(method):
                    method(value)

    def setorChangeMonoParam(self, key, value):
        """Will set a mono-parameter or change it if already in message """
        if key in self.content:
            self.content[self.content.index(key) + 1] = value
        else:
            for elem in [key, value]:
                self.content.append(elem)

        return self

    def query_existing_value(self, index):
        "Find the value associated to a name. Can return false if nothing is found."
        try:
            posIndex = self.content.index(index)
        except ValueError:
            return False
        return self.content[posIndex + 1]

    def change_existing_value(self, index, new_value):
        "Change the value associated to a name."
        try:
            valueIndex = self.content.index(index)
        except ValueError:
            return
        self.content[valueIndex + 1] = new_value

    def willPlay(self):
        """ Return a boolean that will tell if the pattern is sent to
            SuperCollider or if it will be discarded              """
        return True if self.query_existing_value("trig") == 1 else False

    def change(self, index, operator, factor):
        """
        This function can be used to change an existing value in the event:
        - index    : the name of the value you wish to change
        - operator : the mathemetical operator you need to use.
        - factor   : the value.
        FUN FACT: I never actually used it...
        """
        if operator not in ['+', '-', '/', '*']: return
        oldValue = self.query_existing_value(index)
        ops = {'+': opps.add, '-': opps.sub, '*': opps.mul,
               '/': opps.truediv, '=': opps.eq}
        self.change_existing_value(index, ops[operator](oldValue, factor))

    def out(self, output=0):
        """Must be able to deal with polyphonic messages """

        # It is now possible to specify the orbit in this function.
        if output != 0: self.change_existing_value("orbit", output)


        if self.willPlay():

            # Algorithm to detect sublists and handle polyphonic messages
            if any(isinstance(i, list) for i in self.content):
                nestedListsIndex = {} # we will build a dict of polyphonic key-values

                # Building a dictionary of polyphonic values
                for index, value in enumerate(self.content):
                    if isinstance(value, list):
                        nestedListsIndex[self.content[index - 1]] = value

                # Deleting polyphonic values from the current message. Avoiding the for loop.
                self.content = [e for e in self.content if e not in list(nestedListsIndex.keys())]
                self.content = [v for v in self.content if v not in list(nestedListsIndex.values())]

                # detecting the longest value in the dict
                maxLength = max((len(v) for v in nestedListsIndex.values()))
                keys = nestedListsIndex.keys()
                tailLists = []

                for i in range(maxLength):
                    void = []
                    for j in range(len(keys)):
                        void.append(list(keys)[j])
                        try:
                            void.append(nestedListsIndex[list(keys)[j]][i])
                        except IndexError:
                            void.append(None)

                    tailLists.append(void)


                for i in tailLists:
                    #print(self.content + i)
                    dirt(self.content + i)

            # Simple monophonic message need no care
            else:

                #print(self.content)
                dirt(self.content)

        else:
            return None

        def __str__(self):
            return str(self.content)

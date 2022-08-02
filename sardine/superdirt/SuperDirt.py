#!/usr/bin/env python3

from ..io.Osc import dirt
from ..superdirt.superdirt_parameters import params

def partial(func, /, *args, **keywords):
    """
    Specialized partial function taken directly from the Python
    documentation. This one is great because you can have access
    to __name__
    """
    def newfunc(*fargs, **fkeywords):
        newkeywords = {**keywords, **fkeywords}
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

class SuperDirt():

    def __init__(self, sound, **kwargs):

        # A long list of valid SuperDirt parameters
        self._mono_param_list = params
        # Default message when triggering soundfile/synth
        self.content = ["orbit", 0, "trig", 1, "sound", sound]

        # Iterating over kwargs. If we find the given kwargs in the list of
        # valid SuperDirt parameters, we add it to self.content
        for key, value in kwargs.items():
            if key in self._mono_param_list:
                self.setorChangeMonoParam(key, value)
            else:
                # Is there a method in this class that can handle it?
                method = getattr(self, key, None)
                if callable(method):
                    # calling the given method with the given value
                    method(value)

        self.generate_chainable_methods(params)

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def generic_mapper(self, amount, name: str):
        self.addOrChange(name, amount)
        return self

    def generate_chainable_methods(self, params: list):
        for param in params:
            setattr(self, param, partial(self.generic_mapper, name=param))

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

    def setorChangeMonoParam(self, key, value):
        """Will set a mono-parameter or change it if already in message """
        if key in self.content:
            self.content[self.content.index(key) + 1] = value
        else:
            for elem in [key, value]:
                self.content.append(elem)

        return self

    def query_existing_value(self, index):
        "Find the value associated to a name. Return false if not found."
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
        """
        Return a boolean that will tell if the pattern is planned to be sent
        to SuperDirt or if it will be discarded.
        """
        return True if self.query_existing_value("trig") == 1 else False

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


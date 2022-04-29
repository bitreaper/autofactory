"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright (c) 2019-2022 Todd LaWall, aka Bitreaper
"""

import abc
import inspect


class ModelBase(object, metaclass=abc.ABCMeta):
    modelStrings = None

    @classmethod
    def findModel(cls, observedModel, returnBase=False, returnLatest=False):
        """
        This class looks down the inheritance chain for a class that has a string that matches
        observedModel in it's modelStrings list.  It can traverse an inheritance tree.  Make sure
        that you understand that if you have more than one subclass that has the same model string,
        this will return the first one it finds as it traverses depth first in it's subclasses list.
        Much like the MRO and how super() works, this is a depth first search rather than breadth, so
        make sure that your model strings are unique.
        """

        def traverse(searchMe, soughtModel):
            if soughtModel in searchMe.modelStrings:
                return searchMe
            else:
                for sub in searchMe.__subclasses__():
                    possible = traverse(sub, soughtModel)
                    if possible:
                        return possible
                return None

        if not inspect.isclass(cls):
            cls = cls.__class__

        if observedModel in cls.modelStrings:
            return cls
        else:
            # traverse...
            if len(cls.__subclasses__()) >= 1:
                possible = traverse(cls, observedModel)

                if possible:
                    return possible
                else:
                    # if we got here, we fell of the end of the list.  Time to raise a not implemented error.
                    # an alternative here is to return the base (not ModelBase, but the base (like AcuityBase)
                    # rather than die, so that as a default you will have some functionality.
                    if returnBase:
                        print("Didn't find model, defaulting to base")
                        return cls
                    else:
                        raise NotImplementedError(
                            f"Model {observedModel} is not found in the inheritance chain. Hit bottom at "
                            f"{cls.__name__}.  Please check that a model object for this is created."
                        )

            elif cls.__subclasses__() == []:
                # if it's the empty list, we've hit bottom without matching the model string.  Throw a not implemented error,
                # unless we've been told to return the default base class functionality.  This allows for verison-class-chains
                # that still want to return a default.
                if returnBase or returnLatest:
                    print("No subclasses, fell off end.  Using default base")
                    return cls
                else:
                    raise NotImplementedError(
                        f"Model {observedModel} is not found in the inheritance chain. Hit bottom at "
                        f"{cls.__name__}.  Please check that a model object for this is created."
                    )

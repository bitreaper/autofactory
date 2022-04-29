"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright (c) 2019-2022 Todd LaWall, aka Bitreaper
"""

import inspect


class VersionedBase(object):

    """
    VersionedBase - This class is functionality that is mixed in to a class so that it can have subclasses
    that form a version series.  It gives the programmer one anchor point to call on and ask for a version
    that matches the string handed in.  It is meant to make factory methods that much simpler, by asking the
    base class to find a version of itself that can be returned to match instead of having to do an if tree
    case statement.
    """

    versionString = None

    @classmethod
    def newFromVersion(
        cls, *args, version=None, returnDefault=False, returnLast=False, **kwargs
    ):
        """

        The idea is that a class series that forms a version chain inherits at it's base from this class,
        then each class from that point down is a versioned child.  Then this base provides the machinnery
        to look down the inheritance chain for a version that matches the version string handed in.

        version is a string.  It must be something that the implementing base can use to compare to all the subclasses
        for their versionString.  This is how a versioned child is found.

        returnDefault means that you can return the base class's implementation. This is useful if you have
        a set of versions before the base class that the base can take care of, and you start differentiating
        behavior in the children of the base.

        returnLast means that you can return the last class's implementation. This is useful if you want to return
        the latest functionality if you don't have a version string that matches.

        """
        if cls.versionString == version:
            return cls(*args, **kwargs)
        else:
            if len(cls.__subclasses__()) == 1:
                scan = cls.__subclasses__()[0]
                while scan:
                    if scan.versionString == version:
                        # print(f"Found version {version}, returning one")
                        return scan(*args, **kwargs)

                    if len(scan.__subclasses__()) == 1:
                        scan = scan.__subclasses__()[0]
                    else:
                        # if we got here, we fell of the end of the list.  Time to raise a not implemented error.
                        # an alternative here is to return the base (not versioned base, but the base (like AcuityBase)
                        # rather than die, so that as a default you will have some functionality.
                        if returnDefault:
                            # print("Didn't find version, defaulting to base")
                            return cls(*args, **kwargs)
                        elif returnLast:
                            # print("Didn't find version, returning last one in the chain")
                            return scan(*args, **kwargs)
                        else:
                            raise NotImplementedError(
                                f"Version {version} is not found in the inheritance chain. Hit bottom at "
                                f"{scan.__name__}.  Please check that a versioned object for this is created."
                            )

            elif cls.__subclasses__() == []:
                # if it's the empty list, we've hit bottom without matching the version string.  Throw a not implemented error,
                # unless we've been told to return the base class or return the latest class.  This allows for
                # verison-class-chains that still want to return a default.
                if returnDefault:
                    # print("No subclasses, fell off end.  Using default base")
                    return cls(*args, **kwargs)
                elif returnLast:
                    return cls(*args, **kwargs)
                else:
                    raise NotImplementedError(
                        f"Version {version} is not found in the inheritance chain. Hit bottom at "
                        f"{cls.__name__}.  Please check that a versioned object for this is created."
                    )
            else:
                # we don't traverse if we are branched in our children.  This is for a single line lineage only,
                # so we need to return an exception here because you did something you shouldn't have done.  VersionedBase
                # can have multiple children, but none of the children can have anything more than one.  Otherwise, how do
                # we know which of the multiples to create?  I suppose we could do a breadth first search of the children,
                # but then we're going to need some more complicated logic to handle a tree and not a chain.
                raise TypeError(
                    "You are trying to call newFromVersion on a class with more"
                    " than 1 subclass.  Too ambiguous, quitting"
                )

    @classmethod
    def findVersion(cls, version, returnBase=False, returnLatest=False):
        """
        This function returns the class itself, rather than an instance of it.  This is used to find the right class
        based on the version string handed in.  This traverses a tree, so it is not limited to a single line of inheritance,
        however, it may not find the right one if you have two classes that share the same version string.  Of course, you
        shouldn't do that in the first place...

        This function doesn't have returnLatest working yet.

        """

        def traverse(searchMe, soughtVersion):
            if soughtVersion == searchMe.versionString:
                return searchMe
            else:
                if len(searchMe.__subclasses__()) > 0:
                    sub = searchMe.__subclasses__()[0]
                    possible = traverse(sub, soughtVersion)
                    return possible
                elif returnLatest:
                    return searchMe
                else:
                    return None

        # this way we can call this on an instance and it will use it for the class
        if not inspect.isclass(cls):
            cls = cls.__class__

        if version == cls.versionString:
            return cls
        else:
            # traverse...
            if len(cls.__subclasses__()) > 0:
                possible = traverse(cls, version)
                if possible:
                    return possible
                else:
                    # if we got here, we fell of the end of the list.  Time to raise a not implemented error.
                    # an alternative here is to return the base (not ModelBase, but the base (like AcuityBase)
                    # rather than die, so that as a default you will have some functionality.
                    if returnBase:
                        # print("Didn't find model, defaulting to base")
                        return cls
                    else:
                        raise NotImplementedError(
                            f"Version {version} is not found in the inheritance chain. Hit bottom at "
                            f"{cls.__name__}.  Please check that a version object for this is created."
                        )
            else:
                # if it's the empty list, we've hit bottom without matching the model string.  Throw a not implemented error,
                # unless we've been told to return the default base class functionality.  This allows for verison-class-chains
                # that still want to return a default.
                if returnBase or returnLatest:
                    return cls
                else:
                    raise NotImplementedError(
                        f"Version {version} is not found as the version for this class, and there are no subclasses"
                        f"of {cls.__name__} to search.  Please check that a version object for this is created."
                    )

    # This is if you have a class, and need to instantiate one of it's previous versions in case an interface rolled back
    # or some case where you need to downgrade an interface.
    @classmethod
    def findPreviousVersion(cls, previous):
        def climb(base, soughtVersion):
            print(f"Climbing {cls}")

            if base.versionString == soughtVersion:
                return base
            else:
                parent = base.__base__
                if hasattr(parent, "versionString"):
                    return climb(parent, soughtVersion)
                else:
                    print(
                        f"Hit the top of the chain without finding version {soughtVersion}"
                    )

        if not inspect.isclass(cls):
            cls = cls.__class__

        if hasattr(cls.__base__, "versionString"):
            return climb(cls.__base__, previous)

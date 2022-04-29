# autofactory
A python mixin library that allows you to search for an object in a heirarchy based on a tag or version, without needing to create a factory constructor to handle that.

This project was developed out of the need to reduce the maintenance of factory 
functions.  When adding a new version of software being tested, I wanted the 
interface objects that I used to be able to handle those new versions without
having to maintain a factory constructor function.  All I needed to do was add
a child object with the new version for it's version string, and add any overrides
to the interface's methods.  This also had the benefit of keeping the changes
to the interface over time clear.


To use VersionedBase, simply inherit from it.  To find a child version, call 
`findVersion()` on the base class type.  This also can be used to walk 
the parent classes with `findPreviousVersion()`, which can be useful
in the instance where an interface is downgraded and you need to instantiate
a previous version of it.  Being that an object will be an abstraction that
mutates over time, VersionedObject will only work if the inheritance is linear,
that is, no more than one child class per version in the chain.

ModelBase operates much the same, except it traverses the tree, rather than requiring
the inheritance structure to look linear.  This was used for device abstractions,
which usually contained interface objects (which were usually VersionedObjects).

Think of a scenario where you would be testing cell phones.  ModelBase would allow
you to search through the `Phone` class hierarchy looking for the model that you
got when you queried the phone.  Inside the class that was returned would be 
interface objects that are instantiated based on the version of software on the
phone.



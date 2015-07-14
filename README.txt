resolve_id


Usage:
	
python resolve_id.py <anonymous identifier> <database filename>

-compiles with Python 3.4
-requires tokyo-python wrapper of tokyocabinet library
	http://pythonhosted.org/tokyo-python/index.html


Design:

I think of the database as being a collection of linked-lists,
where each key points to its parent, and the last node is the
internal identifier.

Since this exercise was described as a starting point for discussion,
I coded two functions for resolving an identifier.  

find_internal_id(identifier,db)
	uses a while loop to search for an internal identifier.  
	This should be sufficient, because in this particular case 
	we don't need to return/yield the intermediate nodes 
	between the input identifier and the internal identifier.

parent_generator(identifier,db) (called by resolve())
	is a generator that, when next() is called, yields the parent
	of the current node.  For generality, the generator raises 
	StopIteration when an internal identifier is found.  However, 
	the checking for an internal identifier is duplicated by the 
	caller because I couldn't think of a (clean) way to retrieve 
	the last value yielded by a generator (this behavior is out 
	of the scope  of a generator).  So after I call next(), I 
	check to see whether the yielded identifier is prefixed 
	with 'i' or 'n'.

This would generally call for a Strategy Pattern, but since the handling 
of find_internal_id can be done in one line, I just kept it simple.

Unless there were other use cases I'm not aware of, I would use
find_internal_id() in practice, because we care less about traversing
the linked-list-like set of identifiers and only want to resolve
the id to an internal one.

parent_generator() is called by resolve().  find_internal_id() is called
directly by main().


Tests:

I test four cases:
	1) simple call to find_internal_id()
	2) call to find_internal_id() on a 'dead-end' id
	3) simple call to resolve()
	4) call to resolve() on a 'dead-end' id

A 'dead-end' identifier is one that is present in the database, but does not
resolve to an internal identifier.

The test class implements setUp(), tearDown(), setUpClass(), and tearDownClass().

setUp() and tearDown() are called by each instance and open a connection
to the db.

setUpClass() and tearDownClass() handle inserting the test key-value pair
at the start, and removing that value when finished.

I ran into an issue where tearDown() doesn't seem to be called appropriately,
because I get a warning that 'people.db' is still open at termination.  I
have no problem closing the db from the Python command line, so I wonder
if I've done something incorrectly in my use of tearDown().

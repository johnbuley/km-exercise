import sys,os
from tokyo.dbm import *



def find_internal_id(identifier,db):
    """ Simple function searches for internal ancestor of input identifier

    No guarantee of termination, dependant on database.

    Args:
        identifier (bytes): anonymous identifier
        db (tokyo.dbm.TCBDB): Tokyo Cabinet B+ Tree database (dict-like)

    Returns:
        int: internal identifier

    """
    
    # Find parent of input identifier
    try:
        identifier = db[identifier]
    except:
        sys.exit('Key {0} not found'.format(identifier))
    
    # Loop until an internal identifier is found
    while chr(identifier[0]) != 'i':
        try:
            identifier = db[identifier[1:]]
        except:
            sys.exit('Key {0} not found'.format(identifier))

    # Convert bytes result to int
    try:
        return int.from_bytes(identifier[1:],byteorder='little',signed=False)
    except:
        sys.exit('Cannot convert internal identifier {0} to int'.format(identifier[1:]))



def parent_generator(identifier,db):
    """ Generator that iterates through ancestors of identifier in id tree

    Args:
        identifier (bytes): anonymous identifier
        db (tokyo.dbm.TCBDB): Tokyo Cabinet B+ Tree database (dict-like)

    Yields:
        bytes: anonymous or internal identifier with 'n' or 'i' prefix

    """


    try:
        identifier = db[identifier]
    except:
        sys.exit('Key {0} not found'.format(identifier))

    # Reversed order of while loop because input lacks prefix,
    # whereas yielded identifiers need to include prefix.
    while(True):
        yield identifier
        if chr(identifier[0]) == 'i':
            raise StopIteration
        try:
            identifier = db[identifier[1:]]
        except:
            sys.exit('Key {0} not found'.format(identifier))



def resolve(identifier,db):
    """ Attempts to resolve an anonymous identifier to an internal identifier

    Args:
        identifier (bytes): anonymous identifier
        db (tokyo.dbm.TCBDB): Tokyo Cabinet B+ Tree database (dict-like)

    Returns:
        int: internal identifier

    """


    # Check that identifier to be resolved is valid (is present in db)
    if identifier not in db:
        sys.exit('Invalid input identifier: not found')

    parent_gen = parent_generator(identifier,db)

    try:
        # No guarantee of while loop termination, dependent on database
        parent = next(parent_gen)
        while chr(parent[0]) != 'i':
            parent = next(parent_gen)
    except:
        # It would be possible that the try fails before parent is initialized, but that
        # should be caught by the identifier validation above
        sys.exit('Unable to find internal identifier.\nLast found value: {0}'.format(parent))

    # Convert bytes result to int
    try:
        return int.from_bytes(parent[1:],byteorder='little',signed=False)
    except:
        sys.exit('Internal identifier cannot be converted to int')



def main(identifier,db_filename):

    # Open Tokyo Cabinet
    try:
        db = open(db_filename)
    except Exception as e:
        sys.exit(e)

    # Resolve identifier with resolve(), print result
    print('Internal identifier (fcn: resolve): {0}'.format(resolve(identifier,db)))

    # Additional test of find_internal_id()
    print('Internal identifier (fcn: find_internal_id): {0}'.format(
        find_internal_id(identifier,db),byteorder='little',signed=False))


if __name__ == '__main__':

    # Convert input identifier to bytestring.
    # Shouldn't fail through command-line use, but used 
    # try/except in case there is an issue with a strange encoding.
    try:
        identifier = bytes(sys.argv[1],encoding='utf-8')
    except: 
        sys.exit('Invalid string')

    # Check that input db file exists
    if os.path.isfile(sys.argv[2]):
        db_filename = sys.argv[2]
    else: 
        sys.exit('File does not exist')

    main(identifier,db_filename)

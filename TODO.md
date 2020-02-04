# Shard (class)

    - conceptualize the object
    - add cmd building method
    - __init__ exception handling, send args 
        -> DedicatedServer 'try' initialize shard call, send args
            -> ServerControl.select_server 'try' initialize DedicatedServer call, send args
                -> ServerControl.error_dialog, spawns dialog indicating issue from arg chain

# Configuration (class and subclasses)

    - see https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/

# Utility (module)

    - univeral, app-tailored helper functions

# Tests

    - dunno, unittest?
from netstorage.baseservice import Binding

AKAMAI_NETSTORAGE_ACCOUNT = ''
AKAMAI_NETSTORAGE_KEY = ''
AKAMAI_NETSTORAGE_KEY_NAME = ''
AKAMAI_NETSTORAGE_CP_CODE = None

# Which methods (keys) to call and what kwargs to pass to each method (values)
METHODS = {
    'du': {'path': 'some/path/to/test', },
    'dir': {'path': 'some/other/path/to/test', },
}

# How many times to iterate
ITERATIONS = 1000000

bind = Binding(
    AKAMAI_NETSTORAGE_ACCOUNT,
    AKAMAI_NETSTORAGE_KEY,
    AKAMAI_NETSTORAGE_KEY_NAME,
    AKAMAI_NETSTORAGE_CP_CODE,
)

for method_name, kwargs in METHODS.items():
    print '>>> Now testing: Binding.{method}({kwargs}): {repeat} iterations'.format(
        method=method_name,
        repeat=ITERATIONS,
        kwargs=kwargs,
    )

    try:
        for iteration in xrange(ITERATIONS):
            getattr(bind, method_name)(**kwargs)
    except KeyboardInterrupt:
        pass
    except Exception, e:
        _locals = locals()
        print 'Method: "{method_name}"'.format(**_locals)
        print 'Arguments: "{kwargs}"'.format(**_locals)
        print 'Iteration: "{iteration}"'.format(**_locals)
        print 'Exception: {exception_class}, arguments: {exception_arguments}'.format(
            exception_class=e.__class__,
            exception_arguments=e.args,
        )

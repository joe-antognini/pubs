msg_list = {}

def listen(EventClass):
    def wrap(f):
        if isinstance(EventClass, type) \
                and issubclass(EventClass, Event) \
                and EventClass != Event:

            if not EventClass.__name__ in msg_list:
                msg_list[EventClass.__name__] = []
            msg_list[EventClass.__name__].append(f)
            # next step allow us to call the function itself without Event raised
            def wrapped_f(*args):
                f(*args)
            return wrapped_f
        else:
            raise IOError('{} is not an Event subclass'.format(EventClass))
    return wrap


class Event(object):
    def __init__(self, string):
        """This is an example of simple event that can be raised
        Inherit from this class and redefine whatever you need,
        except the send funtion
        """
        self.string = string

    def send(self):
        """ This function send the instance of the class, i.e. the event to be sent,
        to all function that listen to it
        """
        if self.__class__.__name__ in msg_list:
            for f in msg_list[self.__class__.__name__]:
                f(self)

if __name__ == "__main__":

    class TestEvent(Event):
        def print_one(self):
            print 'one'

    @listen(TestEvent)
    def Display(TestEventInstance):
        print TestEventInstance.string

    @listen(TestEvent)
    def Helloword(TestEventInstance):
        print 'Helloword'

    @listen(TestEvent)
    def PrintIt(TestEventInstance):
        TestEventInstance.print_one()

    class AddEvent(Event):
        def __init__(self):
            pass

        def add(self, a, b):
            return a + b

    @listen(AddEvent)
    def DoIt(AddEventInstance):
        print AddEventInstance.add(17, 25)

    # using the callback system
    myevent = TestEvent('abcdefghijklmnopqrstuvwxyz')
    myevent.send()  # this one call three function

    addevent = AddEvent()
    addevent.send()

    # but also work without the event raising system!
    Display(myevent)
    Helloword(myevent)
    PrintIt(myevent)
    DoIt(addevent)

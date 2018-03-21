
import threading
import time

# Define a function for the thread

thread_signal = True


def wait_for_other_thread():
    """Thread needs a function to call 
    in this example the thread executing this
    function simply waits for the global variable
    to change value. Which is done by the other thread"""
    while thread_signal == True:
        print("still no signal at {}\n".format(time.ctime(time.time())))
        time.sleep(0.1)


def send_signal():
    """ global keywords is necessary to change a variable
    outside of this functions namespace"""
    global thread_signal
    print("sender is sending")
    time.sleep(1)
    print("waiting is over")
    thread_signal = False


# keyword target is necessary, since many more arguments could be given
# target is set to callable object
t1 = threading.Thread(target=wait_for_other_thread)
t2 = threading.Thread(target=send_signal)

# Thread.start() forces the object to execute its target()
t1.start()
t2.start()

# join() waits for the thread to finish
t1.join()
t2.join()

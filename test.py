import web
import time
import serial
import thread

urls = (
    "/", "index",
    "/pulse", "pulse",
    "/.*", "redirect_to_index"
)

# establish a shared storage bucket
bucket = web.storage({"BPM": 84, "SPO2":1.5})

def add_global_hook():
    global bucket
    # when a request comes in, the call to add_processor calls the wrapper 
    # we'll define below, to do whatever needs to be done before the call to
    # what he WOULD have done goes off (the original function is passed in as
    # handler, which we get the responsibility of calling. Essentially we get
    # to inject the exposure of the global state bucket into web.py's request
    # handling logic. 
    #
    # Note that this will NOT work if there's not a single python process
    # hosting the script. For your scenario it should work fine.
    def _wrapper(handler):
        web.ctx.globals = bucket
        return handler()
    return _wrapper

class index:
    def GET(self):
        render = web.template.render('templates')
        return render.index()
        
def serialRead():
    global bucket
    s = serial.Serial(port='/dev/tty.usbmodem187', baudrate=57600)
    while 1:
        line = s.readline()
        if line.startswith('1'):
            mySplit = line.split()
            print mySplit
            bucket.BPM = mySplit[2]
            bucket.SPO2 = mySplit[4]

class pulse:
    def GET(self):
        localTp = web.ctx.globals.BPM, web.ctx.globals.SPO2
        jsonString = '{"val1":"%s","val2":"%s"}'%localTp
        print jsonString
        return jsonString

class redirect_to_index:
    def GET(self):
        raise web.seeother("/")

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.add_processor(add_global_hook())
    thread.start_new_thread(serialRead, ())
    app.run()


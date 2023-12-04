from config import connect, get_ip
from microdot_asyncio import Microdot
import logger
import storage

try:
    #Bootstrap
    connect()
    import ntptime
    ntptime.settime()
    
    app = Microdot()

    #App Routes
    @app.route('/status')
    async def status(request):
        return {
            "logs": logger.read_all(),
            "state": storage.load()
        }
    
    try:
        logger.log("Started via IP " + get_ip())
        app.run()
    except KeyboardInterrupt:
        print("Shutdown requested...")
        app.shutdown()    
    
except Exception as err:
    logger.log("ERROR: Booting failed" + str(err))


    
print("Shutdown finished")
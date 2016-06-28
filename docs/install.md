# Installation Instructions

## Installing on CPython 3

Although micropython-microqueue is designed to function with 
micropython, it is supported on most python 3 interpreters.   
Use pip to install on Python3 or PyPy3.

    $ pip install micropython-microqueue
    
## Installing on micropython

The installation process differs depending on the version of 
micropython being used.  However the **upip** module is used to do the 
installation from the Python package repositories.

### Installing on micropython unix

Use the micropython **upip** module to install on micropython.  

    $ micropython -m upip install micropython-microqueue

### Installing on micropython on the esp8266

To install on micropython embedded platforms:

#### Step 1. Change into the esp8266 build directory

    $ cd esp8266

#### Step 2. Use upip to install the module into the scripts directory.

Set the MICROPYPATH environment variable to point to the scripts 
directory.  

    $ MICROPYPATH=scripts;micropython -m upip install micropython-microqueue

#### Step 3. Deploy the module to the esp8266.  

    $ make deploy

## Example, of installing on ESP8266

Install using the upip module into the esp8266 scripts directory

    $ MICROPYPATH=scripts;micropython -m upip install micropython-microqueue
    Installing to: scripts/
    Warning: pypi.python.org SSL certificate is not validated
    Installing micropython-microqueue 0.0.6 from https://pypi.python.org/packages/07/55/c8cb5881a86906da5c3a5bae328cc537e127f760a57c50ba1062a7bebd1c/micropython-microqueue-0.0.6.tar.gz
    Created scripts/microqueue/
    Installing micropython-redis.list 0.0.57 from https://pypi.python.org/packages/4d/71/b12f84002e4d35ce9c66b14d82ef35b900c7a32389eea32661e9e0abad37/micropython-redis.list-0.0.57.tar.gz
    Created scripts/uredis_modular/
    Installing micropython-redis.client 0.0.57 from https://pypi.python.org/packages/5a/b6/641f3f47f8ef6997c37e0fa4499f25ef9d9088a409f71bba1c8031f2b3e2/micropython-redis.client-0.0.57.tar.gz
    Installing micropython-redis-modular 0.0.57 from https://pypi.python.org/packages/0a/68/1424002583bc72e29573f5ccf30a45d6c265ec0435d33999f728f277caa5/micropython-redis-modular-0.0.57.tar.gz

Deploy to the esp8266

    $ make PORT=/dev/ttyUSB0 deploy
    Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
    Generating build/frozen.c
    Generating build/genhdr/mpversion.h
    GEN build/genhdr/qstr.i.last
    GEN build/genhdr/qstr.split
    GEN build/genhdr/qstrdefs.collected.h
    QSTR not updated
    CC ../py/modsys.c
    CC moduos.c
    CC build/frozen.c
    CC ../lib/utils/pyexec.c
    LINK build/firmware.elf
       text    data     bss     dec     hex filename
     527580    1044   56216  584840   8ec88 build/firmware.elf
    Create build/firmware-combined.bin
    esptool.py v1.2-dev
    ('flash    ', 34992)
    ('padding  ', 1872)
    ('irom0text', 493672)
    ('total    ', 530536)
    Writing build/firmware-combined.bin to the board
    esptool.py v1.2-dev
    Connecting...
    Running Cesanta flasher stub...
    Flash params set to 0x0020
    Writing 532480 @ 0x0... 532480 (100 %)
    Wrote 532480 bytes at 0x0 in 46.2 seconds (92.2 kbit/s)...
    Leaving...
    Verifying just-written flash...
    Verifying 0x81868 (530536) bytes @ 0x00000000 in flash against build/firmware-combined.bin...
    -- verify OK (digest matched)
    #@esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=8m 0 build/firmware.elf-0x00000.bin 0x9000 build/firmware.elf-0x0[1-f]000.bin
    $ 

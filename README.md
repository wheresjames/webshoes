
# webshoes

Quickly create a web service supporting both websockets and http.

``` Python

    import webshoes as ws

    def cmdAdd(ctx, q):
        return {'result': int(q.a) + int(q.b)}

    wsa = ws.WebShoesApp('127.0.0.1', 15801, {'verbose': True})
    wsa.register('cmd', 'cmd', 'args', 'event', 'reply', {
            'add': cmdAdd
        })
    wsa.start()

```

---------------------------------------------------------------------
## Table of contents

* [Install](#install)
* [Examples](#examples)
* [References](#references)

&nbsp;

---------------------------------------------------------------------
## Install

    $ pip3 install webshoes

&nbsp;


---------------------------------------------------------------------
## Examples

``` Python

    # Test function
    def cmdAdd(ctx, q):
        return {'result': int(q.a) + int(q.b)}

    # Create the server
    import webshoes as ws
    wsa = ws.WebShoesApp('127.0.0.1', 15801, {'verbose': True})

    # Register the callback function
    #             ----------------------------------> The root for http requests
    #             |      ---------------------------> The variable in websocket request
    #             |      |                              containing the command name
    #             |      |      --------------------> The variable in websocket request
    #             |      |      |                       containing the function arguments
    #             |      |      |       ------------> The variable in websocket request
    #             |      |      |       |               containing the event name
    #             |      |      |       |        ---> Variable in reply to put return data
    #             |      |      |       |        |
    wsa.register('cmd', 'cmd', 'args', 'event', 'reply', {
            'add': cmdAdd
        })

    # Start the server
    wsa.start()


    # Call add function with http request
    import requests
    reply = requests.get('http://127.0.0.1:15801/cmd/add?a=2&b=3')
    Log(reply.text)


    # Call the add function with websockets
    import websockets
    async with websockets.connect('ws://127.0.0.1:15801') as wsc:
        await wsc.send(json.dumps({'cmd':'add', 'args':{'a':2, 'b':3}}))
        reply = await wsc.recv()
        Log(reply)

    # Stop the server
    wsa.stop()

```

&nbsp;


---------------------------------------------------------------------
## References

- Python
    - https://www.python.org/

- pip
    - https://pip.pypa.io/en/stable/


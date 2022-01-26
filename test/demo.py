#!/usr/bin/env python3

import json
import asyncio

Log = print


async def run():

    # Test function
    def cmdAdd(ctx, q):
        return {'result': int(q.a) + int(q.b)}

    # Create the server
    import webshoes as ws
    wsa = ws.WebShoesApp('127.0.0.1', 15801, {'verbose': True})

    # Register the callback function
    #             ----------------------------------> The root for http requests
    #             |      ---------------------------> The variable in websocket requests
    #             |      |                              containing the command name
    #             |      |      --------------------> The variable in websocket requests
    #             |      |      |                       containing the function arguments
    #             |      |      |       ------------> The variable in websocket requests
    #             |      |      |       |               containing the event name
    #             |      |      |       |        ---> Variable in replys to put return data
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

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run())


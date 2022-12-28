#!/usr/bin/env python3

import os
import json
import random
import asyncio
import propertybag as pb
import webshoes

try:
    import sparen
    Log = sparen.log
except:
    Log = print

#-------------------------------------------------------------------
# API

async def getMatrix(ctx, q):
    return {'m': ctx.opts.m}

async def incMatrix(ctx, q):

    if not q.exists('x') or not q.exists('y'):
        raise Exception(f'Invalid parameters: {q}')

    o = ctx.opts

    a = int(q.y) * o.w + int(q.x)
    v = int(o.m[a]) + 1
    if 9 < v:
        v = 0
    o.m = o.m[:a] + str(v) + o.m[a+1:]

    ctx.wsa.triggerEvent('matrixUpdate', {'m': o.m})

    return {'m': o.m}


#-------------------------------------------------------------------
# Server

async def run():

    addr = '127.0.0.1'
    port = 12909

    # Web server
    opts = pb.Bag({'run': True, 'verbose': True})

    # Unique id
    opts.iid = ''.join(random.choice('1324567890ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32))

    # Api variables
    opts.w = 10
    opts.h = 10
    opts.m = (opts.w * opts.h) * '0'

    # Create webshoes app
    wsa = webshoes.WebShoesApp(addr, port, opts)

    # Make Webshoes js available
    wsa.register('webshoes', 'cmd', 'q', 'evt', 'r', {
            '*'    : {'root':webshoes.libPath('web')}
        })

    # Make site html available
    Log(os.path.join(os.path.dirname(__file__), 'site'))
    wsa.register('site', 'cmd', 'q', 'evt', 'r', {
            '*'    : {'root':os.path.join(os.path.dirname(__file__), 'site'), 'defpage':'squares.html'}
        })

    # API
    wsa.register('api', 'cmd', 'q', 'evt', 'r', {
            'heartbeat': lambda ctx, q: {'iid': ctx.opts.iid, 'info': webshoes.__info__},
            'getMatrix': getMatrix,
            'incMatrix': incMatrix
        })

    wsa.start()

    # Initialize events
    wsa.triggerEvent('matrixUpdate', {'m': opts.m})

    Log(f'Running at http://{addr}:{port}/site/squares.html')

    # Idle
    while opts['run'] :
        await asyncio.sleep(3)


def main():

    Log(webshoes.__info__)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Log(e)

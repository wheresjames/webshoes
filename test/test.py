#!/usr/bin/env python3

import json
import requests
import urllib
import asyncio
import websockets
import webshoes as ws

try:
    import sparen
    Log = sparen.log
except:
    Log = print

host = '127.0.0.1'
port = 15301

def getReq(cmd, opts):
    url = f'http://{host}:{port}'

    if cmd:
        params = urllib.parse.urlencode(opts)
        url += f'/{cmd}{("?"+params) if params else ""}'
    #url += ?{json.dumps(opts)}'

    Log(f'GET --> {url}')

    r = requests.get(url)

    Log(f'REP <-- {r.text}')

    return json.loads(r.text)


def cmdHeartbeat(ctx, q):
    return {'status': 'ok'}

def cmdAdd(ctx, q):
    return {'result': int(q.a) + int(q.b)}

def cmdAll(ctx, q):
    return {'p': ctx.p, 'q': q.as_dict()}

async def test_1():

    # Setup server
    wsa = ws.WebShoesApp(host, port, {'verbose': True})
    wsa.register('cmd', 'cmd', 'q', 'evt', 'r', {
            'heartbeat': cmdHeartbeat,
            'add': cmdAdd,
            '*': cmdAll
        })
    wsa.start()

    # Test http functions
    assert getReq('cmd/heartbeat', {})['status'] == 'ok'
    assert getReq('cmd/add', {'a': 3, 'b': 4})['result'] == 7
    assert getReq('cmd/catchall', {'a': 3, 'b': 4})['p'] == '/cmd/catchall'
    assert getReq('cmd/catchall', {'a': 3, 'b': 4})['q']['a'] == "3"

    # Test websockets
    try:

        async def wsRes(wcon):
            r = await wcon.recv()
            j = json.loads(r)
            Log(f'WSR <-- {j}')
            return j

        # Connect to websocket
        async with websockets.connect(f'ws://{host}:{port}') as wcon:

            await wcon.send(json.dumps({'cmd': 'heartbeat'}))
            assert (await wsRes(wcon))['r']['status'] == 'ok'

            await wcon.send(json.dumps({'cmd': 'heartbeat', 'tid':'123456789'}))
            assert (await wsRes(wcon))['tid'] == '123456789'

            await wcon.send(json.dumps({'cmd': 'add', 'q':{'a':3, 'b':4}}))
            assert (await wsRes(wcon))['r']['result'] == 7

            await wcon.send(json.dumps({'cmd': 'catchall', 'q':{'a':3, 'b':4}}))
            assert (await wsRes(wcon))['r']['p'] == 'catchall'

            await wcon.send(json.dumps({'evt': 'someEvent'}))
            assert 'uid' in (await wsRes(wcon))['r']

            wsa.triggerEvent('someEvent', {'value': 42})
            assert (await wsRes(wcon))['r']['value'] == 42

    except Exception as e:
        Log(e)

    # Stop the server
    wsa.stop()


def main():

    Log(ws.__info__)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_1())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Log(e)

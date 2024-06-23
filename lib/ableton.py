from aalink import Link
import asyncio

link_connected = False
async def aa_link():
    global link_connected
    if link_connected == True: return
    link_connected = True

    loop = asyncio.get_running_loop()

    link = Link(0, loop)
    link.start_stop_sync_enabled = True
    link.playing = False
    await asyncio.sleep(1)
    link.set_tempo_callback(handle_tempo_change)
    link.set_start_stop_callback(start_stop_callback)
    link.enabled = True

    while True:
        await link.sync(1)
        if player.is_playing:
            print(f'sync.. beat {link.beat} | phase {link.phase} | time {link.time} | quantum {link.quantum}')
            player.next_beat()

def run_aa_link():
    asyncio.run(aa_link())


### Ableton Link
# def start_stop_callback(playing):
#     print(f'playing: {playing}')

# def handle_tempo_change(tempo):
#     print(f'tempo: {tempo}')

# async def aa_link():
#     loop = asyncio.get_running_loop()

#     link = Link(120, loop)
#     link.set_start_stop_callback(start_stop_callback)
#     link.set_tempo_callback(handle_tempo_change)
#     link.enabled = True

#     while True:
#         await link.sync(1)
#         print('bang!')    

# asyncio.run(aa_link())


class Ableton:
    def __init__(self, loop, bpm):
        self.loop = loop
        self.bpm = bpm
        self.link = Link(bpm, loop)
        self.link.set_start_stop_callback(self.start_stop_callback)
        self.link.set_tempo_callback(self.handle_tempo_change)

    def start_stop_callback(self, playing):
        print(f'playing: {playing}')

    def handle_tempo_change(self, tempo):
        print(f'tempo: {tempo}')

    async def aa_link(self):
        await self.link.start()

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.link.set_bpm(bpm)

    def stop(self):
        self.link.stop()
from aalink import Link

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
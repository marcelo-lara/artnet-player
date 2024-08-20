import asyncio
from aalink import Link

class Ableton:
    def __init__(self, player):
        self.player = player
        self.link_armed = False

    def start_stop_callback(self, playing):
        print(f'ableton -> playing: {playing}')
        if playing:
            self.player.play(auto=False)
        else:
            self.player.stop()

    def handle_tempo_change(self, tempo):
        print(f'ableton -> tempo: {tempo}')
        tempo = round(tempo, 2)
        self.player.set_bpm(tempo)

    link_armed = False
    async def aa_link(self, player):
        if self.link_armed == True: return
        self.link_armed = True

        link = Link(0, asyncio.get_running_loop())

        link.start_stop_sync_enabled = True
        link.playing = False
        await asyncio.sleep(1)
        link.set_tempo_callback(self.handle_tempo_change)
        link.set_start_stop_callback(self.start_stop_callback)
        link.enabled = True
        try:
            print ('Ableton Connected')
            while True:
                await link.sync(1)
                self.link_armed = link.num_peers > 0
                if player.is_playing:
                    print(f'sync.. beat {link.beat} | phase {link.phase} | time {link.time} | num_peers {link.num_peers}')
                    player.next_beat()
                    if not self.link_armed:
                        player.stop()

        except (ConnectionError, asyncio.CancelledError):
            print("Ableton disconnected")

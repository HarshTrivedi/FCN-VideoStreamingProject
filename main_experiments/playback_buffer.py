from atomicfile import AtomicFile

class PlaybackBuffer:

    buffer_state_file = '.buffer_state'

    @classmethod
    def read(cls):
        with open(PlaybackBuffer.buffer_state_file, 'r') as f:
            playback_buffer = float(f.read().strip())
        return playback_buffer

    @classmethod
    def write(cls, playback_buffer):
        with AtomicFile(PlaybackBuffer.buffer_state_file, 'w') as f:
            f.write(str(playback_buffer))

    @classmethod
    def add(cls, increment):

        playback_buffer = PlaybackBuffer.read()
        updated_playback_buffer = max(playback_buffer + increment, 0)
        PlaybackBuffer.write(updated_playback_buffer)





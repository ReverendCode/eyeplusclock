################################################################################
# SoundObject
# PyAudio_Clock_Set_Project.py
# A. Hornof (ajh) - Sept 2015
#
# PyAudio-specific code adapted from https://people.csail.mit.edu/hubert/pyaudio/
# by ajh - Sept 2015
#
################################################################################
__author__ = 'hornof'

import pyaudio
import wave
import time

################################################################################
# Module initialization.
################################################################################

# Global variables
PYAUDIO = pyaudio.PyAudio()     # Instantiate PyAudio.
SOUND_OBJECT_LIST = [ ]         # A list of all SoundObjects.

# The last sound played, so that its stream can be closed before opening the next.
#   (On some devices, Port Audio can only open one stream at a time.)
LAST_OBJECT_PLAYED = None

################################################################################
# class SoundObject
# One object will be created for each sound object in the program.
################################################################################
class Sound:

    # Initializer function
    def __init__(self, sound_file_name):

        # Instance variables.
        self._soundfile_name = sound_file_name
        self._wavefile = wave.open(sound_file_name, 'rb')

        # Add the object to the list of all sound objects.
        SOUND_OBJECT_LIST.append(self)

    # Play the sound.
    def play(self):

        # Declare as global to access the module-level global variable.
        global LAST_OBJECT_PLAYED

        # Close the stream for the last SoundObject that was played.
        if LAST_OBJECT_PLAYED:   # If there is a last object
            LAST_OBJECT_PLAYED._stream.close()   # Close the stream.
            LAST_OBJECT_PLAYED._wavefile.rewind() # Rewind the file.

        # Create the callback function for the stream that will be created
        #   to play this sound object.
        def callback(in_data, frame_count, time_info, status):
            data = self._wavefile.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # Open a stream.
        self._stream = PYAUDIO.open(format=PYAUDIO.get_format_from_width(self._wavefile.getsampwidth()),
            channels=self._wavefile.getnchannels(),
            rate=self._wavefile.getframerate(),
            output=True,
            stream_callback=callback,
            start=True)

        # Record this stream as the new last stream played.
        LAST_OBJECT_PLAYED = self

    # Play the sound without permitting keystroke interruption
    def play_to_end(self):
        self.play()
        while self._stream.is_active():
            time.sleep(0.1)



################################################################################
# Module cleanup.
# This gets called when the module is destroyed/is no longer needed.
################################################################################
def cleanup_module_soundobj():
    # Terminate PyAudio.
    PYAUDIO.terminate()

import atexit
atexit.register(cleanup_module_soundobj)
#########################################################################
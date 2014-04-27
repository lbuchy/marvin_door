from subprocess import Popen, PIPE, STDOUT

from Accelerometer import Accelerometer
from twisted.internet import reactor

import random

import glob
import os

class SoundClip:
    file_path = ""

    def __init__(self, file_path):
        self.file_path = file_path

class Player:
    queue = []
    subproc = None

    def __init__(self):
        self.Reset()

    def AddClip(self, clip):
        self.queue.append(clip)

    def AddClips(self,clips):
        for each in clips:
            self.AddClip(each)

    def Play(self):
        if self.IsPlaying():
            return
        cmd = ['/usr/bin/mpg321']
        for each in self.queue:
            cmd.append(each.file_path)
        self.subproc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def IsPlaying(self):
        if self.subproc is None:
            return False
        # Check if subprocess exists, indicating playing
        ret = self.subproc.poll()
        if (ret == None):
            # Process still running
	    return True
        else:
            #wait for process to die fully
	    self.subproc.communicate()
            self.subproc = None
            return False
        # Should never get here, but good practice
        return False

    def WaitUntilDone(self):
        if self.subproc is None:
            return
        self.subproc.wait()

    def Reset(self):
        self.queue = []

# Returns a list of all mp3 files in a given directory
def GetSoundClips(directory):
    clips = []

    path = directory + "/*.mp3"
    files = glob.glob(path)
    for each in files:
        if not os.path.exists(each):
            continue
        clips.append(SoundClip(each))
    return clips

class AccelPlayer:
    player = None
    clips = None

    def __init__(self, player, clips):
        self.player = player
        self.clips = clips

    # A callback function at attach to the accelerometer
    def getData(self,x,y,z):
        print("x:%d y:%d z:%d" % (x,y,z))
        if not self.player:
            return
        if not self.clips:
            return
        if self.player.IsPlaying():
            return
        self._processData(x,y,z)

    def _playRandomClip(self):
        print("Playing Clip")
        self.player.Reset()
        random.shuffle(self.clips)
        self.player.AddClip(self.clips[0])
        self.player.Play()

    def _processData(self,x,y,z):

        # Implement this function to determine when to play
        # a sound clip
        if x < -20:
            self._playRandomClip()

def main():
    marvin_clips = GetSoundClips("clips")

    accel = Accelerometer(reactor, "/dev/ttyACM0")
    accelPlayer = AccelPlayer(Player(), marvin_clips)
    accel.setCallback(accelPlayer.getData)
    reactor.run()

if __name__ == "__main__":
    main()

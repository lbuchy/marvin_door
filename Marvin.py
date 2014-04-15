from subprocess import Popen, PIPE, STDOUT

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
        cmd = ['/usr/bin/mpg123']
        for each in self.queue:
            cmd.append(each.file_path)
        self.subproc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def IsPlaying(self):
        if self.subproc is None:
            return False
        if self.subproc.poll() is None:
            return False
        else:
            return True

    def WaitUntilDone(self):
        if self.subproc is None:
            return
        self.subproc.wait()

    def Reset(self):
        self.queue = []

def GetSoundClips(directory):
    clips = []

    path = directory + "/*.mp3"
    files = glob.glob(path)
    print files
    for each in files:
        if not os.path.exists(each):
            continue
        clips.append(SoundClip(each))
    return clips

def main():
    marvin_clips = GetSoundClips("/home/pi/marvin_door/clips")

    p = Player()
    p.AddClips(marvin_clips)
    p.Play()
    p.WaitUntilDone()

if __name__ == "__main__":
    main()

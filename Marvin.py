from subprocess import Popen, PIPE, STDOUT

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
    

def main():
    sound_clip = SoundClip("/home/pi/marvin_door/clips/depressed.mp3")

    p = Player()
    p.AddClip(sound_clip)
    p.Play()
    p.WaitUntilDone()

if __name__ == "__main__":
    main()

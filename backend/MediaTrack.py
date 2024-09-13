from aiortc.contrib.media import MediaStreamTrack
# from aiorc import AudioStreamTrack
from aiortc.mediastreams import AudioStreamTrack
from av import VideoFrame


# class AudioTransformTrack(MediaStreamTrack):

#     kind = "audio"

#     def _init_(self,track):
#         super()._init_()
#         self.track = track 

#     async def recv(self):
#         print(self.track)
#         frame = await self.track.recv()
#         print(frame)
#         return frame 



class AudioTransformTrack(AudioStreamTrack):

    kind = "audio"

    def _init_(self,track):
        super()._init_()
        self.track = track 

    async def recv(self):
        print(self.track)
        frame = await self.track.recv()
        print(frame)
        return frame 
    
    


class VideoTransformTrack(MediaStreamTrack):

    kind = "video"

    def _init_(self,track, transform):
        super()._init_()
        self.track = track 
        self.transform = transform

    async def recv(self):
        print(self.track)
        frame = await self.track.recv()
        print(frame)
        return frame
<script setup>

import { ref, onMounted, onUnmounted } from 'vue';




import log_out_svg from '../svg/log_out_svg.vue';
import wavePage from '../components/wavePage.vue'
import interlocutor_svg from '../svg/interlocutor_svg.vue'
import time_svg from '../svg/time_svg.vue'
import world_svg from '../svg/world_svg.vue'
import settings_svg from '../svg/bottom/settings_svg.vue'
import anonim_svg from '../svg/bottom/anonim_svg.vue'
import mic_svg from '../svg/bottom/mic_svg.vue'
import camera_svg from '../svg/bottom/camera_svg.vue'
import next_svg from '../svg/bottom/next_svg.vue'

import camera_off_svg from '../svg/bottom/camera_off_svg.vue'
import mic_off_svg from '../svg/bottom/mic_off_svg.vue'

// import settingsWindow from '../components/settingsWindow.vue'


const a = true;
const isMic = ref(false);
const isCamera = ref(false);


const localStream = ref(null); // Для хранения локального потока
// const pc = ref(null); // Для хранения RTCPeerConnection

const clickMic = async () => {
  isMic.value = !isMic.value;

  if (isMic.value) {
    try {
      localStream.value = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });

      document.getElementById('audio').srcObject = localStream.value;

      } 
    catch (error) {
      console.error('Ошибка получения доступа к микрофону:', error);
    }
  } 
    }

   
    
  
function clickCamera(){

    isCamera.value = !isCamera.value
}

import axios from 'axios'
const pc = ref(null);
const dc = ref(null);
const dcInterval = ref(null);
const dataChannelLog = ref('');
const timeStart = ref(null);
const useDataChannel = ref(false);
const useAudio = ref(false);
const useVideo = ref(false);
const screenSharing = ref(false);
const iceGatheringLog = ref('')
const iceConnectionLog = ref('')
const signalingLog = ref('')



const currentStamp = () => {
  if (timeStart.value === null) {
    timeStart.value = new Date().getTime();
    return 0;
  } else {
    return new Date().getTime() - timeStart.value;
  }
};


const createPeerConnection = () => {
  const config = {
    sdpSemantics: 'unified-plan',
    iceServers: [{ urls: ['stun:stun.l.google.com:19302'] }],
  }
  const pc = new RTCPeerConnection(config)

  // Обработчики событий
  pc.addEventListener('icegatheringstatechange', () => {
    iceGatheringLog.value += ' -> ' + pc.iceGatheringState
  })
  iceGatheringLog.value = pc.iceGatheringState

  pc.addEventListener('iceconnectionstatechange', () => {
    iceConnectionLog.value += ' -> ' + pc.iceConnectionState
  })
  iceConnectionLog.value = pc.iceConnectionState

  pc.addEventListener('signalingstatechange', () => {
    signalingLog.value += ' -> ' + pc.signalingState
  })
  signalingLog.value = pc.signalingState

  // Обработка треков (видео/аудио)
  pc.addEventListener('track', (evt) => {
    if (evt.track.kind === 'audio') {
        document.getElementById('audio').srcObject = evt.streams[0]
    } 
    else{
        document.getElementById('audio').srcObject = evt.streams[0]
    }
  })

  return pc
}


const negotiate = async () => {
    console.log("negotiate")
  try {
    
    pc.value = createPeerConnection();

    const offer = await pc.value.createOffer();
    await pc.value.setLocalDescription(offer);

    
    
    // await new Promise((resolve) => {
    //   if (pc.value.iceGatheringState === 'complete') {
    //     resolve();
    //   } else {
    //     const checkState = () => {
    //       if (pc.value.iceGatheringState === 'complete') {
    //         pc.value.removeEventListener('icegatheringstatechange', checkState);
    //         resolve();
    //       }
    //     };
    //     pc.value.addEventListener('icegatheringstatechange', checkState);
    //     // alert();
    //   }
    // });
   
    // Фильтруем кодеки
    let offerSdp = offer.sdp;
    const audioCodec = "";
    if (audioCodec !== 'default') {
      offerSdp = sdpFilterCodec('audio', audioCodec, offerSdp);
    }
    const videoCodec = "H264/90000";
    if (videoCodec !== 'default') {
      offerSdp = sdpFilterCodec('video', videoCodec, offerSdp);
    }

    // Отображаем Offer SDP
    // document.getElementById('offer-sdp').textContent = offerSdp;
    
    // Отправляем Offer на сервер
    const response = await axios.post('http://localhost:8000/api/offer', {
  sdp: offerSdp,
  type: offer.type,
  video_transform: "none",
});

    console.log(response.status)
    // Получаем Answer от сервера
    const answer = await response.data;
    
    // Отображаем Answer SDP
    // document.getElementById('answer-sdp').textContent = answer.sdp;

    // Устанавливаем Answer на RTCPeerConnection
    await pc.value.setRemoteDescription(answer);
  } catch (e) {
    alert(e);
  }
};


function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const sdpFilterCodec = (kind, codec, realSdp) => {
  const allowed = ref([]);
  const rtxRegex = new RegExp(`a=fmtp:(\\d+) apt=(\\d+)\r$`);
  const codecRegex = new RegExp('a=rtpmap:([0-9]+) ' + escapeRegExp(codec));
  const videoRegex = new RegExp('(m=' + kind + ' .*?)( ([0-9]+))*\\s*$');

  const lines = realSdp.split('\n');
  let isKind = false;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('m=' + kind + ' ')) {
      isKind = true;
    } else if (lines[i].startsWith('m=')) {
      isKind = false;
    }

    if (isKind) {
      let match = lines[i].match(codecRegex);
      if (match) {
        allowed.value.push(parseInt(match[1]));
      }

      match = lines[i].match(rtxRegex);
      if (match && allowed.value.includes(parseInt(match[2]))) {
        allowed.value.push(parseInt(match[1]));
      }
    }
  }

  const skipRegex = 'a=(fmtp|rtcp-fb|rtpmap):([0-9]+)';
  let sdp = '';

  isKind = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('m=' + kind + ' ')) {
      isKind = true;
    } else if (lines[i].startsWith('m=')) {
      isKind = false;
    }

    if (isKind) {
      const skipMatch = lines[i].match(skipRegex);
      if (skipMatch && !allowed.value.includes(parseInt(skipMatch[2]))) {
        continue;
      } else if (lines[i].match(videoRegex)) {
        sdp += lines[i].replace(videoRegex, '$1 ' + allowed.value.join(' ')) + '\n';
      } else {
        sdp += lines[i] + '\n';
      }
    } else {
      sdp += lines[i] + '\n';
    }
  }

  return sdp;
};



const start = async () => {
//   document.getElementById('start').style.display = 'none';
console.log("start")
  pc.value = createPeerConnection();

  if (useDataChannel.value) {
    const parameters = {"ordered":true};
    dc.value = pc.value.createDataChannel('chat', parameters);

    dc.value.onclose = () => {
      clearInterval(dcInterval.value);
      dataChannelLog.value += '- close\n';
    };

    dc.value.onopen = () => {
      dataChannelLog.value += '- open\n';
      dcInterval.value = setInterval(() => {
        const message = 'ping ' + currentStamp();
        dataChannelLog.value += '> ' + message + '\n';
        dc.value.send(message);
      }, 1000);
    };

    dc.value.onmessage = (evt) => {
      dataChannelLog.value += '< ' + evt.data + '\n';
      if (evt.data.substring(0, 4) === 'pong') {
        const elapsedMs = currentStamp() - parseInt(evt.data.substring(5), 10);
        dataChannelLog.value += ' RTT ' + elapsedMs + ' ms\n';
      }
    };
  }

  const constraints = {
    audio: useAudio.value ? {
      echoCancellation: true,
      echoCancellationType: 'system',
      noiseSuppression: true,
    } : false,
    video: false,
  };

  if (useVideo.value) {
    const resolution = "320x240";
    if (resolution) {
      const [width, height] = resolution.split('x').map(Number);
      constraints.video = {
        width: { ideal: width },
        height: { ideal: height },
        frameRate: { ideal: 5 },
      };
    } else {
      constraints.video = {};
    }
  }

  if (constraints.audio || constraints.video) {
    if (constraints.video) {
    //   document.getElementById('media').style.display = 'block';
    }
    if (screenSharing.value) {
      try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: false, audio: true });
        stream.getTracks().forEach((track) => {
          pc.value.addTrack(track, stream);
        });
        if (!constraints.audio) {
          await negotiate();
        }
      } catch (err) {
        alert('Could not acquire media: ' + err);
      }
      if (constraints.audio) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: {
            echoCancellation: true,
            echoCancellationType: 'system',
            noiseSuppression: true,
          }});
          stream.getTracks().forEach((track) => {
            pc.value.addTrack(track, stream);
          });
          await negotiate();
        } catch (err) {
          alert('Could not acquire media: ' + err);
        }
      }
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        stream.getTracks().forEach((track) => {
          pc.value.addTrack(track, stream);
        });
        await negotiate();
      } catch (err) {
        alert('Could not acquire media: ' + err);
      }
    }
  } else {
    await negotiate();
  }

//   document.getElementById('stop').style.display = 'inline-block';
};

const stop = () => {
  if (dc.value) {
    dc.value.close();
  }
  if (pc.value) {
    pc.value.close();
  }
//   document.getElementById('start').style.display = 'inline-block';
//   document.getElementById('stop').style.display = 'none';
  dataChannelLog.value = '';
  timeStart.value = null;
};


onMounted(async () => {
  await start()
});

onUnmounted(() => {
  stop();
});


</script>


<template>
    
    
    <div class="container">

        <settingsWindow v-if="!a"></settingsWindow>

      
        <audio id="audio" autoplay="true"></audio> 
        <audio id="remote_audio" autoplay="true"></audio>


        <div class="header">
            <div class="log_out">
                <log_out_svg></log_out_svg>

            </div>



            <div class="profile_info">
                <div class="image_profile">
                    <img src="diman.jpg">
                    <div class="welcome">
                        <span :style="{color:'white'}">Hello, Dimflix</span>
                        <span :style="{color:'#D9D2D9'}">Your data is safe</span>
                        
                    </div>
                    


                </div>
                
                <div class="online">

                </div> 
                <div class="server">

                </div>                   

            </div>
        </div>

        <div class="main">
           


            
            <div class="wave">
                <wavePage></wavePage>

            </div>
            <div class="voice_info">
                <div class="interlocutor">
                    <interlocutor_svg></interlocutor_svg>
                    <span>Неизвестно</span>


                </div>
                <div class="world">
                    <world_svg></world_svg>
                    <span>Неизвестно</span>

                </div>
                <div class="time">
                    <time_svg></time_svg>
                    <span>0:12:42</span>

                </div>

            </div>
        </div>


        <div class="bottom">

            <div class="settings">
                <settings_svg></settings_svg>

            </div>

            <div class="anonim">
                <anonim_svg></anonim_svg>

            </div>
            <div class="mic" :style="{background:!isMic ? 'red': '#8E1BE6'}"  @click="clickMic">
                <mic_svg v-if="isMic"></mic_svg>
                <mic_off_svg v-else-if="!isMic"></mic_off_svg>

            </div>
            <div class="camera" :style="{background:!isCamera ? 'red': '#8E1BE6'}" @click="clickCamera" >
                <camera_svg v-if="isCamera"></camera_svg>
                <camera_off_svg v-else-if="!isCamera"></camera_off_svg>
                

            </div>

            <div class="next">
                
                <next_svg></next_svg>

            </div>

        </div>
    </div>
</template>


<style scoped lang="scss">

span{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.container{
    width: 100%;
    height: 99vh;
    background: black;
    display: flex;
    flex-direction: column;
    gap: 15%;
}
.header{
    display: flex;
    padding: 15px;
    width: 92.7%;
    // background: red;
    gap: 15px;


        .log_out{
            width: 16%;
            height: 7vh;
            background: #8E1BE6;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;


        }
        .profile_info{
            width: 100%;
            display: flex;
            align-items: center;
            // justify-content: center;
            padding-left:10px ;
        
            height: 7vh;
            background: #8E1BE6;
            border-radius: 15px;

            .image_profile{
                display: flex;
                gap: 5px;
                
            }

            .welcome{
                display: flex;
                flex-direction: column;
                margin-top:5px ;
                
            }

            .image_profile img{
                width: 15%;
                height: 15%;
                border-radius:50% ;

            }
        }

}

.main{
    width: 95%;
    height: 50vh;
    // background: red;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-left:20px ;
    // justify-content: center;


    .voice_info{
        width: 70%;
        height: auto;
        background: #8E1BE6;
        // opacity: 0.5;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        padding-left:15px ;
       padding-top:10px ;
        gap: 10px;
        padding-bottom:5px ;

        .interlocutor, .world, .time{
            display: flex;
            gap: 15%;
            color:white;
            // opacity: 0.9;
            font-size: 17px;
        }

    }

 

}


.bottom{
    width: 100%;
    height: 10vh;
    // background: red;
    // margin-bottom:25px ;
    display: flex;
    align-items: center;
    gap: 10px;



    .settings{
        margin-left:10px ;
    }
    .settings, .anonim, .mic, .camera{
        width: 12%;
            height: 6vh;
            background: #8E1BE6;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
           

    }

    .next{
        width: 37%;
            height: 6vh;
            background: #8E1BE6;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
        
    }



}
</style>
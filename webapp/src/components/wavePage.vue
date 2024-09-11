<template>


  <div class="music">

    <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>
    
     <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>

    <div class="bar"></div>


  
    
  

  </div>

</template>


<style scoped>
* {
  margin: 0;

  padding: 0;

  box-sizing: border-box;
}

body {
  height: 100vh;

  display: flex;

  align-items: center;

  justify-content: center;

  background: black;
}

.music {
  width: 300px;

  height: 200px;

  /* position: relative;   */

  display: inline-flex;

  align-items: center;

  justify-content: space-between;
}

.music .bar {
  width: 12px;

  border-radius: 10px;

  background: #8E1BE6;

  animation: loader 1.5s ease-in-out infinite;
}

@keyframes loader {
  0%,
  100% {
    height: 2px;
  }

  50% {
    height: 80px;
  }
}

.music .bar:nth-child(1) {
  background: #8E1BE6;

  animation-delay: 1s;
}

.music .bar:nth-child(2) {
  background: #8E1BE6;

  animation-delay: 0.8s;
}

.music .bar:nth-child(3) {
  background: #8E1BE6;

  animation-delay: 0.6s;
}

.music .bar:nth-child(4) {
  background: #8E1BE6;

  animation-delay: 0.4s;
}

.music .bar:nth-child(5) {
  background: #8E1BE6;

  animation-delay: 0.2s;
}

.music .bar:nth-child(6) {
  background: #8E1BE6;

  animation-delay: 0.2s;
}

.music .bar:nth-child(7) {
  background: #8E1BE6;

  animation-delay: 0.4s;
}

.music .bar:nth-child(8) {
  background: #8E1BE6;

  animation-delay: 0.6s;
}

.music .bar:nth-child(9) {
  background: #8E1BE6;

  animation-delay: 0.8s;
}

.music .bar:nth-child(10) {
  background: #8E1BE6;

  animation-delay: 1s;
}


</style>
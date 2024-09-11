import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory, } from 'vue-router'



import screenTalk from './pages/screenTalk.vue'
import wavePage from './components/wavePage.vue'
const app = createApp(App)

const routes = [
    {path:"/talk", name:"talk", component:screenTalk},
    {path:"/test", name:"test", component:wavePage}
]



const router = createRouter({
    history: createWebHistory(),
    routes
})

app.use(router)
// app.use(pinia)

app.mount('#app')
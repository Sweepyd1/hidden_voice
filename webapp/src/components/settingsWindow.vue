<script setup>
import chevron_svg from '../svg/chevron_svg.vue'


</script>


<template>
    <div class="container_window">
        <div class="overlay"></div>
        <div class="window">

            <div class="language">
                <span>Язык</span>
                <chevron_svg class="chevron-icon"></chevron_svg>

            </div>

            <div class="theme">
                <span>Тема</span>
                <chevron_svg class="chevron-icon"></chevron_svg>


            </div>

            <div class="server">
                <span>Сервер</span>
                <chevron_svg class="chevron-icon"></chevron_svg>


            </div>


        </div>
    </div>
</template>

<style scoped lang="scss">

.chevron-icon {
    margin-right: 15px; /* Увеличьте или уменьшите значение по вашему усмотрению */
}


span{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.container_window {
    position: fixed;
    width: 97%;
    height: 99vh;
    display: flex;
    align-items: center;
    justify-content: center;

    .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: black;
    opacity: 0.8;
}

    .window {
        width: 95%;
        height: 80vh;
        background: #361251;
        position: relative; // Добавлено для корректного позиционирования
        display: flex;
        flex-direction: column;
        gap: 10px;

        .language, .theme, .server{
            width: 92%;
            height: 7vh;
            background: #7833AC;
            margin-left:10px ;
            border-radius: 10px;
            display: flex;
            align-items: center;
            color: white;
            padding-left:10px ;
            justify-content: space-between;

            
            
        }
    }
}


</style>

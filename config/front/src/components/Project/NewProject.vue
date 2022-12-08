<template>
<!-- @click="to({name : 'project_create'})" -->

    <v-card
        class="mx-6 blurred text-white"
        max-width="400"
        width = "320px"
        height = "180px"
        her
        @click="to()"
        
    >
        <div class = "d-flex justify-center align-center fill-height blurred">
            <v-icon :icon="icons.mdiPlus" size="large"></v-icon>
        </div>
    </v-card>
</template>

<script>

import { mdiPlus  } from '@mdi/js';


export default {
    name : "NewProject",

    data : () => ({
        icons : {mdiPlus}
        
    }),

    methods : {
        to : function(){
            this.$router.push({name : 'project_create'})
        }
    }


}
</script>

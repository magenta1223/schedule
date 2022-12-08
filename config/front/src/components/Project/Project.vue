<template>
    <v-card
        class="mx-6 blurred text-white"
        max-width="400"
        :image="img_src"
        width = "320px"
        height = "180px"
        cover
        @click="to()"
    >
        <div class = "blurred">
            <v-card-title> {{title}} </v-card-title>
            <v-card-subtitle class="pt-4"> {{subtitle}} </v-card-subtitle>

            <v-card-text> {{desc}} </v-card-text>

            <v-card-actions>
                <v-btn color="orange">
                    Edit
                </v-btn>

                <v-btn color="orange">
                    Join
                </v-btn>
            </v-card-actions>
        </div>
    </v-card>
</template>

<script>

export default {
    name : "ProJect",

    data : () => ({
        
    }),

    props : ['project_id', 'img_src', 'title', 'subtitle', 'desc'],
    methods : {
        to : function(){
            console.log(this.project_id)
            this.$router.push({
                name : 'project_retreive',
                query : {
                    project_id : this.project_id
                    },
                }
            )
        }
    }


}
</script>

<style scoped>
    .blurred{
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(2px);
        width : 320px !important;
        height:  100% !important;
    }
</style>
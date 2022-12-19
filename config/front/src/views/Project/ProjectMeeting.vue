<template>
    <v-container>
        <!-- HEADER -->
        <v-row class ="mb-4">
            <v-col cols="4">
                <v-select
                    v-model="activeView"
                    :items="activeViewOptions"
                    item-title="name"
                    item-value="name"
                    label="View"
                    density="compact"
                ></v-select>
            </v-col>
            <v-col cols="4">
                <v-btn
                    class ="mr-1"
                    @click="$refs.vuecal.previous()"
                    :icon="icons.mdiArrowLeft"
                    size="small"
                >
                </v-btn>
                <v-btn
                   
                    @click="$refs.vuecal.next()"
                    :icon="icons.mdiArrowRight"
                    size="small"
                >
                </v-btn>
            </v-col>
        </v-row>

        <!-- CALENDAR -->
        <v-row>
            <VueCal
                ref="vuecal"
                v-model:selected-date="selectedDate"
                v-model:active-view="activeView"
                hide-view-selector
                hide-title-bar
                :events="events"
                :disable-views="disable_views"
                :time-from="time_from"
                :time-to="time_to"
                :time-step="time_step"
                :events-on-month-view="eomv"
                :on-event-click="onEventClick"
            >
                <template #weekday-heading={heading}>
                    <div :style="wdHeaderStyle(heading)">
                        {{wdHeaderText(heading)}}
                    </div>
                </template>
            </VueCal>
        </v-row>

        <!-- RETRIEVE DIALOG -->

        <v-row>
            <v-dialog v-model ="openRetrieve" fullscreen :scrim="false" class="justify-center align-center" transition="dialog-bottom-transition">
                <v-card v-if="isPrivate" width="600px" >
                    <v-card-title>
                        Update Events
                    </v-card-title>
                    <v-row class="ma-2">
                        <v-text-field
                        v-model="selectedEvent.title"
                        label="Title"
                        >
                        </v-text-field>
                    </v-row>
                    <v-row class="ma-2">
                        <v-textarea
                        v-model="selectedEvent.content"
                        label="Content"
                        >
                        </v-textarea>
                    </v-row>
                    <div class="ma-2">
                        <Datepicker v-model="selectedEDate" range />
                    </div>

                    <v-card-actions class="justify-space-around">
                        <v-btn color="primary" width="25%"  variant="outlined" @click="updateEvent">
                            Update
                        </v-btn>
                        <v-btn color="error"  width="25%"  variant="outlined" @click="deleteEvent">
                            Delete
                        </v-btn>

                    </v-card-actions>
                </v-card>
                <v-card v-else width="600px" >
                    <v-card-title>
                        Project Meeting : {{selectedEvent.title}}
                    </v-card-title>
                    <v-card-text>
                        {{selectedEvent.content}}
                    </v-card-text>
                    <EasyDataTable
                        :headers="headers"
                        :items="selectedEvent.blocks"
                        table-class-name="customize-table"
                        show-index
                        body-text-direction ="center"
                        header-text-direction = "center"
                        :hide-rows-per-page="true"
                    >
                    <template #item-artist="{song}">
                        {{song.artist}}
                    </template>
                    <template #item-Vocal="{song}">
                        {{song.Vocal}}
                    </template>
                    <template #item-Guitar1="{song}">
                        {{song.Guitar1}}
                    </template>
                    <template #item-Guitar2="{song}">
                        {{song.Guitar2}}
                    </template>
                    <template #item-Bass="{song}">
                        {{song.Bass}}
                    </template>
                    <template #item-Drum="{song}">
                        {{song.Drum}}
                    </template>
                    <template #item-Keyboard="{song}">
                        {{song.Keyboard}}
                    </template>
                    </EasyDataTable>

                    <!-- <v-card-actions class="justify-space-around">
                        <v-btn color="primary" width="25%"  variant="outlined" @click="updateEvent">
                            Update
                        </v-btn>
                        <v-btn color="error"  width="25%"  variant="outlined" @click="deleteEvent">
                            Delete
                        </v-btn>

                    </v-card-actions> -->
                </v-card>

                
                
            </v-dialog>
        </v-row>


    </v-container>
</template>


<script>

import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import {mdiArrowLeft, mdiArrowRight} from "@mdi/js"
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import axios from "axios";
import setToken from "@/utils/auth.js"
// import { Header, Item } from "vue3-easy-data-table";

let url = "http://127.0.0.1:8000/api/event/";  // 장고 drf 서버 주소
let privateUrl = "http://127.0.0.1:8000/api/private/";  // 장고 drf 서버 주소


export default {
    name: 'ProjectMeeting',

    components: {
        VueCal,
        Datepicker
    },

    data() {
        return {
            icons : {
                mdiArrowLeft, mdiArrowRight
            },
            selectedDate: null,
            activeView: "month",
            activeViewOptions : ['month', 'week', 'day'],
            
            // disabling 
            disable_views : ['years', 'year'],
            disable_days : [], // 이거 computed로 설정. 곡 넣을 때 
            
            // special hours : 검색해서 보자. 곡 선택 시 가능한 지역 알려주는거임. 물론 억지로 넣을 수도 잇게..
            
            // week / day time interval
            time_from : 8 * 60,
            time_to :19 * 60,
            time_step : 30,

            // view events in month
            eomv : 'short',
        
            // header

            weekdayHeadings : {
                Sunday : {
                    short : 'Sun',
                    color : 'red'
                },
                Monday : {
                    short : 'Mon',
                    color : 'black'
                },
                Tuesday : {
                    short : 'Tue',
                    color : 'black'
                },
                Wednesday : {
                    short : 'Wed',
                    color : 'black'
                },
                Thursday : {
                    short : 'Thu',
                    color : 'black'
                },
                Friday : {
                    short : 'Fri',
                    color : 'black'
                },
                Saturday : {
                    short : 'Sat',
                    color : 'blue'
                },

            },

            events:[],

            // add events
            openAdd : false,
            newDate : [
                new Date(), 
                new Date()
            ],
            newEvent : {
                title : "",
                content : ""
            },

            // retrieve events
            openRetrieve : false,
            selectedEvent : {},
            selectedEDate : [],
            isPrivate : true,

            headers : [
                    {text : 'From', value : 'start'},
                    {text : 'To', value : 'end'},
                    {text : 'Artist', value : 'artist'},
                    {text : 'Title', value : 'title'},
                    {text : 'Vocal', value : 'Vocal'},
                    {text : 'Guitar1', value : 'Guitar1'},
                    {text : 'Guitar2', value : 'Guitar2'},
                    {text : 'Bass', value : 'Bass'},
                    {text : 'Drum', value : 'Drum'},
                    {text : 'Keyboard', value : 'Keyboard'},
            ],

        };
    },

    methods : {
        wdHeaderStyle : function(heading){
            if (heading.label === ''){
                return ''
            } else {
                return 'color:' + this.weekdayHeadings[heading.label].color
            }
        },
        wdHeaderText : function(heading){
            if (heading.label === ''){
                return ''
            } else {
                return this.weekdayHeadings[heading.label].short
            }
        },

        modal : function(){
            
            this.newDate[0] = this.selectedDate
            this.newDate[1] = this.selectedDate
            this.openAdd = true
        },

        onlyDate : function(date){
            date = new Date(date)
            return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
        },

        parseEvent : function(event, index){
            if (event.allDay === true){
                event.start = this.onlyDate(event.start)
                event.end = this.onlyDate(event.end)
            } else {
                event.start = new Date(event.start)
                event.end = new Date(event.end)        
            }
            
            event.class = event.cls
            event.index = index
        
            // event.cls가 만약 public이면, schedule을 parse
            // time table과 song으로 보여줘야 함. 




            return event
        },
        
        // list view
        getEvents : function(){
            console.log({
                    user_id : localStorage.getItem('user'),
                    project_id : this.$route.query.project_id,
                    type : 'public'
                }

            )
            axios({
                method : "GET",
                url : url,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    project_id : this.$route.query.project_id,
                    type : 'public'
                }
            }).then((response) => {
                // this.events.push( this.parseEvent(response.data.private))
                // this.events.push( this.parseEvent(response.data.public))


                this.events = response.data.map((event, i) => {
                    return this.parseEvent(event, i)
                })
            }).catch((error) => {
                console.log("Failed to get song list", error.response)
            })
        },

        // create view
        createEvent : function(){

            axios({
                method : "POST",
                url : privateUrl,
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                    start : this.newDate[0],
                    end : this.newDate[1],
                    title : this.newEvent.title,
                    content : this.newEvent.content,
                    participants : JSON.stringify([ localStorage.getItem('user')])
                }
            }).then((response) => {
                this.events.push( this.parseEvent(response.data))
                this.openAdd = false,
                this.newDate = [
                    new Date(), 
                    new Date()
                ]


            }).catch((error) => {
                console.log("Failed to get song list", error.response);
            });

        },

        // retrieve 
        onEventClick : function(event){
            this.selectedEvent = event
            this.selectedEDate = [event.start, event.end]
            this.openRetrieve = true
            this.isPrivate = event.cls === 'private'
        },

        // update 
        updateEvent : function(){
            axios({
                method : "PATCH",
                url : url + this.selectedEvent.id + '/',
                headers : setToken(),
                params : {
                    event_id : this.selectedEvent.id,
                    start : this.selectedEDate[0],
                    end : this.selectedEDate[1],
                    title : this.selectedEvent.title,
                    content : this.selectedEvent.content,
                }
            }).then((response) => {
                this.events[this.selectedEvent.index] = this.parseEvent(response.data, this.selectedEvent.index )
                this.selectedEvent = {}
                this.selectedEDate = []
                this.openRetrieve = false

            }).catch((error) => {
                console.log("Failed to update private event", error.response);
            });

        },

        // delete 
        deleteEvent : function(){
            axios({
                method : "DELETE",
                url : url + this.selectedEvent.id + '/',
                headers : setToken(),
                params : {
                    event_id : this.selectedEvent.id,
                }
            }).then((response) => {
                response;
                this.openRetrieve = false
                this.events.splice(this.selectedEvent.index, 1)
                this.events = this.events.map((event, i) => {
                    return this.parseEvent(event, i)
                })


            }).catch((error) => {
                console.log("Failed to update private event", error.response);
            });

        },



    },

    mounted() {
        this.getEvents()
    }

    


};
</script>

<style>
.v-dialog .v-overlay__content{
    flex-direction : row;
    justify-content : center
}

.vuecal--month-view .vuecal__cell {height: 100px;}

.vuecal--month-view .vuecal__cell-content {
  justify-content: flex-start;
  height: 100%;
  align-items: flex-end;
}

.vuecal--month-view .vuecal__cell-date {padding: 4px;}
.vuecal--month-view .vuecal__no-event {display: none;}
.vuecal--week-view .vuecal__no-event {display: none;}

.vuecal__event.P {
  background: rgb(255, 98, 98);
  display: flex;
  justify-content: center;
  align-items: center;
}

.private {
    background: rgb(255, 98, 98);
    display: flex;
    justify-content: center;
    align-items: center;
}

.public {
    background: rgb(159, 189, 255);
    display: flex;
    justify-content: center;
    align-items: center;
}


</style>
<template>
    <v-container>
        <!-- 헤더 -->
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
            <v-col>
                {{selectedDate}}
            </v-col>
            <v-col cols="2">
                <v-btn @click="modal"> SEARCH </v-btn>
            </v-col>
        </v-row>
        
        <!-- 캘린더 -->
        <v-row>
            <v-item-group multiple>
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
                    @cell-click="onCellClick"
                >
                    <template #weekday-heading={heading}>
                        <div :style="wdHeaderStyle(heading)">
                            {{wdHeaderText(heading)}}
                        </div>
                    </template>
                    
                    <template #cell-content="{ cell, view, events, goNarrower }" >
                        <div class="vuecal__flex vuecal__cell-content custom-cell" @click="onCellClick(cell)">
                            <!-- <v-row class ="ma-2">
                                {{ cell.content }}
                            </v-row> -->
                            <v-item v-slot="{ isSelected, toggle }">
                                <v-card
                                :color="isSelected ? 'primary' : ''"
                                class="d-flex align-center rounded-0 elevation-0"
                                dark
                                @click="[onCellClick(isSelected, cell), toggle()]"
                                height="100%"
                                width="100%"
                                >
                                <v-card-text class="text-center">
                                    {{cell.content}}
                                    <!-- {{ isSelected ? 'Selected' : 'Click Me!' }} -->
                                </v-card-text>
                                </v-card>
                            </v-item>

                        </div>
                        <span class="vuecal__cell-date" :class="view.id" v-if="view.id === 'day'" @click="goNarrower">
                        {{ cell.content }}
                        </span>
                        <span class="vuecal__cell-events-count" v-if="view.id === 'month' && events.length">{{ events.length }} </span>
                        <span class="vuecal__no-event" v-if="['week', 'day'].includes(view.id) && !events.length">Nothing here 👌</span>
                    </template>
                </VueCal>
            </v-item-group>
        </v-row>
        <!-- 모달 -->
        <v-row>
            <v-dialog
            v-model="openAddMeeting"
            fullscreen
            :scrim="false"
            transition="dialog-bottom-transition"
            >

                <v-card>
                    <!-- 툴바 -->
                    <v-toolbar
                    dark
                    color="primary"
                    >
                        <v-btn
                            :icon="icons.mdiClose"
                            dark
                            @click="openAddMeeting = false"
                        >
                        </v-btn>

                        <v-toolbar-title>
                            Searching best meeting
                        </v-toolbar-title>
                    </v-toolbar>

                    <!-- 참여 가능 인원 받아오기 -->
                    <v-container v-if="dialogView==='condition'">
                        <!-- 시간 constraint -->
                        <div class="text-h3">Time</div>
                        <v-range-slider
                            :min="9"
                            step="1"
                            thumb-label="always"
                            :max="24"
                            v-model="timeRange"
                            strict
                        ></v-range-slider>
                        <!-- 곡 constraint -->
                        <div class="text-h3">Songs</div>

                        <v-chip-group v-model="selectedSongs" multiple >
                            <v-chip v-for="song in project.songs" :key="song" filter>
                                {{song.title}}
                            </v-chip>
                        </v-chip-group>
                        <div class="text-h3">Dates</div>
                        <!-- 클릭 시, 배치 뷰로 바뀌어야 됨 -->
                        <v-card v-for="date in constrainedDates" :key="date" class="ma-0 pa-0" @click="arrangeView(date)" :ripple="true"> 
                            <v-card-title>
                                {{date}}
                            </v-card-title>
                            
                            <v-chip-group class="ma-2">
                                
                                <v-chip v-for="song in getSongs(date)" :key="song">
                                    {{song.title}}
                                </v-chip>
                            </v-chip-group>
                            
                            <v-divider></v-divider>
                        </v-card>

                    </v-container>


                    <v-container v-else-if="dialogView==='arange'">
                        <div class="text-h3">Time</div>
                        <!-- 배치를 할건데?
                        날짜 클릭 했자너
                        그럼 날짜 나오고


                        기존 로직대로

                        일단 시간대별로 가능한 곡을 띄워줍니다. 이걸 참조하면서 곡을 넣으면 됨

                        내가 하고싶은 시간을 입력하면

                        아래처럼 띄워줌

                        곡 chip을 마구 누르면 오른쪽에 드가는 시스템. 

                        곡 최소시간 입력 시, 입력초과 

                        한번이라도 들어갔으면 색을 다르게
                        
                        다 정하면 스케쥴 생성! 
        
    
                        1시 ~ 3시      |
                        곡 A, B, C     |
                        -------------  | ----------------- 
                        3시 ~ 6시      |
                        곡 A, C, E     |
            
                        곡 여러번 누르면 카운트 올라가게 해서.. 
                        
                        

                        
                        
                         -->
                    </v-container>
                    <!-- 일단 되는 사람 다 불러오고 -->
                    <!-- 시간대, 곡 등을 조건을 걸어본다. 그에 맞춰서 disable되는 곡이나 사람이 생기겠지? -->
                    <!-- 시간대를 조건으로 걸면?  -->

                    <!-- 조건 다 골랐으면 배치를 해야됨. -->
                    <!-- phase 별로 페이지 짜야됨. 페이지 넘기기 -->
                    


                </v-card>
            </v-dialog>

        </v-row>

    </v-container>
</template>

<script>
import axios from "axios"
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
// import Datepicker from '@vuepic/vue-datepicker';
import {mdiArrowLeft, mdiArrowRight, mdiClose} from "@mdi/js"

import setToken from "@/utils/auth.js"

let url = "http://127.0.0.1:8000/api/project/";  // 장고 drf 서버 주소

export default {
    name: 'YourComponent',

    data : () => {
        return {
            icons : {
                mdiArrowLeft, mdiArrowRight, mdiClose
            },
            
            // calendar header
            selectedDate: null,
            activeView: "month",
            activeViewOptions : ['month', 'week', 'day'],
            
            // views 
            disable_views : ['years', 'year'],
            disable_days : [], // 이거 computed로 설정. 곡 넣을 때 
                    
            // week / day time interval
            time_from : 8 * 60,
            time_to :23 * 60,
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

            events: [
                {
                    id : 1,
                    author : 1,
                    start: '2022-11-26 14:00',
                    end: '2022-11-26 17:30',
                    title: 'Boring event',
                    content: 'CEX',
                    // split : 1
                },
                {
                start: '2022-11-26 12:00',
                end: '2022-11-26 14:00',
                title: '합주',
                class: 'meeting',
                background: true,
                // split : 2
                },
            ],

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

            selectedNewDates : new Set(),
            openAddMeeting : false,

            timeRange : [12, 22],
            selectedSongs : [],

            dialogView : 'condition',

        }
    },

    components: {
        VueCal,
        // Datepicker
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

        onEventClick: function(event){
            event;
            console.log('eventclick')
        },

        onCellClick : function(isSelected, event){
            event;
            // isSelected === true : 이제 선택 안함
            // isSelected === false : 이제 선택 함
            // selected events에서 제거할지 말지 ? 
            if (typeof(isSelected) === 'boolean'){
                if (!isSelected){
                    console.log(event.startDate)
                    this.selectedNewDates.add(String(event.startDate))
                } else {
                    this.selectedNewDates.delete(String(event.startDate))
                }
            } 

            // console.log('----------------------------')
            // console.log(isSelected, this.selectedNewDates)
            // console.log('----------------------------')

        },

        retrieveProject : function(){
            axios({
                method : "GET",
                url : url + this.$route.query.project_id + '/',
                headers : setToken(),
                params : {
                    user_id : localStorage.getItem('user'),
                }
            }).then((response) => {
                this.project = response.data // project만 가져오자. songs는 songs list에서 가져오고 
                this.project.songs.map((song, index) => {
                    song.index = index
                    return this.parsePlayer(song)
                })
            }).catch((error) => {
                console.log("Failed to get retreival", error.response);
            });
        },

        parsePlayer : function(song){
            song.players.map((player) => {
                if (player.fixed){
                    //song[player.position] = player 
                    song[player.player.position] = player.player.user.name 
                }
            })
            return song
        },


        modal : function(){
            
            this.openAddMeeting = true
            this.dialogView = 'condition'
            console.log(this.selectedNewDates)
            this.getSongs()

        },

        
        // 1. 전체 사용자에 대해 날짜별, 시간대별로 가능한 곡을 전부 뽑는다. 
        // 2. 리스팅

        // 이걸 날짜별로 나누고 싶어.
        // 1. 전체 사용자에 대해 일정 contraint를 고려해, 날짜별로 가능한 곡을 전부 뽑아본다
        // 2. 여기에 추가적으로 합주시간 범위를 지정. global contraint
        // 3. 곡에 대한 constraint : 
        // 1번과 조건이 역임.
        // 어떤 곡에 대해, 현재 선택된 날짜들로 가봄
        // 날짜와 곡이 동시에 주어진 상황. 되냐?
        // 

        getSongs : function(date){
            // 일단은 하루별로 가능한 곡을 뽑아봄. 
            let availableSongs = Array()
            
                // 탐색의 범위를 줄이기 위해. 일부라도 가능하면.. 


                // let availableUsers = this.getAvailableUsers(date)

            
            for (let j in this.project.songs){
                let song = this.project.songs[j]
                
                for (let t = this.timeRange[0]; t < this.timeRange[1]; t++) {
                    console.log(song.title, date, t, this.isAvailableAt(song, date, t))
                    if(this.isAvailableAt(song, date, t)){
                        availableSongs.push(song)
                        break
                    }
                }
            }


                // 2) song. 루프 돌기전에 그 곡들을 먼저 체크. 하나라도 안되면 그날은 안되는 날.

                
            
            return availableSongs

        },

        isAvailableAt(song, date, time){
            let songStart = new Date(date)
            let songEnd = new Date(date)
            songStart.setHours(time)
            songEnd.setHours(time + 1)


            for (let i in song.players){
                let songplayer = song.players[i]

                if (!songplayer.fixed){
                    // fixed player 만 고려 
                    continue
                }

                let events = songplayer.player.user.events
                for (let j in events){
                    let event = events[j]
                    let eventStart = new Date(event.start)
                    let eventEnd = new Date(event.end)
                    if (event.allDay){
                        eventEnd.setHours(23, 59, 59)
                        if (songStart <= eventEnd && songEnd > eventStart){
                            return false
                        }
                    } else {
                        if (songStart <= eventEnd && songEnd > eventStart){
                            return false
                        }    
                    }
                }
            }

            return true

        }, 

        getAvailableUsers : function(date){

            let users = new Set()
            users; date;

            date = new Date(date)
            
            for (let i in this.project.songs){
                let players = this.project.songs[i].players
                let breakpoint = false
                for (let j in players){
                    let events = players[j].user.events
                    for (let k in events){
                        let event = events[k]
                        let start = new Date(event.start)
                        let end = new Date(event.end)


                        if (event.allDay){
                            if (start <= date && end >= date){
                                // allday 1일 찍어놓으면 시작과 끝이 같음.
                                // 겹치면 ? 일정이 있음! 
                                breakpoint = true
                                break
                            }
                        } else {
                            if (start <= date && end > date){
                                // allday 1일 찍어놓으면 시작과 끝이 같음.
                                breakpoint = true
                                break
                            }    
                        }
                    }
                    // 무사히 루프를 빠져나오면?
                    if (!breakpoint){
                        users.add(players[j])
                        breakpoint = false
                    }
                }
            }
            console.log(users)


        }, 

        getAvailableSongs : function(availableUsers){
            // 
            
            availableUsers;
            let availableSongs = Array()
            return availableSongs
            
        },



        getAvailableDays : function(constraintSongs){
            // 이 곡을 꼭 해야돼
            // 그르면 날짜별로 그 곡이 가능한지 체크를 한다.
            // 되는 날짜를 반환
            constraintSongs;

            this.selectedNewDates.map((date) => {
                date;

            })

            let availableDays = Array()
            return availableDays

        },

        arrangeView : function(date){
            console.log(date)
            this.dialogView = 'arange'
        }
    },

    mounted() {
        this.retrieveProject()
    },

    computed : {
        constrainedDates() {
            if (this.selectedSongs.length === 0){
                return this.selectedNewDates
            } else{


                let dates = new Set();
                
                for (let date of this.selectedNewDates){
                    for (let j in this.selectedSongs){
                        let song = this.project.songs[this.selectedSongs[j]]
                        for (let t = this.timeRange[0]; t < this.timeRange[1]; t++) {
                            if(this.isAvailableAt(song, date, t)){
                                dates.add(date)
                            }
                        }
                    }
                }
                console.log(dates)

                return dates
            }
            
        }
    }

    // watch : {
    //     selectedSongs : {
    //         handler : function(newVal, oldVal){
    //             oldVal; newVal;
    //             console.log(newVal)
    //         },

    //         intermediate : true,
    //         deep : true
    //     }
    // }

}
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

.vuecal__flex[grow]{
    flex:none
}



.vuecal__flex .vuecal__cell-content .custom-cell{
    align-items: center;
    justify-content: center;

}

</style>


<template>
    <VueCal
        hide-view-selector
        :events="events"
        :disable-views="disable_views"
        :time-from="time_from"
        :time-to="time_to"
        :time-step="time_step"
        :events-on-month-view="eomv"
        :small="true"
        :startWeekOnSunday="true"
        show-time-in-cells
    >
        <template #weekday-heading={heading}>
            <!-- {{heading}}
            color:'+weekdayHeadings[heading.heading.label].color
                        {{weekdayHeadings[heading.heading.label].short}}
            -->
            <div :style="wdHeaderStyle(heading)">
                {{wdHeaderText(heading)}}
            </div>
        </template>
    </VueCal>
</template>


<script>

import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

export default {
    name: 'YourComponent',
    components: {
        VueCal
    },
    data() {
        return {
            activeView: "month",
            
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

            // splitDays: [
            //     // The id property is added automatically if none (starting from 1), but you can set a custom one.
            //     // If you need to toggle the splits, you must set the id explicitly.
            //     // 합주실 나눌 때
            //     { id: 1, class: 'mom', label: 'Mom' },
            //     { id: 2, class: 'dad', label: 'Dad', hide: false }, 
            // ],
            
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
                    start: '2022-11-26 14:00',
                    end: '2022-11-26 17:30',
                    title: 'Boring event',
                    content: '<i class="icon material-icons">block</i><br>I am not draggable, not resizable and not deletable.',
                    class: 'blue-event',
                    deletable: false,
                    resizable: false,
                    draggable: false,
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
            ]        
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
        }
    }

    


};
</script>

<style>
/* .vuecal--month-view .vuecal__cell {height: 80px;}

.vuecal--month-view .vuecal__cell-content {
  justify-content: flex-start;
  height: 100%;
  align-items: flex-end;
}

.vuecal--month-view .vuecal__cell-date {padding: 4px;}
.vuecal--month-view .vuecal__no-event {display: none;}

.vuecal__cell {
    height : 100px!important
} */

</style>
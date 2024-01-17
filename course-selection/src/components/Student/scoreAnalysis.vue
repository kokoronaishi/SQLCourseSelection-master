<template>
    <div>
      <el-card class="card_box">
        <div id="main" style="width: 1200px; height: 550px"></div>
      </el-card>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router';
  import * as echarts from 'echarts'
  
  export default {
    setup() {
        const route = useRoute();
        const avgScoreList = ref([])
        
        const getData = async () => {
            let student_id = route.params.username
            const res = await fetch('http://localhost:8000/student/scoreAnalysis/',{
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                {student_id : student_id}
                )
            })
            const data = await res.json()
            if (res.status !== 200) {
            console.error('获取数据失败')
            return
            }
            console.log(data)
            avgScoreList.value = data.avg_score
        }
  
      const drawChart = () => {
        var myChart = echarts.init(document.getElementById('main'))
        var colors = ['#5470C6', '#91CC75', '#EE6666']
        var option = {
            title: {
            text: '平均成绩变化情况',
            x: 'center',
          },
          tooltip: {
            trigger: 'axis',
          },
          legend: {
            orient: 'vertical',
            x: 'right',
            y: 'center',
          },
          toolbox: {
            show: true,
            feature: {
              magicType: { show: true, type: ['line', 'bar'] },
              restore: { show: true },
              saveAsImage: { show: true },
            },
          },
          calculable: true,
          // 横轴
          xAxis: [
            {
              type: 'category',
              data: avgScoreList.value[0],
            },
          ],
          yAxis: [
            {
              type: 'value',
              name: '分数',
              min: 0,
              max: 100,
              position: 'left',
              axisLine: {
                show: true,
                lineStyle: {
                  color: colors[0],
                },
              },
            },
          ],
          series: [
            {
              type: 'line',
              name: '平均成绩',
              data: avgScoreList.value[1],
            },
          ],
        }
        myChart.setOption(option)
      }
  
      const refresh = async () => {
        await getData()
        drawChart()
      }
  
      onMounted(refresh)
  
      return {
        avgScoreList,
        refresh,
        getData,
        drawChart,
      }
    },
  }
  </script>
  
  <style scoped>
  .card_box {
    margin-top: 20px;
  }
  .pagination {
    margin-top: 15px;
  }
  </style>
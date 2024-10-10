<script lang="ts" setup>
const props = defineProps(["point", "number", "total"]);
const { point, number,total } = toRefs(props);
import { useScoreStore } from "@/store/score";
import { storeToRefs } from "pinia";
import {  ref, toRefs, watch } from "vue";
import { loadDb } from "@/sqlite.js";
import { nums } from "@/config.js";
const num = nums["vocab"];
// [0,num)随机数
const rand = Math.floor(Math.random() * num);
const db = await loadDb("gapfilling",`db/gapfilling/gapfilling${rand}.db`);
const data=db.exec(`select * from gapfilling ORDER BY RANDOM()LIMIT 1`)[0].values[0]
const { score, isFinished } = storeToRefs(useScoreStore());
import { Check, Close } from "@element-plus/icons-vue";
const processMaterial=(material:string)=>{
  return material.split("\n").map(str=>"&nbsp;&nbsp;&nbsp;&nbsp;"+str).join("<br/>")
}
const material=data[1]
const options=JSON.parse(data[2])
const answers=JSON.parse(data[3])
const explanations=JSON.parse(data[4])
const yourAnswers=ref([])
const lastScore=ref(0)
const isCorrects=ref([])
watch(yourAnswers,(newVal)=>{
    isCorrects.value=newVal.map((item,index)=>item==answers[index])
    const currentScore=isCorrects.value.reduce((a,b)=>{return a+b*(parseInt(point.value)/10)},0)
    score.value=score.value-lastScore.value+currentScore
    lastScore.value=currentScore
},{deep:true})


</script>

<template>
  <el-row justify="center">
    <el-card style="width: 90%; margin: 20px">
      <template #header>
        <div style="display: flex; justify-content: space-between">
          <div
            style="
              font-family: 'SimSun', '宋体', serif;
              font-weight: bold;
              font-size: 14px;
            "
          >
            第 {{ number }} 大题（共 {{ total }} 大题）：{{ point }}分
          </div>
          </div>
      </template>
      <div style="font-size: 16px;"><div v-html="processMaterial(material)"></div>
    </div>
      <el-row justify="center">
        <el-card style="width: 90%; margin-top: 20px" v-for="i in options.length">
          <div style="display: flex; justify-content: space-between">
            <div>第{{i}}小题({{ point/10 }}分)</div>
            <div v-if="isFinished" style="font-size: 20px">
              <div v-if="isCorrects[i-1]" style="color: green">
                <el-icon><Check /></el-icon>
              </div>
              <div v-else style="color: red">
                <el-icon><Close /></el-icon>
              </div>
            </div>
          </div>
          
          <div style="font-size: 25px;">
            <div v-for="(item, index) in options[i-1]" :key="index">
              <el-radio v-model="yourAnswers[i-1]" :value="index" :disabled="isFinished">{{ item }}</el-radio>
            </div>
          </div>
          <div v-if="isFinished">
            您的答案：{{ yourAnswers[i-1]!=null ? options[i-1][yourAnswers[i-1]]:"未作答" }}
            <br/>
            正确答案：{{options[i-1][answers[i-1]] }}
            <br/>
            您答{{ isCorrects[i-1]?'对':'错' }}了！
            <br/>
            答案解析：{{ explanations[i-1] }}
          </div>
        </el-card>
      </el-row>
     
     
      <template #footer>
        <div v-if="isFinished">
          {{ chinese }}
        </div>
      </template>
    </el-card>
  </el-row>
</template>

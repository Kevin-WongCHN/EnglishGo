<script lang="ts" setup>
const props = defineProps(["point", "number", "total"]);
const { point, number } = toRefs(props);
import { useScoreStore } from "@/store/score";
import { storeToRefs } from "pinia";
import { computed, ref, toRefs, watch } from "vue";
import { loadDb } from "@/sqlite.js";
import { nums } from "@/config.js";
const num = nums["vocab"];
// [0,num)随机数
const rand = Math.floor(Math.random() * num);
const db = await loadDb("vocab",`db/vocab/vocab${rand}.db`);
const data=db.exec(`select * from completion ORDER BY RANDOM()LIMIT 1`)[0].values[0]
const { score, isFinished } = storeToRefs(useScoreStore());
import { Check, Close } from "@element-plus/icons-vue";
const question=data[1]
const answer=ref()
const truth=data[2]
const isCorrect = computed(() => {
  return answer.value == truth
})
watch(isCorrect, (newVal, oldVal) => {
  if (newVal && !oldVal) {
    score.value += point.value
  }
  if (!newVal && oldVal) {
    score.value -= point.value
  }
});

</script>

<template>
  <el-row justify="center">
    <el-card style="width: 80%; margin: 20px">
      <template #header>
        <div style="display: flex; justify-content: space-between">
          <div
            style="
              font-family: 'SimSun', '宋体', serif;
              font-weight: bold;
              font-size: 14px;
            "
          >
            第 {{ number }} 题（共 {{ total }} 题）：{{ point }}分
          </div>
          <div v-if="isFinished" style="font-size: 20px">
            <div v-if="isCorrect" style="color: green">
              <el-icon><Check /></el-icon>
            </div>
            <div v-else style="color: red">
              <el-icon><Close /></el-icon>
            </div>
          </div>
        </div>
      </template>
      <div style="font-size: 16px;">{{question}}</div>
      <div style="font-size: 25px;">
        <el-input v-model="answer"></el-input>
      </div>
     
      <template #footer>
        <div v-if="isFinished">
          您的答案:{{ answer ? truth : "未作答" }} <br/>
          正确答案:{{ truth }} <br/>
          您答{{ isCorrect ? "对" : "错" }}了！
        </div>
      </template>
    </el-card>
  </el-row>
</template>

<script lang="ts" setup>
import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router=useRouter()
const doms = JSON.parse(route.query.data);
import { mapping } from "../utils.js";
import { ref, Suspense } from "vue";
import { useScoreStore } from "@/store/score";
import { storeToRefs } from "pinia";
let { score, isFinished } = storeToRefs(useScoreStore());
isFinished.value=false;
score.value = 0;
const totalScore = doms.reduce((a, b) => a + parseInt(b[2])*parseInt(b[1]), 0);
const submit = () => {
  isFinished.value = true;
};
const redo=()=>{
    router.push({name:"index"})
}
</script>

<template>
  <el-row justify="center">
    <el-card style="width: 90%; margin-top: 20px">
        <el-result
        v-if="isFinished"
          icon="success"
          title="向下滑动查看详情！"
          :sub-title="`您的得分：${score}/${totalScore}`"
        >
          <template #extra>
            <el-button type="primary" @click="redo">再做一次</el-button>
          </template>
        </el-result>
      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item v-for="dom in doms" :name="dom[0]">
          <template #title>
            <div
              style="
                font-size: 18px;
                font-weight: bold;
                font-family: 'SimSun', '宋体', serif;
              "
            >
              {{ dom[0] }}
            </div>
          </template>
          <Suspense>
            <component
              v-for="i in parseInt(dom[1])"
              :point="dom[2]"
              :number="i"
              :total="parseInt(dom[1])"
              :is="mapping[dom[0]]"
            ></component>
          </Suspense>
        </el-collapse-item>
      </el-collapse>
      <el-row justify="center">
        <el-button
          type="primary"
          @click="submit"
          style="margin-top: 20px"
          v-if="!isFinished"
          >提交</el-button
        >
        
      </el-row>
    </el-card>
  </el-row>
</template>

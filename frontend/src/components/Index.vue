<script lang="ts" setup>
import { reactive, ref, watch } from "vue";

const checkList = ref();
const doms = ref([]);
watch(checkList, (newVal, oldVal) => {
  console.log(newVal,oldVal)
  if(!oldVal){
      doms.value.push([newVal[0],1,null])
  }else if(newVal.length>oldVal.length){
      const diff=newVal.filter(ele=>!oldVal.includes(ele))[0]
      doms.value.push([diff,1,null])
  }else{
      const diff = oldVal.filter(ele=>!newVal.includes(ele))[0]
      doms.value=doms.value.filter(arr=>arr[0]!=diff)
  }
});
import { useRouter } from "vue-router";
const router=useRouter()
const confirm=()=>{
    router.push({name:"quiz",query:{data:JSON.stringify(doms.value)}})
}

</script>

<template>
  <el-row justify="center">
    <el-card style="width: 680px; margin-top: 20px">
      <template #header>
        <div class="card-header">
          <!-- 宋体 -->
          <div
            style="
              font-family: 'SimSun', '宋体', serif;
              font-size: 25px;
              font-weight: bold;
              text-align: center;
            "
          >
            请选择题型、数量和分值
          </div>
        </div>
      </template>

      <el-checkbox-group v-model="checkList">
        <el-checkbox label="完形填空" value="完形填空" />
      </el-checkbox-group>
      <el-checkbox-group v-model="checkList">
        <el-checkbox label="长篇阅读" value="长篇阅读" />
        <el-checkbox label="短篇阅读" value="短篇阅读" />
      </el-checkbox-group>
      <el-checkbox-group v-model="checkList">
        <el-checkbox label="首字母填空" value="首字母填空" />
        <el-checkbox label="近义词" value="近义词" />
        <el-checkbox label="反义词" value="反义词" />
      </el-checkbox-group>
      <el-checkbox-group v-model="checkList">
        <el-checkbox label="对话听力" value="对话听力" />
        <el-checkbox label="短篇听力" value="短篇听力" />
        <el-checkbox label="释义听力" value="释义听力" />
      </el-checkbox-group>
      <template #footer>
        <el-form label-width="auto">
          <el-form-item v-for="dom in doms" :label="dom[0]">
            <div style="display: flex;">
              <div style="color: #606266;">题目数量：</div>
              <el-select placeholder="请选择题目数量" v-model="dom[1]" style="width: 80px;margin-right:20px">
                <el-option v-for="i in 5" :label="i" :value="i">
                </el-option>
              </el-select>
              <div style="color: #606266;">题目分值：</div>
              <el-select placeholder="请选择题目分值" v-model="dom[2]" style="width: 80px;margin-right:20px"> 
                <div v-if="dom[0]=='长篇阅读'">
                  <el-option v-for="i in 5" :label="i*5" :value="i*5"/>
                </div>
                <div v-else-if="dom[0]=='短篇阅读'">
                  <el-option v-for="i in 5" :label="i*3" :value="i*3"/>
                </div>
                <div v-else-if="dom[0]=='完形填空'">
                  <el-option v-for="i in 5" :label="i*10" :value="i*10"/>
                </div>
                <div v-else-if="dom[0]=='对话听力'">
                  <el-option v-for="i in 5" :label="i*3" :value="i*3"/>
                </div>
                <div v-else-if="dom[0]=='短篇听力'">
                  <el-option v-for="i in 5" :label="i*3" :value="i*3"/>
                </div>
                <div v-else>
                  <el-option v-for="i in 5" :label="i" :value="i"/>
                </div>
               
              </el-select>
            </div>
          </el-form-item>
          <el-row justify="center">
              <el-button type="primary" @click="confirm" :disabled="!doms.length">确定</el-button>
          </el-row>
          
        </el-form>
        
      </template>
    </el-card>
  </el-row>
</template>

<style scoped>
.el-form-item__label {
    width: 3000px;
}
</style>

<script lang="ts" setup>
</script>

<template>
    <el-row justify="center" >
        <el-card style="width: 70%; margin-top:20px">
            <el-row>
                <el-col :span="6">
                    <el-statistic title="题目生成工具" value="ChatGPT" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="音频生成工具" value="ChatTTS" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="前端框架" value="vue3+elementUI" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="数据存储" value="sqlite" />
                  </el-col>
            </el-row>
        </el-card>
        
        <el-card style="width: 70%; margin-top:20px">
            内容由chatGPT生成，请勿完全相信内容，答案有可能错误，有问题可以提issue，谢谢！
        </el-card>
        <el-card style="width: 70%; margin-top:20px">
            本项目由gitpage托管，完全是个前端项目，版本号为v1.0.1
        </el-card>
        <el-card style="width: 70%; margin-top:20px">
            目前题库数量：
            <br/>
            完形填空：6题
            长篇阅读：6题，
            短篇阅读：6题，
            对话听力：6题，
            短篇听力：6题
            释义听力：180题，
            首字母填空：180题，
            近义词：180题，
            反义词：180题
            <br/>
            题库大约1周一更，敬请期待
        </el-card>
      </el-row>

</template>
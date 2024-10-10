<script lang="ts" setup>
const doms=[
    ["完形填空",1,1],
    ["长篇阅读",1,1],
    ["短篇阅读",1,1],
    ["近义词",1,1],
    ["反义词",1,1],
    ["完形填空",1,1],
    ["首字母填空",1,1],
    ["对话听力",1,1],
    ["短篇听力",1,1],
    ["释义听力",1,1]
    ]
</script>

<template>
    <el-row justify="center">
        <el-card style="width: 85%; margin-top: 20px">
            <el-collapse v-model="activeNames" @change="handleChange">
                <el-collapse-item v-for="dom in doms" :title="dom[0]" :name="dom[0]">
                </el-collapse-item>
              </el-collapse>
        </el-card>
    </el-row>
</template>
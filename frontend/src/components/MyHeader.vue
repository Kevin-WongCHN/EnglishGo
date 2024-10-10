<script lang="ts" setup>
import { ref } from 'vue';
const activeIndex = ref('/index');
</script>

<template>
    <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    router
  >
    <el-menu-item>
        <div style="font-size: 26px; font-style: italic; font-weight: bold;">
            EnglishGo
        </div>
      
    </el-menu-item>
    <el-menu-item index="/index">首页/答题</el-menu-item>
    <el-menu-item index="/example">题型示例</el-menu-item>
    <el-menu-item index="/about">关于我们</el-menu-item>
  </el-menu>
</template>
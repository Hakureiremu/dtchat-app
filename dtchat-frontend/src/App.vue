<template>
  <div id="app">
    <ChatInterface />
  </div>
</template>

<script>
import ChatInterface from './components/ChatInterface.vue';

export default {
  name: 'App',
  components: {
    ChatInterface
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}
</style>

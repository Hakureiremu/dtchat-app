<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" :class="{'message': true, 'message-user': message.sender === 'You', 'message-bot': message.sender === 'Bot'}">
        <div class="message-content">{{ message.text }}</div>
      </div>
    </div>
    <div class="input-container">
      <input v-model="input" @keyup.enter="sendMessage" placeholder="Type your message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      input: '',
      messages: [
        { sender: 'Bot', text: 'Hello! How can I help you today?' }
      ]
    };
  },
  methods: {
    async sendMessage() {
      if (this.input.trim() === '') return;
      // 缓存用户输入的消息
      const userInput = this.input;

      // 清空输入框
      this.input = '';
      // Add user's message
      this.messages.push({ sender: 'You', text: userInput });
      
      // Send message to backend
      try {
        const response = await axios.post('http://127.0.0.1:11000/api/chat/ask/', { question: userInput });
        this.messages.push({ sender: 'Bot', text: response.data.answer });
      } catch (error) {
        this.messages.push({ sender: 'Bot', text: 'Sorry, there was an error processing your request.' });
      }

    }
  }
}
</script>

<style>
.chat-container {
  width: 100%;
  height: 80vh;
  max-width: 1200px;
  margin: 0 auto;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.message {
  margin-bottom: 10px;
  display: flex;
}

.message-content {
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
}

.message-bot .message-content {
  background-color: #f1f1f1;
  align-self: flex-start;
  text-align: left;
  margin-left: 0;
}

.message-user {
  justify-content: flex-end;
}

.message-user .message-content {
  background-color: #e0ffe0;
  text-align: left;
  margin-right: 0;
}

.input-container {
  display: flex;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  margin-left: 10px;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #36a273;
}
</style>

<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" :class="{'message': true, 'message-user': message.sender === 'You', 'message-bot': message.sender === 'Bot'}">
        <div class="message-content">
          <!-- 显示文本内容 -->
          <div v-if="message.text">{{ message.text }}</div>
          
          <!-- 显示加载动画 -->
          <div v-if="message.loading" class="loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>

          <!-- 显示结构化数据 -->     
          <div v-if="message.table" class="structured-table">
            <table>
              <thead>
                <tr>
                  <th v-for="(header, idx) in message.table.headers" :key="idx">{{ header }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, rowIndex) in message.table.rows" :key="rowIndex">
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                    <template v-if="Array.isArray(cell)">
                      {{ cell.join(', ') }}
                    </template>
                    <template v-else>
                      {{ cell }}
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>       
        </div>      
      </div>
    </div>

    <div class="input-container">
      <input v-model="input" @keyup.enter="sendMessage" placeholder="Type your message..." />
      <button @click="sendMessage">Send</button>
    </div>

    <!-- 错误信息 -->
    <p v-if="error" class="error">Error: {{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      input: '',
      messages: [
        { sender: 'Bot', text: 'Hello! How can I help you today? Multiple APIs have been integrated to help you obtain higher quality responses' },
        { sender: 'Bot', text: 'Try to ask me questions related to:\n 1. CS Research\n 2. Weather\n 3. News\n 4. iTunes Music\n 5. Youtube Videos/Channels\n 6. Professional Email Addresses' }
      ],
      function_name: '',
      data:[], 
      schemas: {
        'get_publications': {
          headers: ['title', 'author', 'venue', 'year'],
          fields: ['title', 'authors', 'venue', 'year']
        },
        'get_videos':{
          headers: ['title', 'description', 'channelTitle', 'publishTime'],
          fields: ['title', 'description', 'channelTitle', 'publishTime']         
        },
        'get_news':{
          headers: ['headline', 'section', 'url', 'publish_date'],
          fields: ['headline', 'section', 'url', 'publish_date']        
        },
        'get_itunes':{
          headers: ['type', 'kind',	'artistName',	'collectionName',	'trackName', 'trackTime'],
          fields: ['type', 'kind',	'artistName',	'collectionName',	'trackName', 'trackTime']   
        },
        'get_emails':{
          headers: ['first_name', 'last_name',	'email',	'position',	'department'],
          fields: ['first_name', 'last_name',	'email',	'position',	'department']      
        }
      },
      error: ''
    };
  },
  
  computed: {
    schema() {
      return this.schemas[this.function_name] || { columns: [] };
    }
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
      
      // 添加加载动画消息到聊天记录
      const loadingMessage = { sender: 'Bot', loading: true };
      this.messages.push(loadingMessage);

      // 清除之前的错误信息
      this.error = '';
      
      // Send message to backend
      try {
        const response = await axios.post('http://127.0.0.1:11000/api/chat/ask/', { question: userInput });
        const responseData = response.data 

        // 处理结构化数据
        // 创建Bot的消息对象
        const botMessage = { sender: 'Bot', text: responseData.answer };

        // 检查是否有结构化数据
        if (responseData.function_name && responseData.data && this.schemas[responseData.function_name]) {
          const schema = this.schemas[responseData.function_name];
          const rows = responseData.data.map(item => schema.fields.map(field => item[field]));

          // 添加结构化数据到Bot的消息中
          botMessage.table = {
            headers: schema.headers,
            rows: rows
          };
        }
        
        // 替换加载动画消息为实际的Bot消息
        const loadingIndex = this.messages.findIndex(msg => msg === loadingMessage);
        if (loadingIndex !== -1) {
          this.$set(this.messages, loadingIndex, botMessage);
        } else {
          this.messages.push(botMessage);
        }
      } catch (error) {
        console.error('Error:', error);
        // 替换加载动画消息为错误消息
        const loadingIndex = this.messages.findIndex(msg => msg === loadingMessage);
        if (loadingIndex !== -1) {
          this.$set(this.messages, loadingIndex, { sender: 'Bot', text: 'Sorry, there was an error processing your request.' });
        } else {
          this.messages.push({ sender: 'Bot', text: 'Sorry, there was an error processing your request.' });
        }

        if (error.response && error.response.data && error.response.data.error) {
          this.error = error.response.data.error;
        } else {
          this.error = '未知错误。';
        }
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

/* 表格样式 */
.structured-table {
  margin-top: 10px;
  overflow-x: auto;
}

.structured-table table {
  width: 100%;
  border-collapse: collapse;
  word-wrap: break-word;
  table-layout: fixed;
}

.structured-table th,
.structured-table td {
  padding: 8px 12px;
  border: 1px solid #ccc;
}

.structured-table th {
  background-color: #f9f9f9;
}

/* 加载动画样式 */
.loading {
  display: flex;
  align-items: center;
}

.dot {
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #888;
  border-radius: 50%;
  animation: blink 1.4s infinite both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes blink {
  0%, 80%, 100% {
    opacity: 0;
  }
  40% {
    opacity: 1;
  }
}
</style>

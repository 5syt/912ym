const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const chatRoutes = require('./routes/chat');
const knowledgeRoutes = require('./routes/knowledge');
const recordRoutes = require('./routes/records');
const faqRoutes = require('./routes/faq');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../public')));

app.use('/api/chat', chatRoutes);
app.use('/api/knowledge', knowledgeRoutes);
app.use('/api/records', recordRoutes);
app.use('/api/faq', faqRoutes);

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.listen(PORT, () => {
  console.log(`旅游助手智能体服务已启动: http://localhost:${PORT}`);
});

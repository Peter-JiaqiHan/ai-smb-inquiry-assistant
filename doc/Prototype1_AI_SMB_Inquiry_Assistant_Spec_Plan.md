# Prototype 1 Spec & Plan — AI 商家询盘助手 (AI SMB Inquiry Assistant)

## 1. 项目目标
做一个面向中小商家的原型系统，把“客户咨询”转化为“可跟进的销售线索”。

适用商家示例：
- 诊所 / 眼科 / 牙科
- 窗帘 / 家装 / 装修
- 健身房 / 培训机构
- 地产经纪 / 本地服务商

这个原型重点不是做成正式 SaaS，而是验证：
- LLM 是否能回答常见问题
- 系统是否能自动收集客户信息
- 是否能帮助商家更快跟进线索

---

## 2. 核心使用场景
用户在网页聊天窗口中咨询：
- 价格
- 服务内容
- 营业时间
- 地址
- 是否可预约
- 某个服务是否适合自己

系统完成：
1. 基于知识库回答问题
2. 识别高价值咨询
3. 收集客户姓名/电话/邮箱/需求
4. 保存线索到后台
5. 生成简单的 follow-up 建议

---

## 3. V1 原型范围（建议 2–3 周）
### 必须有
- 单商家版本
- 网页聊天界面
- FAQ / 知识库导入
- LLM + 向量检索问答
- lead capture（姓名、电话、邮箱、需求）
- 线索列表后台
- 基本对话记录保存

### 暂时不做
- WhatsApp 正式接入
- Instagram 正式接入
- 多租户
- 复杂权限系统
- 复杂部署
- 精美 UI
- 复杂工作流引擎

---

## 4. 主要功能清单
### 4.1 前台聊天
- 用户输入问题
- 系统返回基于知识库的答案
- 若问题涉及预约/报价/咨询，系统引导用户留下联系方式

### 4.2 知识库问答
知识库内容可包含：
- FAQ
- 服务介绍
- 地址、营业时间
- 价格说明
- 政策说明

### 4.3 线索收集
系统尝试收集：
- 姓名
- 电话
- 邮箱
- 咨询主题
- 用户备注

### 4.4 线索管理后台
后台可查看：
- lead 列表
- 联系方式
- 最近一条问题
- 意向等级（高/中/低）
- 创建时间

### 4.5 简单意向判断
初版可用规则或 LLM 输出：
- 高：询问预约、价格、时间、明确需求
- 中：了解服务细节
- 低：泛泛咨询

---

## 5. 页面清单
### 页面 1：聊天页
内容：
- 商家名称
- 欢迎语
- 聊天消息区
- 输入框
- 联系方式收集区（可在聊天中插入）

### 页面 2：Lead 管理页
内容：
- lead 列表
- 搜索 / 简单筛选
- 查看 lead 详情
- 查看聊天摘要

### 页面 3：知识库管理页（可简化）
内容：
- FAQ 列表
- 添加 / 编辑 FAQ
- 导入文本

如果时间紧，知识库管理页可以先不做成页面，直接用 JSON / CSV 文件导入。

---

## 6. 数据模型建议
### lead
- id
- name
- phone
- email
- inquiry_topic
- intent_level
- summary
- created_at
- updated_at

### conversation
- id
- lead_id (nullable)
- session_id
- created_at

### message
- id
- conversation_id
- role (user / assistant / system)
- content
- created_at

### knowledge_document
- id
- title
- content
- source_type
- created_at

### knowledge_chunk
- id
- document_id
- chunk_text
- embedding
- chunk_index

---

## 7. 技术栈建议
### Backend
- FastAPI
- SQLModel
- MySQL

### Frontend
- React.js
- TypeScript
- Tailwind CSS
- Responsive GUI

### AI / Retrieval
- OpenAI-compatible API
- Embedding API
- 简单 RAG 流程
- Top-k 检索
- 轻量向量检索层（原型阶段可独立于 MySQL）

### 技术说明
- **FastAPI**：适合做聊天接口、管理后台 API、Webhook 和第三方平台集成。
- **SQLModel**：对 Python 开发者上手更自然，适合原型和中小型项目的模型定义。
- **MySQL**：更贴近真实商业项目，适合作为作品集中的正式业务数据库。
- **React.js + Tailwind CSS**：适合快速搭建聊天页、管理后台、商品页和 FAQ 页面。
- **Responsive GUI**：让原型在桌面和手机浏览器上都能正常演示，更像真实产品。

### 关于向量检索
建议原型阶段先采用：
- **MySQL** 存业务数据
- **独立轻量向量检索层** 处理 embedding 检索

这样能保持主技术栈清晰，也避免一开始把数据库方案做得过重。

---

## 8. API 设计建议
### Public API
- POST /api/chat/message
- POST /api/leads
- GET /api/knowledge/search (可选)

### Admin API
- GET /api/admin/leads
- GET /api/admin/leads/{id}
- GET /api/admin/conversations/{id}
- POST /api/admin/knowledge/import
- GET /api/admin/knowledge/docs

---

## 9. 聊天流程建议
### 典型流程
1. 用户提问
2. 系统检索知识库
3. LLM 生成回答
4. 若用户表现出较强意向，则提示留下联系方式
5. 保存 lead
6. 生成简短 summary

### 系统提示词重点
- 只能依据知识库回答
- 不确定时要诚实说明
- 回答后尽量引导下一步
- 不要虚构价格和政策

---

## 10. Demo 演示脚本建议
### 场景 A：普通 FAQ
用户问营业时间 / 地址 / 服务范围  
-> 系统准确回答

### 场景 B：高意向咨询
用户问价格、预约、适不适合  
-> 系统回答并引导留下电话邮箱

### 场景 C：后台查看
管理员打开 lead 列表  
-> 能看到新线索和聊天摘要

---

## 11. 简历描述建议
- Built an AI-powered inquiry assistant for SMBs to answer FAQs, capture lead details, and qualify customer intent.
- Developed a FastAPI + React prototype with knowledge-base retrieval, lead management, and conversation logging.
- Designed a lightweight RAG workflow to support customer support and inquiry handling for local businesses.

---

## 12. 2–3 周开发计划
### Week 1
- 建项目结构
- FastAPI 基础接口
- React 基础聊天页
- MySQL 建表
- FAQ 数据准备

### Week 2
- 实现 embedding + 检索
- 接入 LLM
- 完成聊天闭环
- 实现 lead capture
- 实现 lead 列表页

### Week 3
- 优化提示词
- 增加意向等级
- 增加聊天摘要
- 修 UI
- 录 demo 视频
- 写 README

---

## 13. V2 可选扩展
- 邮件通知商家
- 预约链接
- WhatsApp webhook 模拟接入
- 多商家模式
- Dashboard 统计
- 自动 follow-up 建议增强

---

## 14. 成功标准
做到以下几点就算成功：
- 本地可运行
- 能回答 FAQ
- 能保存咨询记录
- 能收集 lead
- 能演示真实业务场景
- 具备基本 Responsive GUI，桌面和手机浏览器都可演示
- 能写进简历和 GitHub README

---

## 15. Developer Accounts to Apply

### Apply now
#### 1. GitHub
Use for:
- source control
- portfolio presentation
- README
- demo links
- issue/task tracking

Why now:
This is the base account for the whole prototype and future job search.

#### 2. Google Account + Google Cloud Project
Use for:
- learning OAuth and callback flows
- future Gmail / Calendar / Maps integrations
- possible email notification flow
- general API integration practice

Why now:
Even though V1 is mainly a web chat prototype, Google Cloud is a very good developer setup for learning real integration patterns.

#### 3. One LLM API Provider Account
Examples:
- OpenAI
- another OpenAI-compatible provider

Use for:
- embeddings
- RAG answer generation
- lead summary
- intent classification

Why now:
As soon as the prototype moves beyond static UI, this becomes necessary.

### Apply later
#### 4. Meta for Developers
Use for:
- future Instagram / WhatsApp extensions
- webhook testing
- message-channel integration learning

Why later:
V1 does not require official social channel integration.

#### 5. WhatsApp Business Account / WhatsApp Cloud API setup
Use for:
- future WhatsApp inquiry handling
- message-based lead capture
- conversational follow-up flow

Why later:
V1 can start as a web chat only. Formal WhatsApp setup can wait until V2.

### Minimum account set for Prototype 1
- GitHub
- Google Account / Google Cloud Project
- One LLM API Provider Account

---

## Update Note
This file has been aligned with the recommended implementation stack:

- Backend: **FastAPI + SQLModel + MySQL**
- Frontend: **React.js + Tailwind CSS + Responsive GUI**
- AI / Retrieval: **LLM API + Embedding API + lightweight vector retrieval layer**

The business data can stay in MySQL, while vector retrieval can remain a lightweight separate layer during the prototype stage.

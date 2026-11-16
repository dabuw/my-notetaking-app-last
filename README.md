# NoteTaker - Personal Note Management Application

> ⚠️ 这是早期版本，已停止更新。新版见 [my-note-book](https://github.com/dabuw/my-note-book)。

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

### 📝 核心功能
- **创建笔记**: 添加带标题和丰富内容的新笔记
- **编辑笔记**: 实时编辑现有笔记内容
- **删除笔记**: 移除不再需要的笔记
- **搜索笔记**: 通过标题和内容快速查找笔记
- **自动保存**: 输入时自动保存笔记内容

### 🤖 AI 增强功能
- **智能笔记生成**: 通过 GitHub Models API 将自然语言输入转换为结构化笔记
- **日期时间解析**: 自动识别和解析"今天下午5点"等时间表达
- **标签自动提取**: AI 自动为笔记生成相关标签
- **多语言翻译**: 支持笔记内容的多语言翻译

### �️ 标签云功能
- **可视化标签统计**: 以标签云形式展示最常用的标签和主题
- **智能标签大小**: 根据使用频率调整标签大小和颜色深度
- **一键标签筛选**: 点击标签快速筛选相关笔记
- **实时统计更新**: 创建、编辑、删除笔记后自动刷新标签云
- **清晰状态指示**: 筛选时显示当前状态和快速清除选项

### �🎨 用户体验
- **响应式设计**: 完美适配桌面和移动设备
- **现代界面**: 美观的渐变设计和流畅动画
- **实时更新**: 即时反馈和更新
- **标签管理**: 支持笔记标签和分类
- **事件管理**: 支持事件日期和时间设置

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### 前端技术
- **HTML5**: 语义化标记结构
- **CSS3**: 现代样式设计，包含渐变、动画和响应式布局
- **JavaScript (ES6+)**: 交互功能和 API 通信

### 后端技术
- **Python Flask**: Web 框架和 API 端点
- **SQLAlchemy**: ORM 数据库操作
- **Flask-CORS**: 跨域资源共享支持
- **Python-dateutil**: 日期时间解析
- **Requests**: HTTP 客户端库

### 数据库
- **SQLite**: 轻量级文件数据库 (本地开发)
- **PostgreSQL**: 生产环境数据库 (Neon/Vercel)

### AI & 集成服务
- **GitHub Models**: 主要 AI 服务，支持 GPT-4o-mini 等模型进行自然语言处理和笔记生成
- **OpenAI API**: 备用 AI 服务（可选配置）

### 部署平台
- **Vercel**: 无服务器部署平台
- **Neon**: PostgreSQL 云数据库

## 📁 Project Structure

```
MyNoteTaking/
├── 📁 api/
│   └── index.py             # Vercel 部署入口点
├── 📁 database/
│   └── app.db               # SQLite 数据库文件 (本地开发)
├── 📁 src/
│   ├── 📁 models/
│   │   ├── user.py          # 用户模型和数据库配置
│   │   └── note.py          # 笔记模型和数据库结构
│   ├── 📁 routes/
│   │   ├── user.py          # 用户 API 路由
│   │   ├── note.py          # 笔记 CRUD API 端点
│   │   ├── translate.py     # 翻译 API 端点
│   │   ├── generate.py      # AI 笔记生成端点
│   │   └── tags.py          # 标签云统计和搜索端点
│   ├── 📁 static/
│   │   ├── index.html       # 前端单页应用
│   │   └── favicon.ico      # 网站图标
│   ├── call_llm_model.py    # AI 模型调用和笔记生成
│   ├── llm.py              # LLM 客户端配置
│   └── main.py              # Flask 应用入口点
├── 📁 .venv/                # Python 虚拟环境 (本地)
├── .env                     # 环境变量配置 (本地, 不提交)
├── .env.example             # 环境变量示例模板
├── .env.vercel.example      # Vercel 环境变量示例
├── .gitignore               # Git 忽略规则
├── requirements.txt         # Python 依赖列表
├── vercel.json              # Vercel 部署配置
├── VERCEL_DEPLOYMENT_GUIDE.md # Vercel 部署指南
└── README.md               # 项目说明文档
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

**注意：** 此项目依赖多个第三方库（Flask、SQLAlchemy、OpenAI SDK 等），强烈建议使用虚拟环境来隔离依赖，避免与系统 Python 或其他项目冲突。

### Installation Steps

1. **Clone or download the project**
   Navigate to the project directory in PowerShell or Command Prompt.

2. **Create virtual environment** (if not already created)
   ```powershell
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   **Windows PowerShell (推荐):**
   ```powershell
   # 如果执行策略阻止脚本运行，请先运行此命令：
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # 激活虚拟环境：
   .\.venv\Scripts\Activate.ps1
   ```
   
   **Windows Command Prompt:**
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   **Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```

   **验证激活成功：**
   激活后，你的命令行提示符前应该出现 `(.venv)` 标识，表示虚拟环境已成功激活。

4. **Install dependencies**
   ```powershell
   # 确保虚拟环境已激活 (显示 (.venv) 前缀)
   pip install -r requirements.txt
   
   # 或者直接使用虚拟环境的 Python (无需激活)
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. **设置环境变量** (AI 功能必需)
   复制 `.env.example` 为 `.env` 并配置 GitHub Token：
   ```powershell
   copy .env.example .env
   ```
   **重要：** 如需使用 AI 笔记生成功能，必须在 `.env` 文件中配置 `GITHUB_TOKEN`。
   
   获取 GitHub Token 步骤：
   1. 访问 [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
   2. 生成新的 token，勾选必要的权限
   3. 复制 token 并在 `.env` 文件中设置 `GITHUB_TOKEN=你的token`

6. **Run the application**
   ```powershell
   # 方法1: 使用激活的虚拟环境
   python src\main.py
   
   # 方法2: 直接使用虚拟环境的 Python (推荐)
   .venv\Scripts\python.exe src\main.py
   ```

7. **Access the application**
   - 打开浏览器访问 `http://localhost:5001`
   - 应用将在所有网络接口上运行 (0.0.0.0:5001)
   - 首次运行会自动创建数据库表结构

### 快速启动 (已完成初始设置)
如果你已经完成了虚拟环境设置，可以直接启动应用：

```powershell
# 1. 导航到项目目录
cd path\to\MyNoteTaking

# 2. 启动应用 (推荐方式)
.venv\Scripts\python.exe src\main.py

# 或者激活虚拟环境后启动
.\.venv\Scripts\Activate.ps1
python src\main.py
```

### 停止应用
在运行应用的终端中按 `Ctrl+C` 停止服务器。

### 常见问题解决
- **端口被占用**: 如果 5001 端口被占用，修改 `src/main.py` 中的端口号
- **虚拟环境问题**: 确保虚拟环境已正确创建和激活
- **依赖缺失**: 运行 `pip install -r requirements.txt` 重新安装依赖
- **数据库问题**: 删除 `database/app.db` 让应用重新创建数据库

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes

### Tag Cloud API
- `GET /api/tags/statistics` - Get tag usage statistics and frequency data
- `GET /api/tags/search/<tag_name>` - Search notes by specific tag

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "tags": ["work", "important"],
  "event_date": "2025-10-12",
  "event_time": "17:00",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321"
}
```

## 🧠 Generate Notes (AI)

The app includes a simple AI-assisted "Generate Notes" feature that converts natural-language input into a structured note. It extracts a concise title, full note content, optional tags, and — importantly — event date and time when present (normalized to `YYYY-MM-DD` and `HH:MM`).

Where to find it in the UI:
- In the left sidebar under "Generate Notes", enter free-form text such as "今天下午5点去野餐" and click the "Generate Notes" button. A new note will be created with the parsed title, content, tags, event date and event time populated in the editor.

API endpoint:

- `POST /api/generate-notes`

Request JSON (example):

```json
{
   "user_input": "今天下午5点去野餐",
   "language": "Chinese"
}
```

Response JSON (example):

```json
{
   "title": "今天野餐",
   "content": "今天下午5点去野餐。",
   "tags": ["野餐", "户外活动"],
   "event_date": "2025-10-12",
   "event_time": "17:00"
}
```

Notes about parsing:
- The backend uses `src.call_llm_model.process_user_notes` which attempts to extract structured fields using an LLM and falls back to deterministic date/time parsing for many common Chinese/English expressions (e.g. 今天/明天/下午5点/5pm).
- The frontend does additional normalization so the values are compatible with `input[type=date]` (`YYYY-MM-DD`) and `input[type=time]` (`HH:MM`).

Quick PowerShell tests (run from project root):

```powershell
# 1) Directly call the LLM parsing function (no server required)
.venv\Scripts\python.exe -c "import sys,json; sys.path.append('src'); from call_llm_model import process_user_notes; print(json.dumps(process_user_notes('Chinese','今天下午5点去野餐'), indent=2, ensure_ascii=False))"

# 2) Call the API using Flask test client (no server required)
.venv\Scripts\python.exe -c "import sys,json; sys.path.append('src'); from main import app; c=app.test_client(); r=c.post('/api/generate-notes', json={'user_input':'今天下午5点去野餐','language':'Chinese'}); print(r.status_code); print(json.dumps(r.get_json(), ensure_ascii=False, indent=2))"
```


## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table
```sql
CREATE TABLE note (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,                    -- JSON array of tags
    event_date DATE,             -- Optional event date
    event_time TIME,             -- Optional event time
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment

The application is configured for easy deployment with:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Persistent SQLite database

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions

### Database Configuration
- Database file: `database/app.db` (created in project root)
- Automatic table creation on first run
- SQLAlchemy ORM for database operations

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**


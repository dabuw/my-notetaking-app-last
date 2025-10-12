# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **SQLite**: Lightweight, file-based database for data persistence

## 📁 Project Structure

```
MyNoteTaking/
├── src/
│   ├── models/
│   │   ├── user.py          # User model and database setup
│   │   └── note.py          # Note model with database schema
│   ├── routes/
│   │   ├── user.py          # User API routes (template)
│   │   ├── note.py          # Note CRUD API endpoints
│   │   ├── translate.py     # Translation API endpoints
│   │   └── generate.py      # AI note generation endpoints
│   ├── static/
│   │   └── index.html       # Frontend application
│   ├── call_llm_model.py    # LLM integration for note generation
│   ├── llm.py              # LLM client configuration
│   └── main.py              # Flask application entry point
├── database/
│   └── app.db               # SQLite database file
├── .venv/                   # Python virtual environment
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   Navigate to the project directory in PowerShell or Command Prompt.

2. **Create virtual environment**
   ```powershell
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   **Windows PowerShell:**
   ```powershell
   # If execution policy blocks the script, run this first:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   
   # Then activate the environment:
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

4. **Install dependencies**
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. **Run the application**
   ```powershell
   .venv\Scripts\python.exe src\main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`
   - The application will be running on all network interfaces (0.0.0.0:5001)

### Quick Start (Windows)
If you already have the virtual environment set up, you can start the application directly:

```powershell
# Navigate to project directory
cd D:\workspace\lab2\MyNoteTaking

# Start the application (virtual environment will be used automatically)
.venv\Scripts\python.exe src\main.py
```

### Stopping the Application
Press `Ctrl+C` in the terminal where the application is running to stop the server.

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes

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


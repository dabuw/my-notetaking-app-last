#!/usr/bin/env python3
"""
测试笔记 API 功能
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from src.models.user import db
from src.routes.note import note_bp
from src.models.note import Note
from dotenv import load_dotenv

load_dotenv()

def create_test_app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # 启用 CORS
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(note_bp, url_prefix='/api')
    
    # 配置数据库
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # 确保 SSL 模式
        if database_url.startswith('postgres') and 'sslmode=' not in database_url:
            sep = '&' if '?' in database_url else '?'
            database_url = f"{database_url}{sep}sslmode=require"
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # 本地 SQLite 数据库
        ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化数据库
    db.init_app(app)
    
    return app

def test_notes_api():
    """测试笔记 API"""
    print("🧪 测试笔记 API 功能\n")
    
    app = create_test_app()
    
    with app.app_context():
        try:
            # 创建表（如果不存在）
            db.create_all()
            print("✅ 数据库表创建/验证成功")
            
            # 查询所有笔记
            notes = Note.query.all()
            print(f"📝 数据库中的笔记数量: {len(notes)}")
            
            if notes:
                print("\n📋 现有笔记:")
                for i, note in enumerate(notes[:5], 1):  # 只显示前5个
                    print(f"   {i}. {note.title[:50]}{'...' if len(note.title) > 50 else ''}")
                    print(f"      创建时间: {note.created_at}")
                    print(f"      更新时间: {note.updated_at}")
                    if note.tags:
                        tags = note.get_tags()
                        print(f"      标签: {', '.join(tags) if tags else '无'}")
                    print()
                
                if len(notes) > 5:
                    print(f"   ... 还有 {len(notes) - 5} 个笔记")
            else:
                print("📝 数据库中暂无笔记")
            
            # 测试创建新笔记
            print("\n🧪 测试创建新笔记...")
            test_note = Note(
                title="测试笔记",
                content="这是一个测试笔记内容"
            )
            test_note.set_tags(['测试', 'API'])
            
            db.session.add(test_note)
            db.session.commit()
            
            print(f"✅ 测试笔记创建成功，ID: {test_note.id}")
            
            # 测试查询
            retrieved_note = Note.query.get(test_note.id)
            if retrieved_note:
                print(f"✅ 笔记查询成功: {retrieved_note.title}")
                print(f"   内容: {retrieved_note.content[:100]}...")
                print(f"   标签: {retrieved_note.get_tags()}")
            else:
                print("❌ 笔记查询失败")
            
            # 清理测试数据
            db.session.delete(test_note)
            db.session.commit()
            print("🗑️  测试数据已清理")
            
            return True
            
        except Exception as e:
            print(f"❌ API 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_notes_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 笔记 API 功能测试成功！")
    else:
        print("💥 笔记 API 功能测试失败！")
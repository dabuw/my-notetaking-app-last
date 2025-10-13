#!/usr/bin/env python3
"""
测试数据库连接脚本
"""
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

# 加载环境变量
load_dotenv()

def test_database_connection():
    """测试数据库连接"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ 错误: 未找到 DATABASE_URL 环境变量")
        return False
    
    print(f"📊 正在测试数据库连接...")
    print(f"🔗 数据库 URL: {database_url[:50]}...")
    
    try:
        # 解析数据库 URL
        parsed = urlparse(database_url)
        print(f"🏠 主机: {parsed.hostname}")
        print(f"🔌 端口: {parsed.port}")
        print(f"🗄️  数据库名: {parsed.path[1:]}")  # 去掉开头的 '/'
        print(f"👤 用户名: {parsed.username}")
        
        # 尝试连接数据库
        print("\n🔄 正在连接数据库...")
        conn = psycopg2.connect(database_url)
        
        # 测试基本查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ 数据库连接成功!")
        print(f"📋 PostgreSQL 版本: {version[0]}")
        
        # 测试表是否存在
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📊 现有表格 ({len(tables)} 个):")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("📊 数据库中暂无表格")
        
        # 如果有 note 表，查询记录数
        cursor.execute("""
            SELECT COUNT(*) as table_count 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'note';
        """)
        note_table_exists = cursor.fetchone()[0] > 0
        
        if note_table_exists:
            cursor.execute("SELECT COUNT(*) FROM note;")
            note_count = cursor.fetchone()[0]
            print(f"📝 Note 表中的记录数: {note_count}")
        else:
            print("📝 Note 表尚未创建")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return False

def test_sqlalchemy_connection():
    """使用 SQLAlchemy 测试连接"""
    try:
        from sqlalchemy import create_engine, text
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ 未找到 DATABASE_URL")
            return False
        
        print("\n🔧 使用 SQLAlchemy 测试连接...")
        
        # 创建引擎
        engine = create_engine(database_url)
        
        # 测试连接
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test;"))
            test_value = result.fetchone()[0]
            print(f"✅ SQLAlchemy 连接成功! 测试查询结果: {test_value}")
            
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy 连接失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 数据库连接测试开始\n")
    print("=" * 50)
    
    # 测试原始 psycopg2 连接
    psycopg2_success = test_database_connection()
    
    print("\n" + "=" * 50)
    
    # 测试 SQLAlchemy 连接
    sqlalchemy_success = test_sqlalchemy_connection()
    
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print(f"   psycopg2 连接: {'✅ 成功' if psycopg2_success else '❌ 失败'}")
    print(f"   SQLAlchemy 连接: {'✅ 成功' if sqlalchemy_success else '❌ 失败'}")
    
    if psycopg2_success and sqlalchemy_success:
        print("\n🎉 数据库连接完全正常！")
    elif psycopg2_success or sqlalchemy_success:
        print("\n⚠️  部分连接成功，可能需要进一步调试")
    else:
        print("\n💥 数据库连接完全失败，请检查配置")
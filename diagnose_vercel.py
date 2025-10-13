#!/usr/bin/env python3
"""
Vercel 部署诊断脚本
用于检测可能导致 Serverless 函数崩溃的问题
"""
import os
import sys
import json
import traceback
from datetime import datetime

def diagnose_vercel_deployment():
    """诊断 Vercel 部署问题"""
    print("🔍 Vercel 部署诊断开始")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # 1. 检查 Python 环境
    print("📋 Python 环境信息:")
    print(f"   Python 版本: {sys.version}")
    print(f"   平台: {sys.platform}")
    print(f"   工作目录: {os.getcwd()}")
    print()
    
    # 2. 检查关键文件存在性
    print("📁 关键文件检查:")
    critical_files = [
        'api/index.py',
        'vercel.json', 
        'requirements.txt',
        'src/main.py',
        'src/models/note.py',
        'src/routes/note.py',
        'src/static/index.html'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - 文件缺失")
            issues.append(f"Missing file: {file_path}")
    print()
    
    # 3. 检查环境变量
    print("🔧 环境变量检查:")
    required_env_vars = [
        'DATABASE_URL',
        'SECRET_KEY', 
        'ZHIPUAI_API_KEY'
    ]
    
    for var in required_env_vars:
        value = os.environ.get(var)
        if value:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"   ✅ {var}: {masked_value}")
        else:
            print(f"   ⚠️  {var}: 未设置")
            warnings.append(f"Environment variable {var} not set")
    print()
    
    # 4. 测试模块导入
    print("📦 模块导入测试:")
    modules_to_test = [
        'flask',
        'flask_cors', 
        'flask_sqlalchemy',
        'psycopg2',
        'requests',
        'openai',
        'dateutil'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            issues.append(f"Cannot import {module}: {e}")
    print()
    
    # 5. 测试数据库连接
    print("🗄️  数据库连接测试:")
    try:
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            import psycopg2
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            print(f"   ✅ 数据库连接成功: {result[0]}")
        else:
            print("   ⚠️  DATABASE_URL 未设置，将使用内存数据库")
            warnings.append("Using in-memory database")
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        issues.append(f"Database connection failed: {e}")
    print()
    
    # 6. 测试 Flask 应用初始化
    print("🌐 Flask 应用测试:")
    try:
        # 临时添加路径
        sys.path.insert(0, os.path.dirname(__file__))
        
        from api.index import app
        with app.app_context():
            print("   ✅ Flask 应用初始化成功")
            
            # 测试基本路由
            with app.test_client() as client:
                response = client.get('/api/health')
                if response.status_code == 200:
                    print("   ✅ 健康检查端点正常")
                else:
                    print(f"   ⚠️  健康检查端点返回: {response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Flask 应用初始化失败: {e}")
        issues.append(f"Flask app initialization failed: {e}")
        traceback.print_exc()
    print()
    
    # 7. 生成诊断报告
    print("📊 诊断总结:")
    if not issues and not warnings:
        print("   🎉 所有检查通过！部署应该可以正常工作")
    else:
        if issues:
            print(f"   ❌ 发现 {len(issues)} 个严重问题:")
            for i, issue in enumerate(issues, 1):
                print(f"      {i}. {issue}")
        
        if warnings:
            print(f"   ⚠️  发现 {len(warnings)} 个警告:")
            for i, warning in enumerate(warnings, 1):
                print(f"      {i}. {warning}")
    
    # 8. 生成修复建议
    if issues:
        print("\n🔧 修复建议:")
        for issue in issues:
            if "Missing file" in issue:
                print("   - 确保所有必需文件都已提交到 Git 仓库")
            elif "Cannot import" in issue:
                print("   - 检查 requirements.txt 是否包含所有依赖")
                print("   - 确保包版本与 Python 3.9+ 兼容")
            elif "Database connection" in issue:
                print("   - 在 Vercel 项目设置中正确配置 DATABASE_URL")
                print("   - 确保数据库允许来自 Vercel IP 的连接")
            elif "Flask app initialization" in issue:
                print("   - 检查 api/index.py 中的导入路径")
                print("   - 确保所有环境变量在 Vercel 中正确设置")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = diagnose_vercel_deployment()
    sys.exit(0 if success else 1)
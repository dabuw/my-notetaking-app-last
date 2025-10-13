#!/usr/bin/env python3
"""
简单的 HTTP API 测试
"""
import requests
import json

def test_api():
    """测试 API 端点"""
    base_url = "http://localhost:5001/api"
    
    try:
        print("🧪 测试 /api/notes 端点...")
        response = requests.get(f"{base_url}/notes", timeout=10)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            notes = response.json()
            print(f"✅ 成功获取 {len(notes)} 个笔记")
            
            if notes:
                print("\n📋 前3个笔记:")
                for i, note in enumerate(notes[:3], 1):
                    print(f"   {i}. {note.get('title', 'No Title')}")
                    print(f"      ID: {note.get('id')}")
                    print(f"      创建时间: {note.get('created_at')}")
                    print()
            else:
                print("📝 数据库中暂无笔记")
                
        else:
            print(f"❌ API 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 服务器可能未启动或端口不正确")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_api()
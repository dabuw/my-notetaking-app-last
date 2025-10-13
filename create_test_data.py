#!/usr/bin/env python3
"""
简单测试：创建一些带标签的测试笔记，用于验证标签云功能
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def create_test_notes():
    """创建一些测试笔记用于展示标签云功能"""
    test_notes = [
        {
            "title": "工作会议记录",
            "content": "今天的项目会议讨论了新功能开发计划。",
            "tags": ["工作", "会议", "项目"]
        },
        {
            "title": "学习笔记",
            "content": "今天学习了Python Flask框架的基础知识。",
            "tags": ["学习", "Python", "Flask", "技术"]
        },
        {
            "title": "购物清单",
            "content": "需要购买：面包、牛奶、鸡蛋、水果。",
            "tags": ["生活", "购物"]
        },
        {
            "title": "旅行计划",
            "content": "下周末计划去北京旅游，需要预定酒店和车票。",
            "tags": ["旅行", "北京", "计划"]
        },
        {
            "title": "读书笔记",
            "content": "《代码大全》读书心得：良好的代码结构很重要。",
            "tags": ["读书", "学习", "技术"]
        },
        {
            "title": "健身计划",
            "content": "制定了新的健身计划：每周3次，每次1小时。",
            "tags": ["健康", "健身", "计划"]
        }
    ]
    
    print("🚀 Creating test notes for tag cloud demo...")
    created_notes = []
    
    for note_data in test_notes:
        try:
            response = requests.post(f"{BASE_URL}/api/notes", json=note_data)
            if response.status_code == 200:
                note = response.json()
                created_notes.append(note)
                print(f"✅ Created: {note['title']} (Tags: {', '.join(note.get('tags', []))})")
            else:
                print(f"❌ Failed to create: {note_data['title']}")
        except Exception as e:
            print(f"❌ Error creating note: {e}")
    
    return created_notes

def verify_tag_cloud():
    """验证标签云API是否正常工作"""
    try:
        response = requests.get(f"{BASE_URL}/api/tags/statistics")
        if response.status_code == 200:
            stats = response.json()
            print(f"\n📊 Tag Cloud Statistics:")
            print(f"   - Total unique tags: {stats.get('unique_tags', 0)}")
            print(f"   - Total tag uses: {stats.get('total_tags', 0)}")
            
            if stats.get('tag_counts'):
                print("   - Popular tags:")
                for tag in stats['tag_counts'][:5]:
                    print(f"     * {tag['tag']}: {tag['count']} uses")
            return True
        else:
            print("❌ Failed to get tag statistics")
            return False
    except Exception as e:
        print(f"❌ Error verifying tag cloud: {e}")
        return False

def main():
    print("🎯 Tag Cloud Feature Test Setup")
    print("=" * 40)
    
    # Create test notes
    created_notes = create_test_notes()
    
    if created_notes:
        print(f"\n✅ Successfully created {len(created_notes)} test notes")
        
        # Verify tag cloud
        if verify_tag_cloud():
            print("\n🎉 Tag cloud is working! Open http://localhost:5001 to see it in action.")
            print("\n💡 Test these features:")
            print("   1. Click on tags in the tag cloud to filter notes")
            print("   2. Notice how the editor clears when filtering")
            print("   3. Click 'Clear Filter' or select a note to exit filter mode")
            print("   4. Create new notes and see tag cloud update automatically")
        else:
            print("\n⚠️  Tag cloud verification failed")
    else:
        print("\n❌ No test notes were created")

if __name__ == "__main__":
    main()
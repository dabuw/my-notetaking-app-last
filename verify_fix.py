#!/usr/bin/env python3
"""
验证日期解析修复效果的对比测试
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.call_llm_model import process_user_notes
from datetime import date, timedelta

def test_specific_cases():
    """测试具体的问题案例"""
    print("🧪 验证日期解析修复效果")
    print(f"📅 今天: {date.today()} ({date.today().strftime('%Y年%m月%d日')})")
    print(f"📅 明天: {date.today() + timedelta(days=1)} ({(date.today() + timedelta(days=1)).strftime('%Y年%m月%d日')})")
    print(f"📅 后天: {date.today() + timedelta(days=2)} ({(date.today() + timedelta(days=2)).strftime('%Y年%m月%d日')})")
    print("=" * 60)
    
    # 问题案例：用户输入"后天下午9点去上跆拳道课"
    test_input = "后天下午9点去上跆拳道课。"
    expected_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')  # 2025-10-15
    
    print(f"📝 测试输入: {test_input}")
    print(f"🎯 期望日期: {expected_date} (后天)")
    print()
    
    try:
        result = process_user_notes("Chinese", test_input)
        
        print("✅ AI 解析结果:")
        print(f"   📌 标题: {result.get('Title', 'N/A')}")
        print(f"   📅 事件日期: {result.get('Event_Date', 'N/A')}")
        print(f"   ⏰ 事件时间: {result.get('Event_Time', 'N/A')}")
        print(f"   🏷️  标签: {result.get('Tags', [])}")
        
        actual_date = result.get('Event_Date')
        
        if actual_date == expected_date:
            print(f"\n🎉 ✅ 修复成功！日期解析正确: {actual_date}")
            print("   后天日期现在正确解析为15号，而不是14号")
        else:
            print(f"\n❌ 修复失败！日期解析错误:")
            print(f"   期望: {expected_date} (后天)")
            print(f"   实际: {actual_date}")
        
        # 验证时间解析
        expected_time = "21:00"  # 下午9点 = 21:00
        actual_time = result.get('Event_Time')
        
        if actual_time == expected_time:
            print(f"🕘 时间解析正确: {actual_time} (下午9点)")
        else:
            print(f"⚠️  时间解析: 期望 {expected_time}, 实际 {actual_time}")
            
    except Exception as e:
        print(f"❌ 测试执行失败: {e}")
        import traceback
        traceback.print_exc()

def test_other_cases():
    """测试其他相关案例"""
    print("\n" + "=" * 60)
    print("🔍 测试其他相关日期表达")
    
    test_cases = [
        ("今天晚上8点", "2025-10-13", "20:00"),
        ("明天早上7点", "2025-10-14", "07:00"),
        ("大后天下午3点", "2025-10-16", "15:00")
    ]
    
    for i, (input_text, expected_date, expected_time) in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {input_text}")
        try:
            result = process_user_notes("Chinese", input_text)
            actual_date = result.get('Event_Date')
            actual_time = result.get('Event_Time')
            
            date_ok = actual_date == expected_date
            time_ok = actual_time == expected_time
            
            print(f"   📅 日期: {actual_date} {'✅' if date_ok else '❌'} (期望: {expected_date})")
            print(f"   ⏰ 时间: {actual_time} {'✅' if time_ok else '❌'} (期望: {expected_time})")
            
        except Exception as e:
            print(f"   ❌ 解析失败: {e}")

if __name__ == "__main__":
    test_specific_cases()
    test_other_cases()
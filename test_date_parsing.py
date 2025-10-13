#!/usr/bin/env python3
"""
测试日期解析修复效果
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.call_llm_model import process_user_notes, parse_date_time_fallback
from datetime import date, timedelta
import json

def test_date_parsing():
    """测试日期解析功能"""
    print("🧪 测试日期解析修复效果")
    print(f"📅 当前日期: {date.today()}")
    print(f"📅 明天日期: {date.today() + timedelta(days=1)}")
    print(f"📅 后天日期: {date.today() + timedelta(days=2)}")
    print("-" * 50)
    
    # 测试用例
    test_cases = [
        "今天下午5点去跆拳道",
        "明天上午9点开会",
        "后天下午9点去上跆拳道课",
        "大后天晚上8点看电影",
        "下周一下午2点见面"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🔍 测试 {i}: {test_input}")
        
        try:
            # 测试 LLM 解析
            result = process_user_notes("Chinese", test_input)
            
            print(f"✅ LLM 解析结果:")
            print(f"   标题: {result.get('Title', 'N/A')}")
            print(f"   事件日期: {result.get('Event_Date', 'N/A')}")
            print(f"   事件时间: {result.get('Event_Time', 'N/A')}")
            
            if 'error' in result:
                print(f"⚠️  LLM 解析失败: {result['error']}")
            
            # 测试 fallback 解析
            fallback_date, fallback_time = parse_date_time_fallback(test_input)
            print(f"🔄 Fallback 解析:")
            print(f"   事件日期: {fallback_date}")
            print(f"   事件时间: {fallback_time}")
            
            # 验证"后天"的解析
            if "后天" in test_input:
                expected_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
                actual_date = result.get('Event_Date') or fallback_date
                
                if actual_date == expected_date:
                    print(f"🎉 后天日期解析正确: {actual_date}")
                else:
                    print(f"❌ 后天日期解析错误: 期望 {expected_date}, 实际 {actual_date}")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_date_parsing()
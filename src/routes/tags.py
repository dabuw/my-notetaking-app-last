from flask import Blueprint, jsonify
from collections import Counter
from src.models.note import Note
import json

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/api/tags/statistics', methods=['GET'])
def get_tags_statistics():
    """获取所有笔记中标签的使用统计信息"""
    try:
        # 获取所有笔记
        notes = Note.query.all()
        
        # 收集所有标签
        all_tags = []
        for note in notes:
            tags = note.get_tags()
            if tags:
                all_tags.extend(tags)
        
        if not all_tags:
            return jsonify({
                'tag_counts': [],
                'total_tags': 0,
                'unique_tags': 0,
                'most_popular': None
            })
        
        # 统计标签频次
        tag_counter = Counter(all_tags)
        
        # 准备返回数据
        tag_counts = []
        max_count = max(tag_counter.values()) if tag_counter else 0
        min_count = min(tag_counter.values()) if tag_counter else 0
        
        for tag, count in tag_counter.most_common():
            # 计算标签的权重（相对于最大使用频次）
            weight = count / max_count if max_count > 0 else 1
            
            tag_counts.append({
                'tag': tag,
                'count': count,
                'weight': weight,
                'percentage': round((count / len(all_tags)) * 100, 1) if all_tags else 0
            })
        
        # 统计信息
        statistics = {
            'tag_counts': tag_counts,
            'total_tags': len(all_tags),  # 总标签数（包括重复）
            'unique_tags': len(tag_counter),  # 唯一标签数
            'most_popular': tag_counter.most_common(1)[0] if tag_counter else None,
            'distribution': {
                'max_count': max_count,
                'min_count': min_count,
                'avg_count': round(sum(tag_counter.values()) / len(tag_counter), 2) if tag_counter else 0
            }
        }
        
        return jsonify(statistics)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get tag statistics: {str(e)}'}), 500

@tags_bp.route('/api/tags/search/<tag_name>', methods=['GET'])
def search_notes_by_tag(tag_name):
    """根据标签搜索相关笔记"""
    try:
        notes = Note.query.all()
        matching_notes = []
        
        for note in notes:
            tags = note.get_tags()
            if tags and tag_name.lower() in [t.lower() for t in tags]:
                matching_notes.append(note.to_dict())
        
        return jsonify({
            'tag': tag_name,
            'count': len(matching_notes),
            'notes': matching_notes
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to search notes by tag: {str(e)}'}), 500
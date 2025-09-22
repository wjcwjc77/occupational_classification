import csv
import json
import re

def parse_occupation_code(code):
    """解析职业代码，返回层级信息"""
    clean_code = re.sub(r'\(GBM\s*\d+\)', '', code).strip()
    
    parts = clean_code.split('-')
    
    if len(parts) == 1:
        # 大类：如 "1"
        return {
            'level': 'major',
            'major': parts[0],
            'medium': None,
            'small': None,
            'detail': None,
            'code': clean_code
        }
    elif len(parts) == 2:
        # 中类：如 "1-01"
        return {
            'level': 'medium',
            'major': parts[0],
            'medium': parts[1],
            'small': None,
            'detail': None,
            'code': clean_code
        }
    elif len(parts) == 3:
        # 小类：如 "1-01-00"
        return {
            'level': 'small',
            'major': parts[0],
            'medium': parts[1],
            'small': parts[2],
            'detail': None,
            'code': clean_code
        }
    elif len(parts) == 4:
        # 细类：如 "1-01-00-00"
        return {
            'level': 'detail',
            'major': parts[0],
            'medium': parts[1],
            'small': parts[2],
            'detail': parts[3],
            'code': clean_code
        }
    else:
        return None

def read_csv_files():
    all_data = []
    
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                all_data.append({
                    'code': row[0].strip(),
                    'name': row[1].strip()
                })

    
    return all_data

def build_tree_structure(data):
    """构建树状结构"""
    tree = {}
    
    for item in data:
        parsed = parse_occupation_code(item['code'])
        if not parsed:
            continue
            
        major_code = parsed['major']
        medium_code = parsed['medium']
        small_code = parsed['small']
        detail_code = parsed['detail']
        
        # 确保大类存在
        if major_code not in tree:
            tree[major_code] = {
                'code': major_code,
                'name': '',
                'children': {}
            }
        
        # 如果是中类或更细的层级
        if medium_code:
            if medium_code not in tree[major_code]['children']:
                tree[major_code]['children'][medium_code] = {
                    'code': f"{major_code}-{medium_code}",
                    'name': '',
                    'children': {}
                }
            
            # 如果是小类或更细的层级
            if small_code:
                if small_code not in tree[major_code]['children'][medium_code]['children']:
                    tree[major_code]['children'][medium_code]['children'][small_code] = {
                        'code': f"{major_code}-{medium_code}-{small_code}",
                        'name': '',
                        'children': {}
                    }
                
                # 如果是细类
                if detail_code:
                    if detail_code not in tree[major_code]['children'][medium_code]['children'][small_code]['children']:
                        tree[major_code]['children'][medium_code]['children'][small_code]['children'][detail_code] = {
                            'code': f"{major_code}-{medium_code}-{small_code}-{detail_code}",
                            'name': '',
                            'children': {}
                        }
    
    # 填充名称
    for item in data:
        parsed = parse_occupation_code(item['code'])
        if not parsed:
            continue
            
        major_code = parsed['major']
        medium_code = parsed['medium']
        small_code = parsed['small']
        detail_code = parsed['detail']
        
        if parsed['level'] == 'major':
            tree[major_code]['name'] = item['name']
        elif parsed['level'] == 'medium':
            tree[major_code]['children'][medium_code]['name'] = item['name']
        elif parsed['level'] == 'small':
            tree[major_code]['children'][medium_code]['children'][small_code]['name'] = item['name']
        elif parsed['level'] == 'detail':
            tree[major_code]['children'][medium_code]['children'][small_code]['children'][detail_code]['name'] = item['name']
    
    return tree

def convert_to_list_format(tree):
    """将树状结构转换为列表格式"""
    result = []
    
    for major_code in sorted(tree.keys()):
        major_item = tree[major_code]
        major_node = {
            'code': major_item['code'],
            'name': major_item['name'],
            'level': 'major',
            'children': []
        }
        
        for medium_code in sorted(major_item['children'].keys()):
            medium_item = major_item['children'][medium_code]
            medium_node = {
                'code': medium_item['code'],
                'name': medium_item['name'],
                'level': 'medium',
                'children': []
            }
            
            for small_code in sorted(medium_item['children'].keys()):
                small_item = medium_item['children'][small_code]
                small_node = {
                    'code': small_item['code'],
                    'name': small_item['name'],
                    'level': 'small',
                    'children': []
                }
                
                for detail_code in sorted(small_item['children'].keys()):
                    detail_item = small_item['children'][detail_code]
                    detail_node = {
                        'code': detail_item['code'],
                        'name': detail_item['name'],
                        'level': 'detail',
                        'children': []
                    }
                    small_node['children'].append(detail_node)
                
                medium_node['children'].append(small_node)
            
            major_node['children'].append(medium_node)
        
        result.append(major_node)
    
    return result

def main():
    data = read_csv_files()
    
    tree = build_tree_structure(data)
    
    result = convert_to_list_format(tree)
    
    with open('occupation_tree.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print('done')

if __name__ == "__main__":
    main()

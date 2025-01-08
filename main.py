import json

# 文件名
m3u_filename = 'm3u/20250108.m3u'
json_filename = 'json/20250108.json'


# 将M3U文件内容转换为JSON格式
def m3u_to_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    json_data = {"lives": []}
    current_group = {}
    current_channel_list = []

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            parts = line.split(',')
            channel_name = parts[-1]
            group_title_part = parts[0]
            group_name = group_title_part.split('group-title="')[1].split('"')[
                0] if 'group-title="' in group_title_part else "未分类"

            # 新建组
            if not current_group or current_group["group"] != group_name:
                if current_group:
                    current_group["channels"] = current_channel_list
                    json_data["lives"].append(current_group)
                current_group = {"group": group_name}
                current_channel_list = []

            # 新建频道
            channel = {"name": channel_name, "urls": []}
            current_channel_list.append(channel)

        elif line.startswith("http://") or line.startswith("https://"):
            # 添加URL到最近的频道
            if current_channel_list:
                current_channel_list[-1]["urls"].append(line)

    # 添加最后一个组
    if current_group and current_channel_list:
        current_group["channels"] = current_channel_list
        json_data["lives"].append(current_group)

    return json_data


# 读取M3U文件并转换为JSON
json_result = m3u_to_json(m3u_filename)

# 将结果保存为JSON文件
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(json_result, json_file, ensure_ascii=False, indent=4)

print(f"JSON文件已成功保存为 {json_filename}")

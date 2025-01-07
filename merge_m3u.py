# m3u 文件合并与分组脚本，支持 group-title
def merge_and_group_m3u_with_group_title(input_file, output_file):
    # 定义存储结果的字典
    channels = {}

    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 处理 m3u 文件
    current_channel = None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # 提取频道名称（逗号后的文本）
            current_channel = line.split(",", 1)[-1].strip()
            if current_channel not in channels:
                channels[current_channel] = {"info": line, "urls": []}
        elif line and not line.startswith("#"):  # 处理 URL
            if current_channel:
                channels[current_channel]["urls"].append(line)

    # 分组逻辑
    grouped_channels = {"央视": [], "卫视": [], "ihot": [], "其他": []}
    for channel, data in channels.items():
        if channel.startswith("CCTV"):
            grouped_channels["央视"].append(data)
        elif channel.endswith("卫视"):
            grouped_channels["卫视"].append(data)
        elif "ihot" in channel.lower():
            grouped_channels["ihot"].append(data)
        else:
            grouped_channels["其他"].append(data)

    # 生成分组后的 m3u 内容
    merged_content = "#EXTM3U\n"
    for group, group_channels in grouped_channels.items():
        for data in group_channels:
            # 修改频道信息，添加 group-title 属性
            updated_info = data["info"].replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{group}"')
            merged_content += f"{updated_info}\n" + "\n".join(data["urls"]) + "\n"

    # 保存到新文件
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_content)


# 使用示例
input_file = 'm3u/20241116.m3u'
output_file = 'm3u/20241116-.new.m3u'
merge_and_group_m3u_with_group_title(input_file, output_file)

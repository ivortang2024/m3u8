import json


def json_to_m3u(json_path, m3u_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(m3u_path, 'w', encoding='utf-8') as m3u_file:
        m3u_file.write("#EXTM3U\n")

        for group in data["lives"]:
            group_name = group.get("group", "General")

            for channel in group["channels"]:
                channel_name = channel.get("name", "Unknown")

                for url in channel["urls"]:
                    # M3U格式行：#EXTINF:-1 group-title="GroupName", ChannelName
                    m3u_file.write(f'#EXTINF:-1 group-title="{group_name}",{channel_name}\n')
                    m3u_file.write(f'{url}\n')

    print(f"M3U 文件已成功保存为 {m3u_path}")


# 调用函数转换 JSON 为 M3U
json_to_m3u("json/iptv20241103_chengren.json", "m3u/output.m3u")

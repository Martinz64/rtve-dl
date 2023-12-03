import requests
import json
import sys
import os
import re
import ztnr_rtve

if not (len(sys.argv) == 3 or len(sys.argv) == 2):
    print("wrong arguments.",len(sys.argv))
    sys.exit(1)

asset_id = sys.argv[1]

ztnr_url = f"https://api-ztnr.rtve.es/api/videos/{asset_id}.json"

program_data = requests.get(ztnr_url)
program_data_json = json.loads(program_data.content)
title = program_data_json["page"]["items"][0]["longTitle"].replace(":", "")
desc = program_data_json["page"]["items"][0]["shortDescription"]

subtitles_ref_url = program_data_json["page"]["items"][0]["subtitleRef"]
sub_url = None
if subtitles_ref_url:
    subtitles = requests.get(subtitles_ref_url)
    subtitles_json = json.loads(subtitles.content)
    sub_url = subtitles_json["page"]["items"][0]["src"]


print(f"[i] Título: {title}")
print(f"[i] Descripcion: {desc}")
print(f"[i] Url subtitulos: {sub_url}")


urls = ztnr_rtve.get_urls(asset_id)
#primer_mp4 = [url for url in urls if b'.m3u8' in url][0].decode('utf-8')
#mp4_limpio = primer_mp4.split("/video.m3u8")[0]

mp4_correcto = [url for url in urls if not b'.mp4/' in url][0].decode('utf-8')

print(f"[i] Url vídeo: {mp4_correcto}")
print("Descargando video...")
os.system(f"wget -O \"{title}.mp4\" {mp4_correcto}")

if sub_url:
    print("Downloading subtitles...")
    os.system(f"wget -O \"{title}.vtt\" {sub_url}")

print("Done")

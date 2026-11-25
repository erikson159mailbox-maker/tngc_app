import asyncio
import json
import os
import edge_tts

# 讀取同工發布的節目腳本清單
with open("audio/episodes.json", "r", encoding="utf-8") as f:
    episodes = json.load(f)

os.makedirs("audio/mp3", exist_ok=True)

async def synthesize_episode(ep):
    output_path = f"audio/mp3/{ep['id']}.mp3"
    if os.path.exists(output_path):
        return  # 已生成過的音檔不重複轉檔

    lines = [line.strip() for line in ep["script"].split("\n") if "：" in line]
    audio_chunks = bytearray()

    for line in lines:
        speaker, text = line.split("：", 1)
        clean_text = text.replace("「", "").replace("」", "").strip()
        # 陳哥用台灣溫暖男聲(雲哲)，小恩用台灣親切女聲(曉臻)
        voice = "zh-TW-YunJheNeural" if "陳哥" in speaker else "zh-TW-HsiaoChenNeural"
        rate = "-4%" if "陳哥" in speaker else "-2%"

        communicate = edge_tts.Communicate(clean_text, voice, rate=rate)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.extend(chunk["data"])

    with open(output_path, "wb") as out_f:
        out_f.write(audio_chunks)
    print(f"✅ 已產出台灣自然人聲 MP3：{output_path}")

async def main():
    for ep in episodes:
        await synthesize_episode(ep)

if __name__ == "__main__":
    asyncio.run(main())

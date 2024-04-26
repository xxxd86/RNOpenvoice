import os
import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter


def rundemo():
    ckpt_converter = 'checkpoints/converter'
    # 使用CPU进行计算
    device = 'cpu'
    output_dir = 'outputs'

    # 加载基础模型
    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    # 训练音频
    reference_speaker = 'resources/demo_speaker0.mp3'
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed',
                                                vad=True)
    # TTS配置
    ckpt_base = 'checkpoints/base_speakers/ZH'
    base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
    base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')
    source_se = torch.load(f'{ckpt_base}/zh_default_se.pth').to(device)
    save_path = f'{output_dir}/output_chinese.wav'
    text = "哆啦A梦是一个可以提供大家使用签到的软件"
    src_path = f'{output_dir}/tmp.wav'
    # TTS转换，speed为语速
    base_speaker_tts.tts(text, src_path, speaker='default', language='Chinese', speed=1)
    # 数字水印内容
    encode_message = "@Print_Lin"
    # 运行转换
    tone_color_converter.convert(
        audio_src_path=src_path,
        src_se=source_se,
        tgt_se=target_se,
        output_path=save_path,
        message=encode_message)


def readAllText():
    f2 = open("text.txt", encoding='utf-8')
    lines = f2.readlines()
    result = ""
    for line3 in lines:
        result += line3
    return result


if __name__ == '__main__':
    rundemo()

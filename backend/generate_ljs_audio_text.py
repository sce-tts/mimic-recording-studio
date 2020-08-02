import sys

from pathlib import Path
import random
from unicodedata import normalize
from pydub import AudioSegment

USER_UUID = sys.argv[1]

audio_path = Path('.') / 'audio_files' / USER_UUID
ljs_path = Path('.') / 'filelists'
wav_path = ljs_path / 'wavs'

ljs_path.mkdir()
wav_path.mkdir()

audio_data = []

print(f"audio_path: {audio_path}")
print(f"ljs_path: {ljs_path}")

with open(audio_path / f'{USER_UUID}-metadata.txt', 'r', encoding='utf8') as metadata:
    for line in metadata:
        if not line:
            continue
        data = line.split('|')

        original_wav_path = audio_path / data[0]

        if not original_wav_path.is_file():
            continue

        print(f"Converting {str(original_wav_path)}...")

        sound = AudioSegment.from_wav(str(original_wav_path))
        sound = sound.set_channels(1)
        sound = sound.set_frame_rate(22050)
        sound.export(str(wav_path / data[0]), format="wav")

        audio_data.append(data)

random.shuffle(audio_data)
splitter = int(len(audio_data) * 0.95)

print(f"Generating ljs_audio_text_train_filelist.txt...")
with open(ljs_path / 'ljs_audio_text_train_filelist.txt', 'w', encoding='utf8') as filelist:
    for audio_item in audio_data[:splitter]:
        original_wav_filename = audio_item[0]
        text = audio_item[1]

        filelist.write(f'filelists/wavs/{original_wav_filename}|{text}\n')

print(f"Generating ljs_audio_text_val_filelist.txt...")
with open(ljs_path / 'ljs_audio_text_val_filelist.txt', 'w', encoding='utf8') as filelist:
    for audio_item in audio_data[splitter:]:
        original_wav_filename = audio_item[0]
        text = audio_item[1]

        filelist.write(f'filelists/wavs/{original_wav_filename}|{text}\n')

print(f"Generating ljs_audio_text_test_filelist.txt...")
with open(ljs_path / 'ljs_audio_text_test_filelist.txt', 'w', encoding='utf8') as filelist:
    pass

print(f"Generating metadata.csv...")
with open(ljs_path / 'metadata.csv', 'w', encoding='utf8') as filelist:
    for audio_item in audio_data:
        original_wav_filename = audio_item[0]
        text = audio_item[1]
        filename = original_wav_filename[:-4]

        filelist.write(f'{filename}|{text}\n')
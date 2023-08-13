import os
import shutil
import argparse
from mutagen.flac import FLAC
import eyed3
from tqdm import tqdm

def has_embedded_lyrics(audio):
    if isinstance(audio, FLAC):
        return 'LYRICS' in audio
    elif isinstance(audio, eyed3.core.AudioFile):
        return audio.tag.lyrics is not None
    return False

def embed_lrc(directory, skip_existing, delete_lrc):
    total_audio_files = 0
    embedded_lyrics_files = 0
    
    audio_files = [file for file in os.listdir(directory) if file.endswith('.flac') or file.endswith('.mp3')]
    with tqdm(total=len(audio_files), desc='Embedding LRC files', unit='file') as pbar:
        for file in audio_files:
            audio_path = os.path.join(directory, file)
            lrc_file = os.path.splitext(file)[0] + '.lrc'
            lrc_path = os.path.join(directory, lrc_file)
            
            if os.path.exists(lrc_path):
                if skip_existing:
                    audio = None
                    if file.endswith('.flac'):
                        audio = FLAC(audio_path)
                    elif file.endswith('.mp3'):
                        audio = eyed3.load(audio_path)
                    if has_embedded_lyrics(audio):
                        pbar.set_postfix({"status": "skipped"})
                        pbar.update(1)
                        continue
                
                try:
                    if file.endswith('.flac'):
                        audio = FLAC(audio_path)
                        audio['LYRICS'] = open(lrc_path, 'r', encoding='utf-8').read()
                        audio.save()
                    elif file.endswith('.mp3'):
                        audio = eyed3.load(audio_path)
                        tag = audio.tag
                        tag.lyrics.set(open(lrc_path, 'r', encoding='utf-8').read())
                        tag.save(version=eyed3.id3.ID3_V2_3)
                    
                    embedded_lyrics_files += 1
                    pbar.set_postfix({"status": "embedded"})
                    pbar.update(1)
                    
                    if delete_lrc:
                        os.remove(lrc_path)
                        pbar.set_postfix({"status": "embedded, LRC deleted"})
                        pbar.update(1)
                
                except Exception as e:
                    print(f"Error embedding LRC for {file}: {str(e)}")
                    pbar.set_postfix({"status": "error"})
                    pbar.update(1)
                    if os.path.exists(lrc_path):
                        shutil.move(lrc_path, lrc_path + ".failed")
                    continue

    return len(audio_files), embedded_lyrics_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Embed LRC files into audio files (FLAC and MP3) and optionally delete the LRC files.')
    parser.add_argument('-d', '--directory', required=True, help='Directory containing audio and LRC files')
    parser.add_argument('-s', '--skip', action='store_true', help='Skip files that already have embedded lyrics')
    parser.add_argument('--delete', action='store_true', help='Delete LRC files after embedding')
    args = parser.parse_args()

    banner = """
██╗     ██████╗  ██████╗██████╗ ██╗   ██╗████████╗
██║     ██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝
██║     ██████╔╝██║     ██████╔╝██║   ██║   ██║   
██║     ██╔══██╗██║     ██╔═══╝ ██║   ██║   ██║   
███████╗██║  ██║╚██████╗██║     ╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝      ╚═════╝    ╚═╝   
Scripted by TheRedSpy15"""
    print(banner)
    
    directory_path = args.directory
    skip_existing = args.skip
    delete_lrc = args.delete
    total, embedded = embed_lrc(directory_path, skip_existing, delete_lrc)
    percentage = (embedded / total) * 100 if total > 0 else 0
    
    print(f"Total audio files: {total}")
    print(f"Embedded lyrics in {embedded} audio files.")
    print(f"Percentage of audio files with embedded lyrics: {percentage:.2f}%")

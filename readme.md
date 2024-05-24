# Audio Lyrics Embedding Script (lrcput.py)

The `lrcput.py` script allows you to embed LRC (Lyrics) files into both FLAC, M4A and MP3 audio files. It supports specifying a directory containing the audio files and their corresponding LRC files with the same name.

**this script was designed to embed lyrics acquired from [lrcget](https://github.com/tranxuanthang/lrcget)**

## Requirements

- Python 3.x
- Required Python libraries (install using `pip install`):
  - mutagen
  - eyed3
  - tqdm (for progress bar)

## Usage

1. Place your audio files (FLAC or M4A or MP3) and their corresponding LRC files in the same directory.

2. Open a terminal or command prompt.

3. Navigate to the directory where the script `lrcput.py` is located.

4. Run the script with the following command to embed LRC files and optionally reduce (delete) them:

   ```sh
   python lrcput.py -d "path/to/your/directory" -s -r
   ```

Replace "path/to/your/directory" with the actual path to the directory containing your audio and LRC files.

    -d or --directory: Specify the directory containing audio files and LRC files.
    -s or --skip: Optional. Skip files that already have embedded lyrics.
    -r or --reduce: Optional. Reduce (delete) LRC files after embedding.
    -R or --recursive: Optional. Recursively process subdirectories

## Example

Suppose you have the following directory structure:

```audio_directory/
|-- song1.flac
|-- song1.lrc
|-- song2.mp3
|-- song2.lrc
|-- song3.m4a
|-- song3.lrc
|-- ...
```

To embed LRC files into the audio files and delete them after embedding, navigate to the script's directory and run the following command:

```
python lrcput.py -d "path/to/audio_directory" -s -r
```

## Notes

- The LRC files should have the same name astheir corresponding audio files, but with a .lrc extension.

- You can modify the script's options andbehavior by editing the script directly.

- Make sure to backup your original audiofiles before running the script.

## Acknowledgments

This script utilizes the mutagen and eyed3 libraries for working with audio and metadata.

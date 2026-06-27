(Inteface on spanish)

req  python3.8+, ffmpeg


ubuntu/debian
```bash
sudo apt install git
sudo apt install python3
sudo apt install ffmpeg
```
--after cloning the repo:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


termux (android)
```bash
pkg install git
pkg install python3
pkg install ffmpeg
```
--after cloning the repo:
```bash
pip install -r requirements.txt
```
(give termux access to your storage if you havent set it up yet)
```bash
termux-setup-storage
```

clone
```bash
git clone https://github.com/tuna-hub/yt-music-downloader
cd yt-music-downloader
```
To execute
```bash
python3 descargador.py
```


you can put either youtube single video or entire playlist with url, the program makes a folder with the name of the playlist when you download one, the artist is gotten from either the channel name, or video metadata

NOTE:maximum playlist lenght is around 100

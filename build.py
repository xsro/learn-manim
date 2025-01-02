import subprocess
from pathlib import Path
import argparse
import os

def merge_videos_ffmpeg(video_path, output_path,run=False):
    tmpdir=output_path.parent.joinpath("tmp")
    if not tmpdir.exists():
        tmpdir.mkdir()
    to_merge=[]
    for i,p in enumerate(video_path):
        tmpfilename=output_path.name+f"_{i}.ts"
        to_merge.append(tmpfilename)
        tmp=tmpdir.joinpath(tmpfilename)
        if tmp.exists():
            tmp.unlink()
        cmd = ["ffmpeg","-i",str(p),"-c","copy",str(tmp)]
        print(" ".join(cmd))
        if run:
            subprocess.run(cmd)
    cmd = ["ffmpeg",]
    cmd.extend(["-i", "concat:{}".format("|".join(to_merge))])
    cmd.extend(["-c", "copy", str(output_path)])
    print(" ".join(cmd))
    if run:
        subprocess.run(cmd,cwd=str(tmpdir))

PROJ=Path(__file__).parent

class Producer:
    manim=True
    ffmpeg=True
    def produce(self,config,i18n="",cwd=PROJ):
        manim=self.manim
        ffmpeg=self.ffmpeg
        if i18n=="en":
            i18n=""
        elif i18n=="zh-cn":
            i18n="Zh"
        mp4files=[]
        for file,scene in config:
            cmd=["manim","render","-ql",file+".py",scene+i18n]
            print(" ".join(cmd))
            if manim:
                subprocess.run(cmd,cwd=str(cwd))
            p=cwd.joinpath(f"media/videos/{file}/480p15/{scene+i18n}.mp4").absolute()
            mp4files.append(p)
        print(mp4files)

        outpath=cwd.joinpath("media","output"+i18n+".mp4").absolute()
        if outpath.exists():
            outpath.unlink()
        merge_videos_ffmpeg(mp4files,output_path=outpath,run=ffmpeg)
            

def read_list(scenelist):
    scenes=[]
    with open(scenelist) as f:
        lines=f.readlines()
        for line in lines:
            line=line.strip()
            if line.startswith("#"):
                continue
            if line=="":
                continue
            scenes.append(tuple(line.split(" ")))
    return scenes


if __name__=="__main__":
    p=Producer()
    parser = argparse.ArgumentParser()
    parser.add_argument("scenelist")
    parser.add_argument("--manim",action="store_true")
    parser.add_argument("--ffmpeg",action="store_true")
    args = parser.parse_args()
    scenelist=Path(args.scenelist)
    if not scenelist.exists():
        raise FileNotFoundError(scenelist)
    scenes=read_list(scenelist)
    p.manim=args.manim
    p.ffmpeg=args.ffmpeg
    p.produce(scenes,i18n="Zh",cwd=scenelist.parent.absolute())
    p.produce(scenes,i18n="en",cwd=scenelist.parent.absolute())
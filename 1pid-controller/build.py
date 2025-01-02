import subprocess
from pathlib import Path
PROJ=Path(__file__).parent

config=[
    ("introduction","Introduction"),
    ("control2order","PidPerformance")
]

class Producer:
    manim=True
    ffmpeg=True
    def produce(self,i18n=""):
        manim=self.manim
        ffmpeg=self.ffmpeg
        if i18n=="en":
            i18n=""
        mp4files=[]
        for file,scene in config:
            cmd=["manim","render","-ql",file+".py",scene+i18n]
            print(" ".join(cmd))
            if manim:
                subprocess.run(cmd,cwd=str(PROJ))
            mp4files.append("-i")
            mp4files.append(f"media/videos/{file}/480p15/{scene+i18n}.mp4")
        if ffmpeg:
            out="media/"+PROJ.name+i18n+".mp4"
            subprocess.run(["ffmpeg",*mp4files,"-c", "copy",out],cwd=str(PROJ))


if __name__=="__main__":
    p=Producer()
    p.manim=False
    p.produce(i18n="Zh")
    p.produce(i18n="en")
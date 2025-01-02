from manim import *

class AniTexts:
    def __init__(self):
        self.title = Text(r"PID Controller")
        self.pidtime = MathTex(r"u(t) = ",r"K_p e(t)", "+",
                           r"K_i\int_0^t e(\tau) d\tau","+",
                           r"K_d \frac{d e(t)}{dt}")
        self.pidtf = MathTex(r"G_c(s) = K_p + K_i\frac{1}{s} + K_ds")
        self.transform_title = Text("PID controller consists three terms:")

        

        descriptions=[
            ("Proportional part is about the [[current]] error","and influences the [[stability]] of control performance"),
            ("Integral part is about the [[past]] errors","and influences the [[accuracy]] of control performance"),
            ("Proportional part is the estimation of [[future]] error","and influences the [[rapidity]] of control performance"),
        ]
        self.descriptions=self.set_description(descriptions)

    def style1(self,text1):
        text1=text1.replace("[[",r'<span underline="single" underline_color="green" fgcolor="red">')
        text1=text1.replace("]]",r'</span>')
        return MarkupText(text1,font_size=30)
        
    def style2(self,text2):
        text2=text2.replace("[[",r'<gradient from="RED" to="YELLOW">')
        text2=text2.replace("]]",r'</gradient>')
        return MarkupText(text2,font_size=24)
    
    def set_description(self,descriptions):
        return list(map(lambda x:VGroup(self.style1(x[0]),self.style2(x[1])).arrange(DOWN),descriptions))
    

    @staticmethod
    def new(i18n="en"):
        out=AniTexts()
        if i18n=="zh-cn":
            out.title=Text("PID 控制器")
            out.transform_title = Text("PID 控制器包含三个部分：")
            descriptions=[
                ("比例部分与 [[当前误差]] 有关", "并且影响控制性能的 [[稳定性]]"),
                ("积分部分与 [[以往误差]] 有关", "并且影响控制性能的 [[准确性]]"),
                ("比例部分与 [[未来误差]] 有关", "（未来是不可测量，所以是估计值）并且影响控制性能的 [[快速性]]和震荡特性")
                ]
            out.descriptions=out.set_description(descriptions)
        return out


class Introduction(Scene):
    i18n="en"
    def construct(self):
        texts=AniTexts.new(i18n=self.i18n)
        VGroup(texts.title,texts.pidtime,texts.pidtf).arrange(DOWN)
        self.play(
            Write(texts.title),
            FadeIn(texts.pidtime, shift=DOWN),
            FadeIn(texts.pidtf, shift=DOWN),
        )
        self.wait()

        
        texts.transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(texts.title, texts.transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in texts.pidtf]),
        )
        framebox1 = SurroundingRectangle(texts.pidtime[1], buff = .1)
        framebox2 = SurroundingRectangle(texts.pidtime[3], buff = .1)
        framebox3 = SurroundingRectangle(texts.pidtime[5], buff = .1)
        p_text = Text('P').next_to(framebox1, DOWN)
        i_text= Text('I').next_to(framebox2, DOWN)
        d_text= Text('D').next_to(framebox3, DOWN)

        
        
        for t in texts.descriptions:
            t.to_corner(DOWN)
        self.play(
            Create(framebox1),
            Create(p_text),
            Create(texts.descriptions[0]),
        )
        self.wait(3)
        self.play(
            ReplacementTransform(framebox1,framebox2),
            ReplacementTransform(p_text,i_text),
            ReplacementTransform(texts.descriptions[0],texts.descriptions[1]),
        )
        self.wait(3)
        self.play(
            ReplacementTransform(framebox2,framebox3),
            ReplacementTransform(i_text,d_text),
            ReplacementTransform(texts.descriptions[1],texts.descriptions[2]),
        )
        self.wait(3)


class IntroductionZh(Introduction):
    i18n="zh-cn"
from manim import *


class Introduction(Scene):
    def construct(self):
        title = Tex(r"PID Controller")
        pidtime = MathTex(r"u(t) = ",r"K_p e(t)", "+",
                           r"K_i\int_0^t e(\tau) d\tau","+",
                           r"K_d \frac{d e(t)}{dt}")
        pidtf = MathTex(r"G_c(s) = K_p + K_i\frac{1}{s} + K_ds")
        
        VGroup(title,pidtime,pidtf).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(pidtime, shift=DOWN),
            FadeIn(pidtf, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("PID controller consists three terms:")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in pidtf]),
        )
        framebox1 = SurroundingRectangle(pidtime [1], buff = .1)
        framebox2 = SurroundingRectangle(pidtime [3], buff = .1)
        framebox3 = SurroundingRectangle(pidtime [5], buff = .1)
        p_text = Text('P').next_to(framebox1, DOWN)
        i_text= Text('I').next_to(framebox2, DOWN)
        d_text= Text('D').next_to(framebox3, DOWN)

        descriptions=[
            ("Proportional part is about the [[current]] error","and influences the [[stability]] of control performance"),
            ("Integral part is about the [[past]] errors","and influences the [[accuracy]] of control performance"),
            ("Proportional part is [[future]] error (it's estimation because futher is not measurable)","and influences the [[rapidity]] of control performance"),
        ]
        texts=[]
        for (text1,text2) in descriptions:
            text1=text1.replace("[[",r'<span underline="single" underline_color="green">')
            text1=text1.replace("]]",r'</span>')
            text2=text2.replace("[[",r'<gradient from="RED" to="YELLOW">')
            text2=text2.replace("]]",r'</gradient>')
            t1=MarkupText(text1,font_size=24)
            t2=MarkupText(text2,font_size=24)
            t2.to_corner(DOWN,buff=0.5)
            t1.next_to(t2,UP)
            texts.append(VGroup(t1,t2))
        
        self.play(
            Create(framebox1),
            Create(p_text),
            Create(texts[0]),
        )
        self.wait(5)
        self.play(
            ReplacementTransform(framebox1,framebox2),
            ReplacementTransform(p_text,i_text),
            ReplacementTransform(texts[0],texts[1]),
        )
        self.wait(5)
        self.play(
            ReplacementTransform(framebox2,framebox3),
            ReplacementTransform(i_text,d_text),
            ReplacementTransform(texts[1],texts[2]),
        )
        self.wait(5)

#! this script is very slow

import control as co
from manim import *
import numpy as np

def compose_closed_loop(
        Kp,Ki,Kd,wn,zeta,
):
    """construct a closed loop system of PID control with second order system G(s)=wn^2/(s^2+2*zeta*wn*s+wn^2)
    
    for pid introduction: 【自动控制原理】12_PID控制器_Matlab/Simulink仿真 https://www.bilibili.com/video/BV1xQ4y1T7yv/
    """
    G=co.tf([wn**2],[1,2*zeta*wn,wn**2])
    Gc=co.tf([Kd,Kp,Ki],[1,0])
    Gcl=co.feedback(Gc*G,1)
    return Gcl,G,Gc


class TextsEn:

    def __init__(self,plant,pid):
        self.title_full=[Tex("control the system "+plant,font_size=40),
                    Tex("with PID constroller "+pid,font_size=40)]
        self.title_short=Tex(f"control {plant} with PID "+pid)
        self.descriptions=[
            Tex("Initially, no control input, no response"),
            Tex("increase $K_p$ to track the reference signal"),# [[constant tracking error is observed]]
            Tex("increase $K_i$ to eliminate the tracking error"),
            Tex("increase $K_d$ to reduce oscillating and improve rapidity"),
        ]
        
class TextsCh:

    def __init__(self,plant,pid):
        self.title_full=[
            Tex("使用PID控制器"+pid, tex_template=TexTemplateLibrary.ctex,font_size=40),
            Tex("控制二阶系统 "+plant, tex_template=TexTemplateLibrary.ctex,font_size=40),
        ]
        self.title_short=Tex("使用 "+pid+" 控制 "+plant, tex_template=TexTemplateLibrary.ctex)
        self.descriptions=[
            Tex("初始时刻所有参数为零，无响应", tex_template=TexTemplateLibrary.ctex),
            Tex("增大 $K_p$ 响应逐步靠近参考信号", tex_template=TexTemplateLibrary.ctex),# [[constant tracking error is observed]]
            Tex("增大 $K_i$ 提升准确性，消除静差", tex_template=TexTemplateLibrary.ctex),
            Tex("增大 $K_d$ 提升快速性，减少震荡和超调", tex_template=TexTemplateLibrary.ctex),
        ]


class PidPerformance(Scene):

    def construct(self):
        self.construct0()

    def construct0(self,i18n="en"):
        # 1 full title
        omega_n=1
        zeta=1
        num=f"{omega_n**2}"
        den=f"s^2+{2*zeta*omega_n} s + {omega_n**2}"
        plant= r"$\frac{"+num+"}{"+den+"}$"
        pid=r"$K_p + K_i\frac{1}{s} + K_ds$"

        texts=TextsEn(plant,pid)
        if i18n=="ch":
            texts=TextsCh(plant,pid)
        
        texts.title_full[1].next_to(texts.title_full[0],DOWN,buff=1)
        title_full=VGroup(*texts.title_full)
        self.play(Write(title_full))
        self.wait()

        # short title
        texts.title_short.to_corner(UP+LEFT)
        self.play(ReplacementTransform(title_full,texts.title_short))
        self.wait()
        
        
        # plot the response
        axes = Axes(
            x_range=[0, 10.3, 1],
            y_range=[0, 1.5, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(0, 10.01, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.01, 2),
                "numbers_with_elongated_ticks": np.arange(0, 1.01, 2),
            },
            tips=True,
        )
        data_time=np.arange(0,10,0.1)
        data_ref=np.ones_like(data_time)
        ref_graph = axes.plot_line_graph(data_time,data_ref,add_vertex_dots=False,line_color=RED)

        tp=ValueTracker(0)
        ti = ValueTracker(0)
        td = ValueTracker(0)

        def render_graph():
            Gcl,G,Gc=compose_closed_loop(tp.get_value(),ti.get_value(),td.get_value(),1,1)
            _,data_y=co.forced_response(Gcl,T=data_time,X0=0,U=data_ref)
            return axes.plot_line_graph(data_time,data_y,add_vertex_dots=False,line_color=BLUE)
        def render_parameter():
            return Tex(r"$K_p$={:.2f}, $K_i$={:.2f}, $K_d$={:.2f}".format(1,ti.get_value(),td.get_value())).next_to(ref_graph,UP,buff=1)
        y_graph = always_redraw(render_graph)
        parameter=always_redraw(render_parameter)

        
        plot = VGroup(axes, ref_graph, y_graph).to_corner(DOWN)

        for text in texts.descriptions:
            text.to_corner(UP,buff=1.3)
        transformations=[ReplacementTransform(texts.descriptions[i],texts.descriptions[i+1]) for i in range(len(texts.descriptions)-1)]

        # all parameters are zeros
        self.add(texts.title_short,parameter,texts.descriptions[0])
        self.add(plot)
        self.play(Create(texts.descriptions[0]))
        self.wait(1)

        # increase Kp
        self.play(transformations[0])
        self.play(tp.animate(run_time=5).set_value(10))
        self.wait(1)

        # increase Ki
        self.play(transformations[1])
        self.play(ti.animate(run_time=3).set_value(2))
        self.wait(1)
        self.play(ti.animate(run_time=2).set_value(4))
        self.wait(1)

        # increase Kd
        self.play(transformations[2])
        self.play(td.animate(run_time=5).set_value(8))
        self.wait(1)
        self.play(td.animate(run_time=5).set_value(4.5))


        self.wait(5)

class PidPerformanceCh(PidPerformance):
    def construct(self):
        self.construct0(i18n="ch")


#%%
if __name__=="__main__":
    from matplotlib import pyplot as plt
    data_time=np.arange(0,20,0.1)
    data_ref=np.ones_like(data_time)
    Gcl,G,Gc=compose_closed_loop(10,4,0,1,1)
    _,data_y=co.forced_response(Gcl,T=data_time,X0=0,U=data_ref)

    plt.figure()
    plt.plot(data_time,data_y)
    plt.grid()




# %%

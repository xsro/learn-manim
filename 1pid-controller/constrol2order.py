import control as co
from manim import *
import numpy as np

def compose_closed_loop(
        Kp,Ki,Kd,wn,zeta,
):
    """construct a closed loop system of PID control with second order system G(s)=wn^2/(s^2+2*zeta*wn*s+wn^2)
    
    default parameters are taken from 【自动控制原理】12_PID控制器_Matlab/Simulink仿真 https://www.bilibili.com/video/BV1xQ4y1T7yv/
    """
    G=co.tf([wn**2],[1,2*zeta*wn,wn**2])
    Gc=co.tf([Kd,Kp,Ki],[1,0])
    Gcl=co.feedback(Gc*G,1)
    return Gcl,G,Gc


class Pidperformance(Scene):
    def construct(self):
        # 1 full title
        omega_n=1
        zeta=1
        num=f"{omega_n**2}"
        den=f"s^2+{2*zeta*omega_n} s + {omega_n**2}"
        pid=r"$K_p + K_i\frac{1}{s} + K_ds$"
        title_full=[Tex(r"control the system $\frac{"+num+"}{"+den+"}$",font_size=40),
                    Tex(r"with PID constroller "+pid,font_size=40)]
        title_full[1].next_to(title_full[0],DOWN,buff=1)
        title_full=VGroup(*title_full)
        self.play(Write(title_full))
        self.wait()

        # short title
        title=Tex(r"control $\frac{"+num+"}{"+den+"}$ with PID "+pid,font_size=30)
        title.to_corner(UP+RIGHT)
        self.play(ReplacementTransform(title_full,title))
        self.wait()
        
        # plot the response
        axes = Axes(
            x_range=[0, 10.3, 1],
            y_range=[0, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(0, 10.01, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.01, 2),
                "numbers_with_elongated_ticks": np.arange(0, 1.01, 2),
            },
            tips=False,
        )
        axes_labels = axes.get_axis_labels(
            x_label=Text("time",font_size=20),y_label=Text("signal",font_size=20),
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

        descs=[
            "the system cannot track the reference with no control",
            "increase $K_p$ to track the reference signal",# [[constant tracking error is observed]]
            "increase $K_i$ to eliminate the tracking error",
            "increase $K_d$ to oscillating and improve rapidity",
        ]
        texts=[]
        for desc in descs:
            desc=Tex(desc,font_size=30)
            texts.append(desc)
        

        plot = VGroup(axes, ref_graph, y_graph).to_corner(DOWN)
        labels = VGroup(axes_labels)

        # all parameters are zeros
        self.add(title,parameter,plot, labels,texts[0])
        self.play(Create(texts[0]))
        self.wait(1)

        # increase Kp
        self.play(ReplacementTransform(texts[0],texts[1]))
        self.play(tp.animate.set_value(1))
        self.wait(1)

        # increase Ki
        self.play(ReplacementTransform(texts[1],texts[2]))
        self.play(ti.animate.set_value(0.8))
        self.wait(1)
        self.play(ti.animate.set_value(1))
        self.wait(1)

        # increase Kd
        self.play(ReplacementTransform(texts[2],texts[3]))
        self.play(td.animate.set_value(1))
        self.wait(1)



#%%
if __name__=="__main__":
    from matplotlib import pyplot as plt
    data_time=np.arange(0,20,0.1)
    data_ref=np.ones_like(data_time)
    Gcl,G,Gc=compose_closed_loop(1,0.5,0.5,1,1)
    _,data_y=co.forced_response(Gcl,T=data_time,X0=0,U=data_ref)

    plt.figure()
    plt.plot(data_time,data_y)
    plt.grid()




# %%

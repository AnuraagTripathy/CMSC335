"""Shared slide helpers for the Exam 2 videos. No LaTeX needed."""
from manim import *
import textwrap

MONO = "Consolas"
SANS = "Segoe UI"
BG = "#1b1d2a"
ACCENT = "#ffd166"
OK = "#06d6a0"
BAD = "#ef476f"
config.background_color = BG


def txt(s, size=24, color=WHITE, font=SANS, **kw):
    return Text(s, font=font, font_size=size, color=color, line_spacing=0.9, **kw)


def mono(s, size=22, color=WHITE, **kw):
    return Text(s, font=MONO, font_size=size, color=color, line_spacing=0.9, **kw)


def code(src, w=None, h=None):
    c = Code(code_string=src.strip("\n"), language="javascript", formatter_style="monokai",
             background="window", add_line_numbers=False,
             paragraph_config={"font": MONO, "font_size": 22})
    if w and c.width > w:
        c.scale_to_fit_width(w)
    if h and c.height > h:
        c.scale_to_fit_height(h)
    return c


def read_time(*strings):
    n = sum(len(s or "") for s in strings)
    return min(14, 2.5 + n / 45)


class ExamScene(Scene):
    head = None

    # ---- building blocks -------------------------------------------------
    def intro(self, num, title, weight):
        t = txt(title, 46, ACCENT, weight=BOLD)
        if t.width > 13:
            t.scale_to_fit_width(13)
        n = txt(f"CMSC335 Exam 2  |  Video {num}", 26, GREY_B)
        w = txt(weight, 26, OK)
        g = VGroup(n, t, w).arrange(DOWN, buff=0.4)
        self.play(FadeIn(g, shift=UP * 0.3))
        self.wait(3)
        self.play(FadeOut(g))

    def header(self, s):
        new = txt(s, 34, ACCENT, weight=BOLD).to_edge(UP, buff=0.35)
        if self.head is None:
            self.play(FadeIn(new))
        else:
            self.play(ReplacementTransform(self.head, new))
        self.head = new

    def clear(self, keep_head=True):
        mobs = [m for m in self.mobjects if not (keep_head and m is self.head)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs])
        if not keep_head:
            self.head = None

    def trap(self, s, anchor=None):
        tag = txt("EXAM TRAP", 22, WHITE, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.1, width=tag.width + 0.4, height=tag.height + 0.25,
                               fill_color=BAD, fill_opacity=1, stroke_width=0)
        tag.move_to(box)
        label = VGroup(box, tag)
        body = txt(textwrap.fill(s, 78), 22, "#ffb3c1")
        g = VGroup(label, body).arrange(RIGHT, buff=0.3)
        if g.width > 13:
            g.scale_to_fit_width(13)
        g.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(g, shift=UP * 0.2))
        self.wait(read_time(s) + 1)
        return g

    def console(self, s, w=None):
        out = mono(s, 22, OK)
        lbl = txt("console / result", 16, GREY_B)
        box = SurroundingRectangle(out, color=OK, buff=0.2, corner_radius=0.08)
        g = VGroup(lbl, VGroup(box, out)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        if w and g.width > w:
            g.scale_to_fit_width(w)
        return g

    # ---- one teaching slide ---------------------------------------------
    def slide(self, title, src=None, notes=None, out=None, trap=None, extra_wait=0):
        """Header + code (left) + notes (right) + optional revealed output + optional trap."""
        self.header(title)
        parts = []
        c = n = None
        if src:
            c = code(src, w=8.0 if notes else 12.5, h=5.2 if out or trap else 6.0)
            parts.append(c)
        if notes:
            n = txt(notes, 22)
            if n.width > (4.8 if src else 12.5):
                n.scale_to_fit_width(4.8 if src else 12.5)
            parts.append(n)
        grp = VGroup(*parts).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        grp.next_to(self.head, DOWN, buff=0.4)
        if grp.width > 13.2:
            grp.scale_to_fit_width(13.2)
        grp.set_x(0)
        o = self.console(out, w=12) if out is not None else None
        if o is not None:
            o.next_to(grp, DOWN, buff=0.3).align_to(grp, LEFT)
            limit = -2.6 if trap else -3.7
            if o.get_bottom()[1] < limit:
                if n is None:  # tall code, no notes: put the output beside the code
                    c.become(code(src, w=13.2 - o.width - 0.5, h=6.0 if not trap else 5.2))
                    pair = VGroup(c, o).arrange(RIGHT, buff=0.5, aligned_edge=UP)
                    pair.next_to(self.head, DOWN, buff=0.4).set_x(0)
                else:
                    o.to_corner(DR, buff=0.4)
                    if trap:
                        o.shift(UP * 0.9)
        if c is not None:
            self.play(FadeIn(c, shift=RIGHT * 0.2))
        if n is not None:
            self.play(Write(n), run_time=min(2.5, 0.6 + len(notes) / 120))
        self.wait(read_time(src, notes) + extra_wait)
        if o is not None:
            self.play(FadeIn(o, shift=UP * 0.2))
            self.wait(read_time(out) + 1.5)
        if trap:
            self.trap(trap)
        self.clear()

    # ---- practice question ----------------------------------------------
    def practice(self, n, prompt, src, answer, answer_is_code=False):
        self.header(f"Practice Question {n}")
        p = txt(prompt, 24)
        if p.width > 12.5:
            p.scale_to_fit_width(12.5)
        items = [p]
        if src:
            items.append(code(src, w=12, h=4.2))
        g = VGroup(*items).arrange(DOWN, buff=0.35).next_to(self.head, DOWN, buff=0.35)
        self.play(FadeIn(g))
        self.wait(read_time(prompt) * 0.6)
        # 5 second "pause and try" timer
        label = txt("Pause and try it", 22, GREY_B)
        bar = Rectangle(width=6, height=0.12, fill_color=ACCENT, fill_opacity=1, stroke_width=0)
        timer = VGroup(label, bar).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(timer), run_time=0.4)
        self.play(bar.animate.stretch_to_fit_width(0.01).align_to(bar, LEFT), run_time=5.5, rate_func=linear)
        self.play(FadeOut(timer), run_time=0.3)
        self.clear()
        self.header(f"Practice Question {n}: Answer")
        if answer_is_code:
            a = code(answer, w=12.5, h=6)
        else:
            a = txt(answer, 26, OK)
            if a.width > 12.5:
                a.scale_to_fit_width(12.5)
        a.next_to(self.head, DOWN, buff=0.5)
        self.play(FadeIn(a, shift=UP * 0.2))
        self.wait(read_time(answer) + 3)
        self.clear()

    def outro(self, recap):
        self.header("Recap")
        r = txt(recap, 26)
        if r.width > 12.5:
            r.scale_to_fit_width(12.5)
        r.next_to(self.head, DOWN, buff=0.5)
        self.play(Write(r), run_time=2)
        self.wait(read_time(recap) + 1)
        self.clear(keep_head=False)

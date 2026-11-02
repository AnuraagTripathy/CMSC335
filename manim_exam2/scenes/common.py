"""Shared slide + narration helpers for the Exam 2 videos. No LaTeX needed.

Narration: every helper takes spoken text and times its animations to the speech
(manim-voiceover + the edge-tts service in edge_tts_service.py).
"""
import textwrap

from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

VOICE = "en-US-AndrewNeural"
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


def line_box(c, lines):
    """Highlight bar over code lines (1-based, inclusive) of a Code mobject."""
    a, b = lines if isinstance(lines, tuple) else (lines, lines)
    rows = VGroup(*[l for l in c.code_lines[a - 1:b] if len(l.get_all_points())])
    bg = c[0]
    return Rectangle(width=bg.width - 0.15, height=rows.height + 0.12, stroke_color=ACCENT, stroke_width=2.5,
                     fill_color=ACCENT, fill_opacity=0.12).move_to([bg.get_x(), rows.get_y(), 0])


class ExamScene(VoiceoverScene):
    head = None

    def setup(self):
        super().setup()
        self.set_speech_service(EdgeTTSService(voice=VOICE))

    def say(self, text):
        """with self.say("..."): animations  -> the block lasts at least as long as the speech."""
        return self.voiceover(text=text)

    def highlight(self, c, lines, old=None):
        """Create / move / remove a line highlight on code c. Returns the highlight mobject (or None)."""
        if lines is None:
            if old is not None:
                self.play(FadeOut(old), run_time=0.3)
            return None
        new = line_box(c, lines)
        if old is None:
            self.play(FadeIn(new), run_time=0.3)
            return new
        self.play(Transform(old, new), run_time=0.4)
        return old

    # ---- building blocks -------------------------------------------------
    def intro(self, num, title, weight, say):
        t = txt(title, 46, ACCENT, weight=BOLD)
        if t.width > 13:
            t.scale_to_fit_width(13)
        n = txt(f"CMSC335 Exam 2  |  Video {num}", 26, GREY_B)
        w = txt(weight, 26, OK)
        g = VGroup(n, t, w).arrange(DOWN, buff=0.4)
        with self.say(say):
            self.play(FadeIn(g, shift=UP * 0.3))
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

    def trap(self, s, say=None):
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
        with self.say("Exam trap. " + (say or s)):
            self.play(FadeIn(g, shift=UP * 0.2))
            self.play(Indicate(label, color=WHITE, scale_factor=1.15))
        self.wait(1)
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
    def slide(self, title, src=None, notes=None, out=None, trap=None, say=(), say_out=None, say_trap=None):
        """Header + code (left) + notes (right) + optional revealed output + optional trap.

        say: list of narration segments; each is "text" or ("text", lines) where lines is a
        1-based line number or (first, last) range of the code to highlight while speaking.
        say_out: narration while the output is revealed.  say_trap: spoken version of the trap.
        """
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
        hl = None
        segs = [s if isinstance(s, tuple) else (s, None) for s in say]
        for i, (text, lines) in enumerate(segs):
            with self.say(text):
                if i == 0:
                    if c is not None:
                        self.play(FadeIn(c, shift=RIGHT * 0.2))
                    if n is not None:
                        self.play(Write(n), run_time=min(2.5, 0.6 + len(notes) / 120))
                if c is not None:
                    hl = self.highlight(c, lines, hl)
        if not segs:
            self.play(*[FadeIn(m) for m in parts])
        if hl is not None:
            self.play(FadeOut(hl), run_time=0.3)
        if o is not None:
            with self.say(say_out or "Here's the output."):
                self.play(FadeIn(o, shift=UP * 0.2))
            self.wait(1)
        if trap:
            self.trap(trap, say_trap)
        self.clear()

    # ---- practice question ----------------------------------------------
    def practice(self, n, prompt, src, answer, say_q, say_a, answer_is_code=False):
        self.header(f"Practice Question {n}")
        p = txt(prompt, 24)
        if p.width > 12.5:
            p.scale_to_fit_width(12.5)
        items = [p]
        if src:
            items.append(code(src, w=12, h=4.2))
        g = VGroup(*items).arrange(DOWN, buff=0.35).next_to(self.head, DOWN, buff=0.35)
        with self.say(f"Practice question {n}. {say_q} Pause the video and try it."):
            self.play(FadeIn(g))
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
        with self.say(say_a):
            self.play(FadeIn(a, shift=UP * 0.2))
        self.wait(2)
        self.clear()

    def outro(self, recap, say):
        self.header("Recap")
        r = txt(recap, 26)
        if r.width > 12.5:
            r.scale_to_fit_width(12.5)
        r.next_to(self.head, DOWN, buff=0.5)
        with self.say(say):
            self.play(Write(r), run_time=2)
        self.wait(1.5)
        self.clear(keep_head=False)

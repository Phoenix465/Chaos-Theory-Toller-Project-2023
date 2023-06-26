import manim
from manim import *
from manim_slides import Slide
from manim_pptx import PPTXScene
from typing import List

fontSize = 30


def createTexM(string: str, fontS: float = fontSize) -> MathTex:
    stringS = string.split("=", 1)
    stringS.insert(1, "=")
    stringS = stringS[:2] + stringS[2].split("||")

    return MathTex(*stringS, font_size=fontS)


def generateTexM(*sL: str, startPos, fontS: float = fontSize, downMultiplier=None, specialAlign: MathTex = None) -> List[MathTex]:
    texs = [createTexM(s, fontS) for s in sL]
    texs[0].move_to(startPos)
    for i, tex in enumerate(texs[1:]):
        tex.next_to(texs[i], DOWN * 0.5)
        tex.shift(DOWN * (downMultiplier[i] if downMultiplier else 0))

    # Align to Previous One
    texPart2 = [tex[1] for tex in texs]
    for i, texPart in enumerate(texPart2):
        if i == 0:
            if specialAlign:
                texPart.align_to(specialAlign[1], LEFT)
        else:
            texPart.align_to(texPart2[i - 1], LEFT)

    for i in range(len(texs)):
        texs[i][0].next_to(texPart2[i], LEFT)
        texs[i][2:].next_to(texPart2[i], RIGHT)

    return texs


def replaceTexM(oldTexM: MathTex, newTexM: MathTex) -> None:
    newTexM[1].move_to(oldTexM[1])
    newTexM[0].next_to(newTexM[1], LEFT)
    newTexM[2:].next_to(newTexM[1], RIGHT)


def generateTexME(*sL: List[str], startPos, fontS: float = fontSize, downMultiplier=None) -> List[MathTex]:
    texs = [MathTex(s, font_size=fontS) for s in sL]

    texs[0].move_to(startPos)
    for i, tex in enumerate(texs[1:]):
        tex.next_to(texs[i], DOWN * 0.5)
        tex.shift(DOWN * (downMultiplier and downMultiplier[i]))

    return texs


def alignMathTexNum(mathTexs: List[MathTex], firstOffset, fontS: float = fontSize, startAdd: int = 0,
                    firstObj: MathTex = None):
    texs = [MathTex(f"({i + 1 + startAdd})", font_size=fontS) for i in range(len(mathTexs))]
    xOffset = (firstObj or mathTexs[0]).get_right()[0] + firstOffset

    for i, tex in enumerate(texs):
        tex.move_to(xOffset * RIGHT + mathTexs[i].get_center()[1] * UP)

    return texs


class PPTXSceneFake:
    def __init__(self):
        pass

    def endSlide(self, *args, **kwargs):
        pass


waitDuration = 0.1


class Main(MovingCameraScene, PPTXScene):
    def __init__(self):
        super().__init__()
        self.destroyLater = []

    def construct(self):
        # self.titleStage()
        # self.defineStage()
        # self.doublePendulumDerive()
        # self.doublePendulumDerive2(init=False)
        # self.formulas2()
        # self. tester()
        self.lorenzExplain()
        pass

    def titleStage(self):
        #  Title
        title = Text("Chaos Theory")
        self.add(title)
        self.play(Create(title))
        self.wait(waitDuration)
        self.endSlide()
        self.remove(title)

    def defineStage(self):
        title2 = Text("Chaotic Systems")
        title2.to_edge(UP)
        self.play(Create(title2))
        self.wait(waitDuration)
        self.endSlide()

        #  Define
        conditions = [
            "Sensitive to Initial Conditions",
            "Topologically Mix",
            "Dense Period Orbits"
        ]

        orderObjects = []

        maxX = 0

        for i, key in enumerate(conditions):
            circle = Circle(radius=0.25)
            circle.set_fill(WHITE)
            circle.set_color(WHITE)

            num = Integer(i + 1)
            num.shift(UP * (1 - i))
            num.shift(LEFT * 2)

            circle.move_to(num)

            mainText = Text(key, font_size=30)
            mainText.next_to(num, RIGHT)

            vGroup = VGroup(circle, num, mainText)
            maxX = max(maxX, abs(vGroup.get_center()[0]))

            orderObjects.append((vGroup, circle, num, mainText))

        for objectGroup in orderObjects:
            vGroup, circle, num, mainText = objectGroup
            vGroup.shift(LEFT * maxX)

            self.play(Create(circle), run_time=0.5)
            self.play(ReplacementTransform(circle, num), Write(mainText), run_time=1)
            self.endSlide()

    def doublePendulumDerive(self):
        # Deriving via Kinematics
        # Stage 1
        axes = Axes(axis_config={"tip_shape": StealthTip})
        labels = axes.get_axis_labels(
            Tex("x").scale(1),
            Tex("y").scale(1)
        )

        self.play(Create(axes))
        self.play(Create(labels))
        # self.wait(waitDuration)
        self.endSlide()

        # Stage 2
        pivot = Dot(ORIGIN, radius=0.1, color=YELLOW)
        pivotLabel = Tex("Pivot", font_size=fontSize).next_to(pivot, (LEFT + UP) * 0.25)

        self.play(Create(pivot))
        self.play(Write(pivotLabel))
        # self.wait(waitDuration)
        self.endSlide()

        # Stage 3
        pos1 = (1, -2)
        pos2 = (2, -3)

        firstPendulum = Dot(axes.c2p(*pos1), radius=0.2, color=BLUE)
        linesY1 = axes.get_horizontal_line(firstPendulum.get_center())
        linesX1 = axes.get_vertical_line(firstPendulum.get_center())
        arc1 = Arc(radius=0.5, start_angle=-1.10714871779, angle=-3.141592653589793238 / 2 + 1.10714871779,
                   arc_center=pivot.get_center())

        x1Label = MathTex(r"x_1", font_size=fontSize)
        y1Label = MathTex(r"y_1", font_size=fontSize)
        coord1 = MathTex(r"(x_1, y_1)", font_size=fontSize)
        angle1 = MathTex(r"\theta_1", font_size=fontSize)

        line1 = Line(start=pivot.get_center(), end=firstPendulum.get_center())
        length1 = MathTex(r"l_1", font_size=fontSize)

        x1Label.next_to(axes.c2p(pos1[0], 0), UP)
        y1Label.next_to(axes.c2p(0, pos1[1]), LEFT)
        coord1.next_to(firstPendulum.get_center(), UP + RIGHT)
        length1.next_to(line1.get_center(), RIGHT)
        angle1.next_to(arc1.get_center(), DOWN + RIGHT * 0.2)

        # ----

        secondPendulum = Dot(axes.c2p(*pos2), radius=0.2, color=BLUE)
        linesY2 = axes.get_horizontal_line(secondPendulum.get_center())
        linesX2 = axes.get_vertical_line(secondPendulum.get_center())
        arc2 = Arc(radius=0.5, start_angle=-3.141592653589793238 / 2, angle=3.141592653589793238 / 4,
                   arc_center=firstPendulum.get_center())

        x2Label = MathTex(r"x_2", font_size=fontSize)
        y2Label = MathTex(r"y_2", font_size=fontSize)
        coord2 = MathTex(r"(x_2, y_2)", font_size=fontSize)
        angle2 = MathTex(r"\theta_2", font_size=fontSize)

        line2 = Line(start=firstPendulum.get_center(), end=secondPendulum.get_center())
        angleLine = DashedLine(start=firstPendulum.get_center(), end=firstPendulum.get_center() + DOWN)

        length2 = MathTex(r"l_2", font_size=fontSize)

        x2Label.next_to(axes.c2p(pos2[0], 0), UP)
        y2Label.next_to(axes.c2p(0, pos2[1]), LEFT)
        coord2.next_to(secondPendulum.get_center(), UP + RIGHT)
        length2.next_to(line2.get_center(), RIGHT)
        angle2.next_to(arc2.get_center(), DOWN)

        self.play(Create(firstPendulum), Write(coord1))
        self.play(Create(linesX1), Write(x1Label), Create(linesY1), Write(y1Label))
        self.play(Create(line1), Write(length1))
        self.play(Create(arc1), Write(angle1))
        # self.wait(waitDuration)
        self.endSlide()

        self.play(Create(secondPendulum), Write(coord2))
        self.play(Create(linesX2), Write(x2Label), Create(linesY2), Write(y2Label))
        self.play(Create(line2), Write(length2), Create(angleLine))
        self.play(Create(arc2), Write(angle2))
        # self.wait(waitDuration)
        self.endSlide()

        # self.wait(2)

        # Stage 6 Aligner
        fDD1, fDD2, fDD3, fDD4 = generateTexM(
            r"x_1'' = l_1(cos(\theta_1)\theta_1'' - sin(\theta_1)\theta_1' * \theta_1')",
            r"y_1'' = l_1(sin(\theta_1)\theta_1'' + cos(\theta_1)\theta_1' * \theta_1')",
            r"x_2'' = x_1'' + l_2(cos(\theta_2)\theta_2'' - sin(\theta_2)\theta_2' * \theta_2')",
            r"y_2'' = y_1'' + l_2(sin(\theta_2)\theta_2'' + cos(\theta_2)\theta_2' * \theta_2')",
            startPos=axes.c2p(4, 3.5)
        )

        # Stage 4
        f1, f2, f3, f4 = generateTexM(
            r"x_1 =  l_1sin(\theta_1)",
            r"y_1 = -l_1cos(\theta_1)",
            r"x_2 = x_1 + l_2sin(\theta_2)",
            r"y_2 = y_1 - l_2cos(\theta_2)",
            startPos=axes.c2p(4, 3.5),
            specialAlign=fDD1
        )

        x1C = x1Label.copy()
        y1C = y1Label.copy()
        x2C = x2Label.copy()
        y2C = y2Label.copy()

        self.play(x1C.animate.move_to(f1[0]))
        self.play(Write(f1))
        self.play(y1C.animate.move_to(f2[0]))
        self.play(Write(f2))
        self.play(x2C.animate.move_to(f3[0]))
        self.play(Write(f3))
        self.play(y2C.animate.move_to(f4[0]))
        self.play(Write(f4))

        self.remove(x1C, x2C, y1C, y2C)
        # self.wait(waitDuration)
        self.endSlide()

        # Stage 5
        fD1, fD2, fD3, fD4 = generateTexM(
            r"x_1' = l_1cos(\theta_1) * \theta_1'",
            r"y_1' = l_1sin(\theta_1) * \theta_1'",
            r"x_2' = x_1' + l_2cos(\theta_2) * \theta_2'",
            r"y_2' = y_1' + l_2sin(\theta_2) * \theta_2'",
            startPos=axes.c2p(4, 3.5),
            specialAlign=fDD1
        )

        fD1r, fD2r, fD3r, fD4r = generateTexM(
            r"x_1' = l_1\theta_1'cos(\theta_1)",
            r"y_1' = l_1\theta_1'sin(\theta_1)",
            r"x_2' = x_1' + l_2\theta_2cos(\theta_2)",
            r"y_2' = y_1' + l_2\theta_2'sin(\theta_2)",
            startPos=axes.c2p(4, 3.5),
            specialAlign=fDD1
        )

        self.play(ReplacementTransform(f1, fD1))
        self.play(ReplacementTransform(f2, fD2))
        self.play(ReplacementTransform(f3, fD3))
        self.play(ReplacementTransform(f4, fD4))
        # self.wait(waitDuration)
        self.endSlide()

        self.play(ReplacementTransform(fD1, fD1r))
        self.play(ReplacementTransform(fD2, fD2r))
        self.play(ReplacementTransform(fD3, fD3r))
        self.play(ReplacementTransform(fD4, fD4r))
        # self.wait(waitDuration)
        self.endSlide()

        # Stage 6


        fDD1r, fDD2r, fDD3r, fDD4r = generateTexM(
            r"x_1'' = l_1(\theta_1''cos(\theta_1) - \theta_1'^2sin(\theta_1))",
            r"y_1'' = l_1(\theta_1''sin(\theta_1) + \theta_1'^2cos(\theta_1))",
            r"x_2'' = x_1'' + l_2(\theta_2''cos(\theta_2) - \theta_2'^2sin(\theta_2))",
            r"y_2'' = y_1'' + l_2(\theta_2''sin(\theta_2) + \theta_2'^2)cos(\theta_2)",
            startPos=axes.c2p(4, 3.5),
            specialAlign=fDD1
        )

        fDD1rr, fDD2rr, fDD3rr, fDD4rr = generateTexM(
            r"x_1'' = -\theta_1'^2l_1sin(\theta_1) + \theta_1''l_1cos(\theta_1)",
            r"y_1'' = \theta_1'^2l_1cos(\theta_1) + \theta_1''l_1sin(\theta_1)",
            r"x_2'' = x_1'' - \theta_2'^2l_2sin(\theta_2) + \theta_2''l_2cos(\theta_2) ",
            r"y_2'' = y_1'' + \theta_2'^2l_2cos(\theta_2) + \theta_2''l_2sin(\theta_2)",
            startPos=axes.c2p(4, 3.5),
            specialAlign=fDD1
        )

        self.play(ReplacementTransform(fD1r, fDD1))
        self.play(ReplacementTransform(fD2r, fDD2))
        self.play(ReplacementTransform(fD3r, fDD3))
        self.play(ReplacementTransform(fD4r, fDD4))
        # self.wait(waitDuration)
        self.endSlide()

        self.play(ReplacementTransform(fDD1, fDD1r))
        self.play(ReplacementTransform(fDD2, fDD2r))
        self.play(ReplacementTransform(fDD3, fDD3r))
        self.play(ReplacementTransform(fDD4, fDD4r))
        # self.wait(waitDuration)
        self.endSlide()

        self.play(ReplacementTransform(fDD1r, fDD1rr))
        self.play(ReplacementTransform(fDD2r, fDD2rr))
        self.play(ReplacementTransform(fDD3r, fDD3rr))
        self.play(ReplacementTransform(fDD4r, fDD4rr))
        # self.wait(waitDuration)
        self.endSlide()

        uwObj = [fDD1rr, fDD2rr, fDD3rr, fDD4rr, x1Label, x2Label, y1Label, y2Label, angle1, angle2, length1, length2,
                 coord1, coord2]
        ucObj = [linesX1, linesX2, linesY1, linesY2, arc1, arc2, angleLine]

        self.play(
            *list(map(Unwrite, uwObj)),
            *list(map(Uncreate, ucObj))
        )
        # self.wait(waitDuration)
        self.endSlide()

        self.destroyLater += [axes, pivotLabel, line1, line2, firstPendulum, secondPendulum]

    def doublePendulumDerive2(self, init: bool = True):
        fontSize = 30

        axes = Axes(axis_config={"tip_shape": StealthTip})
        labels = axes.get_axis_labels(
            Tex("x").scale(1),
            Tex("y").scale(1)
        )

        if init:
            self.play(Create(axes))
            self.play(Create(labels))
        else:
            self.add(axes)
            self.add(labels)

        # Stage 2
        pivot = Dot(ORIGIN, radius=0.1, color=YELLOW)
        pivotLabel = Tex("Pivot", font_size=fontSize).next_to(pivot, (LEFT + UP) * 0.25)

        if init:
            self.play(Create(pivot))
            self.play(Write(pivotLabel))
        else:
            self.add(pivot)
            self.add(pivotLabel)

        # Stage 3
        pos1 = (1, -2)
        pos2 = (2, -3)

        firstPendulum = Dot(axes.c2p(*pos1), radius=0.2, color=BLUE)
        arc1 = Arc(radius=0.5, start_angle=-3.141592653589793238 / 2, angle=0.463647609001,
                   arc_center=pivot.get_center())
        arc1.add_tip(tip_width=0.1, tip_length=0.1)
        angle1 = MathTex(r"\theta_1", font_size=fontSize)

        arc1v = Arc(radius=0.5, start_angle=3.141592653589793238 / 2, angle=0.463647609001,
                    arc_center=firstPendulum.get_center())
        arc1v.add_tip(tip_width=0.1, tip_length=0.1)

        angle1v = MathTex(r"\theta_1", font_size=fontSize)

        line1 = Line(start=firstPendulum.get_center(), end=pivot)
        line1R = line1.copy()

        angle1.next_to(arc1.get_center(), DOWN + RIGHT * 0.2)
        angle1v.next_to(arc1v.get_center(), UP + LEFT * 0.1)

        # ----

        secondPendulum = Dot(axes.c2p(*pos2), radius=0.2, color=BLUE)
        line2 = Line(start=firstPendulum.get_center(), end=secondPendulum.get_center())
        line2R = Line(start=secondPendulum.get_center(), end=firstPendulum.get_center())
        line2R2Tip = Line(start=secondPendulum.get_center(), end=(firstPendulum.get_center()) + 0.5 * (
                firstPendulum.get_center() - secondPendulum.get_center())).add_tip()

        angleLine = DashedLine(start=firstPendulum.get_center(), end=firstPendulum.get_center() + UP)

        line1Tip = line1.copy().add_tip()
        line2Tip = line2.copy().add_tip()
        line1RTip = line1R.copy().add_tip()
        line2RTip = line2R.copy().add_tip()

        tLabel1 = MathTex("T_1", font_size=fontSize).next_to(line1Tip.get_tip(), UP * 0.5)
        tLabel2 = MathTex("T_2", font_size=fontSize).next_to(line2Tip.get_tip(), DOWN * 0.5)
        tLabel2R = MathTex("T_2", font_size=fontSize).next_to(line2RTip.get_tip(), UP * 0.5)

        angleLine2 = DashedLine(start=firstPendulum.get_center(), end=firstPendulum.get_center() + DOWN)
        arc2 = Arc(radius=0.5, start_angle=-3.141592653589793238 / 2, angle=3.141592653589793238 / 4,
                   arc_center=firstPendulum.get_center())
        arc2.add_tip(tip_width=0.1, tip_length=0.1)
        angle2 = MathTex(r"\theta_2", font_size=fontSize)
        angle2.next_to(arc2.get_center(), DOWN)

        angleLine3 = DashedLine(start=secondPendulum.get_center(), end=secondPendulum.get_center() + UP)
        arc2v = Arc(radius=0.5, start_angle=3.141592653589793238 / 2, angle=3.141592653589793238 / 4,
                    arc_center=secondPendulum.get_center())
        arc2v.add_tip(tip_width=0.1, tip_length=0.1)
        angle2v = MathTex(r"\theta_2", font_size=fontSize).move_to(angleLine3.get_center() + LEFT * 0.2 + UP * 0.2)

        # ----
        massArrow = Line(start=firstPendulum.get_center(), end=firstPendulum.get_center() + DOWN * 1.4).add_tip()
        massLabel = MathTex("m_1", font_size=fontSize).next_to(massArrow.get_tip(), DOWN * 0.5)

        massArrow2 = Line(start=secondPendulum.get_center(), end=secondPendulum.get_center() + DOWN * 1.4).add_tip()
        massLabel2 = MathTex("m_2", font_size=fontSize).next_to(massArrow2.get_tip(), DOWN * 0.5)

        # ----
        # Speaker Notes: Regard Positive Angles as anti-clockwise
        accelerationX1 = MathTex(r"N2(\rightarrow): -T_1sin(\theta_1) + T_2sin(\theta_2) &= m_1a_x \\ &= m_1x_1''",
                                 font_size=fontSize / 1.5)
        accelerationX1.next_to(axes.c2p(1, -1), RIGHT)

        accelerationY1 = MathTex(r"N2(\uparrow): T_1cos(\theta_1) - T_2(\theta_2) - m_1g &= m_1a_y \\ &= m_1y_1''",
                                 font_size=fontSize / 1.5)
        accelerationY1.align_to(accelerationX1, LEFT)
        accelerationY1.next_to(accelerationX1, DOWN)

        accelerationX2 = MathTex(r"N2(\rightarrow): -T_2sin(\theta_2) &= m_2a_x \\ &= m_2x_2''",
                                 font_size=fontSize / 1.5)
        accelerationY2 = MathTex(r"N2(\uparrow): T_2cos(\theta_2) - m_2g &= m_2a_y \\ &= m_2y_2''",
                                 font_size=fontSize / 1.5)
        accelerationX2.next_to(axes.c2p(3, -1), RIGHT)
        accelerationY2.align_to(accelerationX2, LEFT)
        accelerationY2.next_to(accelerationX2, DOWN)

        if init:
            self.play(Create(firstPendulum))
            self.play(Create(line1))

            self.play(Create(secondPendulum))
            self.play(Create(line2))
        else:
            self.add(firstPendulum)
            self.add(line1)
            self.add(secondPendulum)
            self.add(line2)

        for obj in self.destroyLater:
            self.remove(obj)

        self.wait(waitDuration)
        self.endSlide()

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.set_width(firstPendulum.width * 20).move_to(firstPendulum))
        self.play(Create(arc1), Write(angle1))
        self.play(Create(arc2), Create(angleLine2), Write(angle2))
        self.play(Create(arc1v), Create(angleLine), Write(angle1v))

        secondPendulum.save_state()
        self.play(Uncreate(secondPendulum), Uncreate(pivot), Uncreate(pivotLabel), Uncreate(arc1), Uncreate(angle1))
        secondPendulum.restore()

        self.play(ReplacementTransform(line1, line1Tip), Write(tLabel1))
        self.play(ReplacementTransform(line2, line2Tip), Write(tLabel2))
        self.play(Create(massArrow), Write(massLabel))

        self.wait(waitDuration)
        self.endSlide()

        self.play(Write(accelerationX1))
        self.play(Write(accelerationY1))

        self.wait(waitDuration)
        self.endSlide()

        self.play(accelerationX1.animate.shift(UP * 10), accelerationY1.animate.shift(UP * 10))

        self.wait(waitDuration)
        self.endSlide()
        # self.play()

        self.play(Restore(self.camera.frame))

        self.play(
            ReplacementTransform(line2Tip, line2R), Unwrite(tLabel2), Uncreate(tLabel1),
            Create(secondPendulum),
            ReplacementTransform(line1Tip, line1R),
            Uncreate(massArrow), Unwrite(massLabel),
            Uncreate(arc1v), Uncreate(angleLine), Unwrite(angle1v)
        )

        self.wait(waitDuration)
        self.endSlide()

        self.play(self.camera.frame.animate.set_width(secondPendulum.width * 20).move_to(secondPendulum))

        self.play(Uncreate(line1R), Uncreate(firstPendulum))

        self.play(
            ReplacementTransform(line2R, line2R2Tip),
            Write(tLabel2R)
        )
        self.play(
            Create(angleLine3), Create(arc2v), Create(angle2v)
        )
        self.play(Create(massArrow2), Write(massLabel2))

        self.wait(waitDuration)
        self.endSlide()

        self.play(Write(accelerationX2))
        self.play(Write(accelerationY2))

        self.wait(waitDuration)
        self.endSlide()

        self.wait(waitDuration)
        self.endSlide()

    def formulas(self):
        downMultiplier = [0, 0, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0]

        formulasTex = generateTexM(
            r"m_1x_1'' = -T_1sin(\theta_1) ||+ T_2sin(\theta_2)",
            r"m_1y_1'' = T_1cos(\theta_1) - ||T_2cos(\theta_2)||- m_1g",
            r"m_2x_2'' = -T_2sin(\theta_2)",
            r"m_2y_2'' = T_2cos(\theta_2) - m_2g",

            r"m_1x_1'' = -T_1sin(\theta_1) ||+ T_2sin(\theta_2)",
            r"m_1y_1'' = T_1cos(\theta_1) - ||T_2cos(\theta_2)||- m_1g",

            r"T_1sin(\theta_1)cos(\theta_1) = -m_1x_1''cos(\theta_1) || - m_2x_2''cos(\theta_1)",
            r"-T_1cos(\theta_1)sin(\theta_1) = -m_1y_1''sin(\theta_1) - sin(\theta_1)(m_2y_2'' - m_2g - m_1g)",

            r"m_2x_2'' = -T_2sin(\theta_2)",
            r"m_2y_2'' = T_2cos(\theta_2) - m_2g",

            r"T_2sin(\theta_2)cos(\theta_2) = -m_2x_2''cos(\theta_2)",
            r"T_2cos(\theta_2)sin(\theta_2) = m_2y_2''sin(\theta_2) + m_2gsin(\theta_2)",

            r"sin(\theta_1)(m_1y_1'' + m_2y_2'' - m_2g - m_1g) = -cos(\theta_1)||(m_1x_1'' + m_2x_2'')",
            r"sin(\theta_2)(m_2y_2'' + m_2g) = -cos(\theta_2)(m_2x_2'')",

            startPos=(0, 3.6, 0),
            downMultiplier=downMultiplier
        )

        formulasTex0 = generateTexM(
            r"x_1'' = -\theta_1'^2l_1sin(\theta_1) + \theta_1''l_1cos(\theta_1)",
            r"y_1'' = \theta_1'^2l_1cos(\theta_1) + \theta_1''l_1sin(\theta_1)",
            r"x_2'' = x_1'' - \theta_2'^2l_2sin(\theta_2) + \theta_2''l_2cos(\theta_2)",
            r"y_2'' = y_1'' + \theta_2'^2l_2cos(\theta_2) + \theta_2''l_2sin(\theta_2)",

            r"sin(\theta_1)(m_1y_1'' + m_2y_2'' - m_2g - m_1g) = -cos(\theta_1)||(m_1x_1'' + m_2x_2'')",
            r"sin(\theta_2)(m_2y_2'' + m_2g) = -cos(\theta_2)(m_2x_2'')",

            startPos=(0, 3.6, 0),
            downMultiplier=downMultiplier,
            specialAlign=formulasTex[0]
        )

        f9 = formulasTex[0].copy()
        f9r = createTexM(r"m_1x_1'' = -T_1sin(\theta_1) || -[-T_2sin(\theta_2)]", fontS=fontSize)
        f9rr = createTexM(r"m_1x_1'' = -T_1sin(\theta_1) || -[m_2x_2'']", fontS=fontSize)
        f9rrr = createTexM(r"m_1x_1'' = -T_1sin(\theta_1) || -m_2x_2''", fontS=fontSize)

        f9Ar = createTexM(r"m_1x_1''cos(\theta_1) = -T_1sin(\theta_1)cos(\theta_1) || -m_2x_2''cos(\theta_1)",
                          fontS=fontSize)
        f9Arr = createTexM(r"T_1sin(\theta_1)cos(\theta_1) = -m_1x_1''cos(\theta_1) || -m_2x_2''cos(\theta_1)",
                           fontS=fontSize)
        f9Arrr = createTexM(r"T_1sin(\theta_1)cos(\theta_1) = -cos(\theta_1)||(m_1x_1'' + m_2x_2'')", fontS=fontSize)

        f10 = formulasTex[1].copy()
        f10r = createTexM(r"m_1y_1'' = T_1cos(\theta_1) - ||(T_2cos(\theta_2) - m_2g + m_2g)|| - m_1g", fontS=fontSize)
        f10rr = createTexM(r"m_1y_1'' = T_1cos(\theta_1) - ||(T_2cos(\theta_2) - m_2g) - m_2g|| - m_1g", fontS=fontSize)
        f10rrr = createTexM(r"m_1y_1'' = T_1cos(\theta_1) - ||m_2y_2''|| - m_2g - m_1g", fontS=fontSize)

        f10Ar = createTexM(
            r"m_1y_1''sin(\theta_1) = T_1cos(\theta_1)sin(\theta_1) ||- sin(\theta_1)(m_2y_2'' - m_2g - m_1g)",
            fontS=fontSize)
        f10Arr = createTexM(
            r"-T_1cos(\theta_1)sin(\theta_1) = -m_1y_1''sin(\theta_1) ||- sin(\theta_1)(m_2y_2'' - m_2g - m_1g)",
            fontS=fontSize)
        f10Arrr = createTexM(
            r"T_1cos(\theta_1)sin(\theta_1) = m_1y_1''sin(\theta_1) ||+ sin(\theta_1)(m_2y_2'' - m_2g - m_1g)",
            fontS=fontSize)
        f10Arrrr = createTexM(r"T_1cos(\theta_1)sin(\theta_1) = sin(\theta_1)(m_1y_1'' + m_2y_2'' - m_2g - m_1g)",
                              fontS=fontSize)

        f11 = createTexM(r"m_2x_2'' = -T_2sin(\theta_2)", fontS=fontSize)
        f11r = createTexM(r"m_2x_2''cos(\theta_2) = -T_2sin(\theta_2)cos(\theta_2)", fontS=fontSize)
        f11rr = createTexM(r"T_2sin(\theta_2)cos(\theta_2) = -m_2x_2''cos(\theta_2)", fontS=fontSize)

        f12 = createTexM(r"m_2y_2'' = T_2cos(\theta_2) - m_2g", fontS=fontSize)
        f12r = createTexM(r"m_2y_2''sin(\theta_2) = T_2cos(\theta_2)sin(\theta_2) ||- m_2gsin(\theta_2)",
                          fontS=fontSize)
        f12rr = createTexM(r"-T_2cos(\theta_2)sin(\theta_2) = -m_2y_2''sin(\theta_2) ||- m_2gsin(\theta_2)",
                           fontS=fontSize)
        f12rrr = createTexM(r"T_2cos(\theta_2)sin(\theta_2) = m_2y_2''sin(\theta_2) ||+ m_2gsin(\theta_2)",
                            fontS=fontSize)
        f12rrrr = createTexM(r"T_2cos(\theta_2)sin(\theta_2) = sin(\theta_2)(m_2y_2'' + m_2g)", fontS=fontSize)

        f13 = createTexM(r"sin(\theta_1)(m_1y_1'' + m_2y_2'' - m_2g - m_1g) = -cos(\theta_1)||(m_1x_1'' + m_2x_2'')",
                         fontS=fontSize)
        f14 = createTexM(r"sin(\theta_2)(m_2y_2'' + m_2g) = -cos(\theta_2)(m_2x_2'')", fontS=fontSize)

        replaceTexM(formulasTex[4], f9r)
        replaceTexM(formulasTex[4], f9rr)
        replaceTexM(formulasTex[4], f9rrr)

        replaceTexM(formulasTex[5], f10r)
        replaceTexM(formulasTex[5], f10rr)
        replaceTexM(formulasTex[5], f10rrr)

        replaceTexM(formulasTex[4], f9Ar)
        replaceTexM(formulasTex[6], f9Arr)
        replaceTexM(formulasTex[6], f9Arrr)

        replaceTexM(formulasTex[5], f10Ar)
        replaceTexM(formulasTex[7], f10Arr)
        replaceTexM(formulasTex[7], f10Arrr)
        replaceTexM(formulasTex[7], f10Arrrr)

        replaceTexM(formulasTex[4], f9Ar)
        replaceTexM(formulasTex[6], f9Arr)
        replaceTexM(formulasTex[6], f9Arrr)

        replaceTexM(formulasTex[12], f13)
        replaceTexM(formulasTex[13], f14)

        replaceTexM(formulasTex[2], f11)
        replaceTexM(formulasTex[8], f11r)
        replaceTexM(formulasTex[10], f11rr)

        replaceTexM(formulasTex[3], f12)
        replaceTexM(formulasTex[9], f12r)
        replaceTexM(formulasTex[11], f12rr)
        replaceTexM(formulasTex[11], f12rrr)
        replaceTexM(formulasTex[11], f12rrrr)

        formulaNumbers = alignMathTexNum(
            formulasTex,
            firstOffset=RIGHT * 4,
            fontS=fontSize,
            startAdd=3
        )

        formulaNumbers0 = alignMathTexNum(
            formulasTex0,
            firstOffset=RIGHT * 4,
            fontS=fontSize,
            firstObj=formulasTex[0],
        )

        for formula, formulaN in zip(formulasTex[:4], formulaNumbers):
            self.play(Write(formula), run_time=1)
            self.play(Write(formulaN), run_time=1)
            # self.add(formula)
            # self.add(formulaN)

        self.wait(waitDuration)
        self.endSlide()

        self.play(f9.animate.move_to(formulasTex[4]), Write(formulaNumbers[4]))
        self.play(ReplacementTransform(f9[3:], f9r[3:]))
        self.play(ReplacementTransform(f9r[3:], f9rr[3:]))
        self.play(ReplacementTransform(f9rr[3:], f9rrr[3:]))

        self.play(FadeOut(f9), run_time=0)
        self.add(f9rrr)

        self.play(f10.animate.move_to(formulasTex[5]), Write(formulaNumbers[5]))
        self.play(ReplacementTransform(f10[3:], f10r[3:]))
        self.play(ReplacementTransform(f10r[3:], f10rr[3:]))
        self.play(ReplacementTransform(f10rr[3:], f10rrr[3:]))

        self.play(FadeOut(f10), run_time=0)
        self.add(f10rrr)

        # self.add(f9rrr)

        self.play(
            ReplacementTransform(f9rrr[0], f9Ar[0]),
            ReplacementTransform(f9rrr[2:], f9Ar[2:]),
        )


        f9Copy = f9Ar.copy()
        for partA in f9Arr:
            partB = f9Copy.get_part_by_tex(partA.get_tex_string().lstrip("-+ "))
            self.play(ReplacementTransform(partB, partA))
        self.play(Create(formulaNumbers[6]))


        self.play(ReplacementTransform(f9Arr[2:], f9Arrr[2:]))

        self.play(
            ReplacementTransform(f10rrr[0], f10Ar[0]),
            ReplacementTransform(f10rrr[2:], f10Ar[2:]),
        )


        f10Copy = f10Ar.copy()
        for partA in f10Arr:
            partB = f10Copy.get_part_by_tex(partA.get_tex_string().lstrip("-+ "))
            self.play(ReplacementTransform(partB, partA))
        self.play(Write(formulaNumbers[7]))

        self.play(ReplacementTransform(f10Arr, f10Arrr))
        self.play(ReplacementTransform(f10Arrr, f10Arrrr))

        self.play(f11.animate.move_to(formulasTex[8]), Write(formulaNumbers[8]))
        self.play(ReplacementTransform(f11, f11r))


        self.play(f12.animate.move_to(formulasTex[9]), Write(formulaNumbers[9]))
        self.play(ReplacementTransform(f12, f12r))

        f11rCopy = f11r.copy()
        for partA in f11rr:
            partB = f11rCopy.get_part_by_tex(partA.get_tex_string().lstrip("-+ ").rstrip())
            self.play(ReplacementTransform(partB, partA))
        self.play(Write(formulaNumbers[10]))

        f12rCopy = f12r.copy()
        for partA in f12rr:
            partB = f12rCopy.get_part_by_tex(partA.get_tex_string().lstrip("-+ ").rstrip())
            self.play(ReplacementTransform(partB, partA))
        self.play(Write(formulaNumbers[11]))
        self.play(ReplacementTransform(f12rr, f12rrr))
        self.play(ReplacementTransform(f12rrr, f12rrrr))

        f9ArrrC = f9Arrr.copy()
        f10ArrrrC = f10Arrrr.copy()

        self.play(ReplacementTransform(f10ArrrrC[1], f13[1]))
        self.play(ReplacementTransform(f10ArrrrC[2:], f13[0]))
        self.play(ReplacementTransform(f9ArrrC[2:], f13[2:]))
        self.play(Write(formulaNumbers[12]))


        f11rrC = f11rr.copy()
        f12rrrrC = f12rrrr.copy()

        self.play(ReplacementTransform(f12rrrrC[1], f14[1]))
        self.play(ReplacementTransform(f12rrrrC[2:], f14[0]))
        self.play(ReplacementTransform(f11rrC[2:], f14[2:]))
        self.play(Write(formulaNumbers[13]))

        uw = [
            *formulasTex[:4], *formulaNumbers[:12],
            f9rrr[1], f9Ar, f10rrr[1], f10Ar, f9Arr, f9Arrr,
            f10Arrrr, f11r, f12r, f11rr, f12rrrr
        ]

        self.play(*[Unwrite(obj) for obj in uw])
        self.play(
            f13.animate.move_to(formulasTex0[4]), f14.animate.move_to(formulasTex0[5]),
            formulaNumbers[12].animate.move_to(formulaNumbers0[4]),
            formulaNumbers[13].animate.move_to(formulaNumbers0[5]),
        )

        for formula, formulaN in zip(formulasTex0[:4], formulaNumbers0):
            self.play(Write(formula), run_time=1)
            self.play(Write(formulaN), run_time=1)

        mainFormula1 = createTexM(
            r"\theta_1'' = \frac{-g(2m_1 + m_2)sin \theta_1 - m_2gsin(\theta_1 - 2\theta_2) - 2sin(\theta_1-\theta_2)m_2(\theta_2'^2L_2+\theta_1'^2L_1cos(\theta_1-\theta_2))}{L_1(2m_1+m_2-m_2cos(2\theta_1-2\theta_2))}"
        )

        mainFormula2 = createTexM(
            r"\theta_2'' = \frac{2sin(\theta_1-\theta_2)(\theta_1'^2L_1(m_1+m_2)+g(m_1+m_2)cos\theta_1 + \theta_2'^2L_2m_2cos(\theta_1-\theta_2))}{L_2(2m_1+m_2-m_2cos(2\theta_1-2\theta_2))}"
        )

        mainFormula1.next_to(f14, DOWN)
        mainFormula1.shift(DOWN + RIGHT)
        mainFormula2.next_to(mainFormula1, DOWN)

        self.play(Write(mainFormula1))

        self.play(Write(mainFormula2))

    def formulas2(self):
        downMultiplier = [0, 0, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0]
        formulasTex = generateTexM(
            r"x_1'' = -\theta_1'^2l_1sin(\theta_1) + \theta_1''l_1cos(\theta_1)",
            r"y_1'' = \theta_1'^2l_1cos(\theta_1) + \theta_1''l_1sin(\theta_1)",
            r"x_2'' = x_1'' - \theta_2'^2l_2sin(\theta_2) + \theta_2''l_2cos(\theta_2)",
            r"y_2'' = y_1'' + \theta_2'^2l_2cos(\theta_2) + \theta_2''l_2sin(\theta_2)",

            r"m_1x_1'' = -T_1sin(\theta_1) ||+ T_2sin(\theta_2)",
            r"m_1y_1'' = T_1cos(\theta_1) - ||T_2cos(\theta_2)||- m_1g",
            r"m_2x_2'' = -T_2sin(\theta_2)",
            r"m_2y_2'' = T_2cos(\theta_2) - m_2g",

            startPos=(0, 3.6, 0),
            downMultiplier=downMultiplier,
        )


        formulasTexS = generateTexM(
            r"\theta_1'' = \frac{-g(2m_1 + m_2)sin \theta_1 - m_2gsin(\theta_1 - 2\theta_2) - 2sin(\theta_1-\theta_2)m_2(\theta_2'^2L_2+\theta_1'^2L_1cos(\theta_1-\theta_2))}{L_1(2m_1+m_2-m_2cos(2\theta_1-2\theta_2))}",
            r"\theta_2'' = \frac{2sin(\theta_1-\theta_2)(\theta_1'^2L_1(m_1+m_2)+g(m_1+m_2)cos\theta_1 + \theta_2'^2L_2m_2cos(\theta_1-\theta_2))}{L_2(2m_1+m_2-m_2cos(2\theta_1-2\theta_2))}",

            startPos=formulasTex[-1].get_bottom()[1]*UP + DOWN*1,
            downMultiplier=[0.2, 0.2],
        )

        formulaNumbers = alignMathTexNum(
            formulasTex,
            firstOffset=RIGHT * 4,
            fontS=fontSize,
            startAdd=0
        )

        for formula, formulaN in zip(formulasTex[:4], formulaNumbers[:4]):
            self.play(Write(formula), run_time=1)
            self.play(Write(formulaN), run_time=1)

        self.endSlide()

        for formula, formulaN in zip(formulasTex[4:6], formulaNumbers[4:6]):
            self.play(Write(formula), run_time=1)
            self.play(Write(formulaN), run_time=1)

        self.endSlide()

        for formula, formulaN in zip(formulasTex[6:8], formulaNumbers[6:8]):
            self.play(Write(formula), run_time=1)
            self.play(Write(formulaN), run_time=1)

        self.endSlide()

        for formula in formulasTexS:
            self.play(Write(formula))

            self.wait(waitDuration)
            self.endSlide()

    def tester(self):
        pass

    def lorenzExplain(self):
        square = Square(stroke_width=0)
        heater = Text("Heater")
        cooler = Text("Cooler")
        square.set_fill(BLUE_D, 0.4)

        square.scale(3)
        heater.next_to(square, DOWN)
        cooler.next_to(square, UP)

        convec1 = RoundedRectangle(corner_radius=1, height=5, width=2)
        convec2 = RoundedRectangle(corner_radius=1, height=5, width=2)
        convec1.reverse_points()
        convec2.reverse_points()

        convec1.flip(RIGHT)
        convec1.flip(UP)

        convec2.flip(RIGHT)

        convec1.shift(RIGHT*1.5)
        convec2.shift(LEFT*1.5)

        self.play(GrowFromCenter(square))
        self.play(Write(heater))
        self.play(Write(cooler))

        self.endSlide()

        for i in range(5):
            self.play(Create(convec1), Create(convec2))
            convec1.save_state()
            convec2.save_state()

            self.play(FadeOut(convec1), FadeOut(convec2), run_time=0.5)

            convec1.restore()
            convec2.restore()
        self.endSlide()

        self.wait()

class Main3D(ThreeDScene, PPTXScene):
    def construct(self):
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("z"))
        y_label = axes.get_y_axis_label(Tex("x")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex("y").rotate_about_origin(PI, UP))

        trackerX = ValueTracker(0)
        trackerY = ValueTracker(0)
        trackerZ = ValueTracker(0)

        dot = Dot3D([1 + 0.1, 1 + 0.1, 1 + 0.1], color=BLUE)
        x, y, z = (1, 1, 1)

        verticalLine = DashedLine(axes.c2p(x, 0), axes.c2p(x, y))
        horizontalLine = DashedLine(axes.c2p(0, y), axes.c2p(x, y))
        fallLine = DashedLine(axes.c2p(x, y), axes.c2p(x, y) + OUT * z)

        formulas = generateTexM(
            r"\frac{dx}{dt} = \sigma(y_1-x_1)",
            r"\frac{dy}{dt} = x_1(\rho-z_1)-y_1",
            r"\frac{dz}{dt} = x_1y_1 - \beta z_1",
            startPos=(3.5, 2.5, 0),
            fontS=fontSize
        )

        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        self.wait(0.5)

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(waitDuration)
        self.endSlide()

        self.play(Create(verticalLine), Create(horizontalLine))
        self.play(Create(fallLine))
        self.wait(waitDuration)
        self.endSlide()

        self.play(Create(dot))

        point = axes.coords_to_point((x, y, z))
        coord = MathTex("(x_1, y_1, z_1)", font_size=fontSize)
        coord.next_to(point[0], UR)
        coord.shift(LEFT*0.5 + DOWN*0.3)
        self.add_fixed_in_frame_mobjects(coord)

        self.play(Create(coord))
        self.wait(waitDuration)
        self.endSlide()

        for obj in formulas:
            self.add_fixed_in_frame_mobjects(obj)
            self.play(Write(obj))

            self.wait(waitDuration*2)
            self.endSlide()
        self.wait(2)

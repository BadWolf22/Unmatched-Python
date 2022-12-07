import json

import pygame_menu

cols = ["red", "orange", "yellow", "green", "blue", "purple", "brown", "black"];

class Map:
    def __init__(self, file, menu, widget, onreturn):
        file = open(file)
        self.data = json.load(file)
        self.display(menu, widget, onreturn)
        return

    def display(self, menu, widget, onreturn):
        decorator = widget.get_decorator()
        xOff = -widget.get_width()/2 + 10
        yOff = -widget.get_height()/2 + 25
        for node in range(self.data["nodeCount"]):
            pos1 = self.data[str(node)]["pos"]
            for neighbor in self.data[str(node)]["neighbors"]:
                pos2 = self.data[str(neighbor)]["pos"]
                decorator.add_line(
                    (
                        widget.get_width() * pos1[0] + xOff,
                        widget.get_height() * pos1[1] + yOff,
                    ),
                    (
                        widget.get_width() * pos2[0] + xOff,
                        widget.get_height() * pos2[1] + yOff,
                    ),
                    "#ffffff",
                    width=1,
                    prev=False,
                )
        for node in range(self.data["nodeCount"]):
            pos = self.data[str(node)]["pos"]
            groups = self.data[str(node)]["group"]
            button = menu.add.button(
                "", onreturn, node, button_id=str(node), float=True, align=pygame_menu.locals.ALIGN_LEFT
            )
            widget.pack(button)
            button.translate(widget.get_width() * pos[0], widget.get_height() * pos[1])
            # if len(groups) == 1:
                # if "starting" in self.data[str(node)]: radius = 30
                # else: radius = 25
            button.get_decorator().add_circle(
                # x=menu.get_width() * pos[0] + xOff,
                # y=menu.get_height() * pos[1] + yOff,
                x=0,
                y=0,
                radius=25,
                filled=False,
                color=cols[self.data[str(node)]["group"][0]],
                prev=True,
            )
            # Would be used if we actually cared about sections
            # else:
            #     for neighbor in range(len(groups)):
            #         button.get_decorator().add_arc(
            #             x=0,
            #             y=0,
            #             radius=25,
            #             init_angle=int((360 / len(groups)) * neighbor),
            #             final_angle=int((360 / len(groups)) * (neighbor + 1)),
            #             color=cols[self.data[str(node)]["group"][neighbor]],
            #             prev=False
            #         )
            #         # print(init_angle, final_angle)
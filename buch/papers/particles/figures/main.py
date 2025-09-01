import numpy as np
import matplotlib.pyplot as plt
import matplot2tikz
import os
from pathlib import Path

output_path = Path(__file__).parent.resolve() / "out"

tikz_template = (
r"""
%
% tikztemplate.tex -- template for standalon tikz images
%
% (c) 2021 Prof Dr Andreas Müller, OST Ostschweizer Fachhochschule
%
\documentclass[tikz]{standalone}
\usepackage{amsmath}
\usepackage{times}
\usepackage{txfonts}
\usepackage{pgfplots}
\usepackage{csvsimple}
\usetikzlibrary{arrows,intersections,math}
\begin{document}
\def\skala{1}
\begin{tikzpicture}[>=latex,thick,scale=\skala]

""",
r"""
\end{tikzpicture}
\end{document}
"""
)

def save_wrapped_tikz(filepath, axis_width = None, axis_height = None):
    tikz_code = tikz_template[0] + matplot2tikz.get_tikz_code(strict = True, wrap = False, axis_width=axis_width, axis_height=axis_height) + tikz_template[1]
    with open(filepath, "w+", encoding="utf-8") as f:
        f.write(tikz_code)

def plot_lineares_medium():
    D = 1.0             # Beispielkonstante
    F = np.linspace(-2, 2, 30)
    delta_l = F / D     # lineares Medium

    plt.figure()
    plt.plot(F, delta_l, label=r'$\Delta l = \frac{F}{D}$')
    plt.xlabel('$F$', loc = "center")
    plt.xticks([-2, -1, 0, 1, 2])
    plt.ylabel(r'$\Delta l$', loc="center", rotation=0)
    plt.yticks([-2, -1, 0, 1, 2])
    plt.legend(loc="lower right", frameon=True, edgecolor="black", facecolor="white", framealpha=1)

    # plt.show()
    save_wrapped_tikz(output_path / "lineares_medium_deformation.tex")
        
    plt.figure()
    plt.plot(F, len(F) * [D], label=r'$D(F) = 1$ (const.)')
    plt.xlabel('$F$', loc="center")
    plt.xticks([-2, -1, 0, 1, 2])
    plt.ylabel('$D$', labelpad=0, loc="center", rotation=0)  # Reduce margin with labelpad=0
    plt.ylim((0, 2.1))
    plt.yticks([0, 1, 2])
    plt.legend(loc="lower right", frameon=True, edgecolor="black", facecolor="white", framealpha=1)

    # plt.show()
    save_wrapped_tikz(output_path / "lineares_medium_elast_modul.tex")
    

def plot_nichtlineares_medium():

    pass

def main():
    plot_lineares_medium()

if __name__ == "__main__":
    main()

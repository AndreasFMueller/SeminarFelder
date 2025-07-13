import matplotlib # version <= 3.7.1 needed for proper pgf handling
def enable_export():
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        # 'font.size' : 8,
        'text.usetex': True,
        'pgf.rcfonts': False,
        'axes.unicode_minus' : False,
        "pgf.preamble": "\\usepackage{bm}\n\\usepackage{amsmath}\n\\usepackage{xcolor}\n\\usepackage{tgtermes}",
    })

def set_plot_settings(fig, ax): # Call after plot generated!
    # Set up a very faint grid
    ax.grid(True, which='both', linestyle=':', linewidth=0.25, color='gray')

    # Remove the top and right spines (frame)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Ensure only bottom and left spines are visible
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')

    # Adjust tick parameters for a cleaner look
    ax.tick_params(axis='both', which='both', direction='out', length=3, width=0.5, colors='black')

    # Add arrows at the end of the x and y axes
    arrowprops = dict(facecolor='black', arrowstyle='<-', linewidth=0.5, shrinkA=0, shrinkB=0)

    ax.annotate('', xy=(1, 0), xytext=(1.02, 0), xycoords=ax.transAxes, textcoords=ax.transAxes, arrowprops=arrowprops)
    ax.annotate('', xy=(0, 1), xytext=(0, 1.02), xycoords=ax.transAxes, textcoords=ax.transAxes, arrowprops=arrowprops)

    # Adjust the limits to make space for the arrows
    ax.set_xlim(left=ax.get_xlim()[0] - 0.05, right=ax.get_xlim()[1] + 0.05)
    ax.set_ylim(bottom=ax.get_ylim()[0] - 0.05, top=ax.get_ylim()[1] + 0.05)
            
    fig.set_size_inches(w=4.5, h=2.5)

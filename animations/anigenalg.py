"""
    Genetic Algorithm Animation (version 1.0.4)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Copyright © 2014 by Alberto Lorenzo

    E-mail: alorenzo.md@gmail.com

    -----------------------------------------------------------------------

    Developed with:

    - Python 3.2.5
    - NumPy 1.7.1
    - matplotlib 1.2.1

    External dependencies:

    - ffmpeg (tested under version 2.1.3)

    -----------------------------------------------------------------------

    Description:

    A demonstration of an implementation of a simple genetic algorithm with
    configurable parameters.
"""


# *************************************
#  - Importing libraries -

from os import system    # For calling ffmpeg.
from sys import exit
import argparse

import numpy as np

import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'

import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.animation as ani


# *************************************
# - Script's version -

version = '1.0.4'
date = '26/March/2014'


# *************************************
# - Parsing input block -

# Default values will be displayed in the help menu in brackets.
# Each parameter is described in the help menu.

parser = argparse.ArgumentParser(description='Genetic Algorithm Animation '
                                 '(version {0})'.format(version))
parser.add_argument('-v, --version', action='store_true', default=False,
                    dest='v', help='display script version')

# Algorithm parameters:
parser.add_argument('-g, --generations', action='store', type=int, default=15,
                    dest='g', help='set number of generations [15]',
                    metavar='')
parser.add_argument('-p, --population', action='store', type=int, default=32,
                    dest='p', help='set population size [32]', metavar='')
parser.add_argument('-b, --bits', action='store', type=int, default=16,
                    dest='b',
                    help='set specimen information size in bits [16]',
                    metavar='')
parser.add_argument('-m, --mutation', action='store', type=float, default=0.01,
                    dest='m', help='set mutation probability of a gen [0.01]',
                    metavar='')

# Aptitude function and population setting parameters:
parser.add_argument('-w, --weight', action='store', type=float, default=1.,
                    dest='w', help='set weight incremental ratio [1.0]',
                    metavar='')
parser.add_argument('-z, --zero', action='store_true', default=False,
                    dest='z', help='initial population all at zero')
parser.add_argument('-u, --unit', action='store_true', default=False,
                    dest='u', help='initial population all at one')

# Animation parameters:
parser.add_argument('-t, --blit', action='store_true', default=False,
                    dest='t', help='enable blitting')
parser.add_argument('-a, --AR', action='store', type=float, default=1.778,
                    dest='a', help='set animation aspect ratio [16/9]',
                    metavar='')
parser.add_argument('-i, --interval', action='store', type=int, default=1000,
                    dest='i', help='set delay between frames in ms [1000]',
                    metavar='')
parser.add_argument('-f, --fps', action='store', type=int, default=1,
                    dest='f', help='set output animation frames per '
                    'second [1]', metavar='')

# File saving parameters:
parser.add_argument('-o, --out', action='store', type=str, default='',
                    dest='o', help='save animation to file "<filename>.mp4"',
                    metavar='')
parser.add_argument('-d, --droid', action='store_true', default=False,
                    dest='d', help='create an android compatible copy')
parser = parser.parse_args()

# Passing parsed values to its corresponding program variables.
version = 0. if not parser.v else version

# Algorithm parameters:
gen = parser.g
pop = parser.p
bits = parser.b
pmut = parser.m

# Aptitude function and population setting parameters:
w = parser.w
zero = parser.z
unit = parser.u

# Animation parameters:
blit = parser.t
AR = parser.a
interval = parser.i
fps = parser.f

# File saving parameters:
filename = parser.o
droid = parser.d


# !!! No user input control has been made to prevent innapropiate values for
#     the parameters. Feel free to add your own control routines.

# *************************************
# - Version mode -

# If version flag is set, show's script version and exit.
if version:
    print('Genetic Algorithm Animation (version {0})'.format(version))
    print('{0} by Alberto Lorenzo'.format(date))
    exit(0)

# Print animation info.
print('Genetic Algorithm Animation')
print('Frames = {0}, Interval = {1} ms, Blitting = {2}'.format(gen * 3 + 1,
                                                               interval, blit))

# *************************************
# - Aptitude function -

# Vector of bit weights.
if np.isclose(w, 1.):
    p = np.array([1. / bits for i in range(0, bits)])
else:
    p = np.array([(w - 1.) * w ** i / (w ** bits - 1.)
                 for i in range(0, bits)])


def AF(ind):
    """ Aptitude function. Sum of the products of each bit and its weight. """

    return (np.array(ind, dtype=float) * p).sum()


# *************************************
# - Algorithm subroutines -


def merit(P, AF):
    """ Returns a vector with the results of each individual aptitude
    function. """

    return np.array([AF(P[i]) for i in range(pop)])


def comp(P, m):
    """  Competition operator:

    Chooses random couples and makes them compete. The winners remain in the
    result population matrix. """

    Q = np.empty(P.shape, dtype=bool)
    for i in range(pop):
        i1 = np.random.choice(range(pop))
        i2 = np.random.choice(range(pop))
        if m[i1] >= m[i2]:
            Q[i] = P[i1]
        else:
            Q[i] = P[i2]

    return Q


def cross(P):
    """ Crossover operator.

    Chooses random couples and gets bit from them using a random mask to create
    a new matrix of individuals."""

    Q = np.empty(P.shape, dtype=bool)
    for i in range(pop):
        i1 = np.random.choice(range(pop))
        i2 = np.random.choice(range(pop))
        mask = np.array([np.random.choice((True, False)) for j in range(bits)])
        for j in range(bits):
            if mask[j]:
                Q[i, j] = P[i1, j]
            else:
                Q[i, j] = P[i2, j]

    return Q


def mut(P):
    """ Mutation operator.

    Changes bits with a probability of pmut. """

    Q = np.empty(P.shape, dtype=bool)
    for i in range(pop):
        for j in range(bits):
            r = np.random.random()
            if (r <= pmut):
                Q[i, j] = not P[i, j]
            else:
                Q[i, j] = P[i, j]

    return Q


# *************************************
# - Population setting up -

# If not specified, a random population of individuals is created.
# P stores the population.
if zero:
    P = np.zeros((pop, bits))
elif unit:
    P = np.ones((pop, bits))
else:
    P = np.random.choice((True, False), (pop, bits))

m = merit(P, AF)    # m stores the vector with individuals' merits.

gen_v = [0]    # List storing generations (used for plotting).
max_m = [m.max()]    # List storing maximum merits along generations.
mean_m = [m.sum() / m.size]    # List storing mean value of merits.


# *************************************
# - Drawing -

# If bits + 2 < pop, each individual is represented along y axis, with the
# merit values displayed at right. If, not, individuals are displayed along x
# axis with the merit values displayed on top.
# cell_p stores the matrix of bits used for representation.
# merit_p stores the merit values used for representation.
mode_col = True if (bits + 2) < pop else False
if mode_col:
    x_min = (bits + 2 - pop) // 2
    x_max = pop + x_min
    y_min = 0
    y_max = pop
    cell_p = [[plt.Rectangle((j, i), 1., 1., color='white')
              for j in range(bits)] for i in range(pop)]
    merit_p = [plt.Rectangle((bits + 1, i), 1., 1.,
               color=plt.cm.spectral(m[i])) for i in range(pop)]
else:
    x_min = (pop - bits - 2) // 2
    x_max = (bits + 2) + x_min
    y_min = 0
    y_max = bits + 2
    cell_p = [[plt.Rectangle((i, j), 1., 1., color='white')
              for j in range(bits)] for i in range(pop)]
    merit_p = [plt.Rectangle((i, bits + 1), 1., 1., color=plt.cm.jet(m[i]))
               for i in range(pop)]

# Figure setting up.
FW = 8.125    # Figure's widht in inches.
fig = plt.figure('Genetic Algorithm Animation', figsize=(FW, FW / AR),
                 facecolor='white')

# Axis for representing the bit matrix.
ax1 = fig.add_axes([0., 0.1, 0.5, 0.8], aspect='equal', frameon=False)
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])
title1 = ax1.set_title('')

# Axis for plotting the merit function evolution along generations.
ax2 = fig.add_axes([0.55, 0.15, 0.4, 0.3])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
ax2.set_xlabel(r'$Generations$', fontsize=14)
ax2.set_ylabel(r'$\Phi$', fontsize=14)
ax2.set_xticks([0., gen])
ax2.set_xticklabels(['0', '{0}'.format(gen)])
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['0', '1'])
ax2.set_xlim(0., gen * 1.1)
ax2.set_ylim(0., 1.1)
ax2.grid()
title2 = ax2.set_title('')

# Axis for displaying current animation parameters.
ax3 = fig.add_axes([0.55, 0.55, 0.4, 0.4], frameon=False)
ax3.xaxis.set_ticks([])
ax3.yaxis.set_ticks([])
ax3.text(0., 0.8, 'Genetic Algorithm Animation', fontsize=16)
ax3.text(0.1, 0.6, r'$Population:$ ${0}$'.format(pop), fontsize=14)
ax3.text(0.65, 0.6, r'$Bits:$ ${0}$'.format(bits), fontsize=14)
ax3.text(0.15, 0.4, r'$Mutation$ $probability:$ '
         '${0}\%$'.format(int(pmut * 100.)), fontsize=14)
ax3.text(0.05, 0.1, r'$\Phi=\sum_{{i=1}}^{{bits}}w_{{i}}\cdot bit_{{i}}$  '
         '$/$  $w_{{i-1}}={0:.2f}\cdot w_{{i}}$'.format(w), fontsize=15)

# Attach bits and merit values to ax1.
for i in range(pop):
    ax1.add_patch(merit_p[i])
for i in range(pop):
    for j in range(bits):
        ax1.add_patch(cell_p[i][j])

# Create lines in ax2.
max_l, = ax2.plot(gen_v, max_m, color='black', linewidth=2,
                  label=r'$\Phi_{max}$')
mean_l, = ax2.plot(gen_v, mean_m, ':', color='black', linewidth=2,
                   label=r'$\overline{\Phi_{pop}}$')
ax2.legend(loc=4, fontsize=12)    # Legend at right-bottom corner.


# *************************************
# - Animation routines -

# Changing objects list.
artists = (max_l, mean_l)
for i in range(pop):
    artists += tuple(cell_p[i])
artists += tuple(merit_p)
artists += (title1, title2)


def init():
    """ Animation init function."""

    global P
    global m

    # Setting up titles.
    title1.set_text(r'$Initial$ $population$')
    title2.set_text(r'$Generation$ $\#0$')

    # Drawing initial population and merit.
    for i in range(pop):
        merit_p[i].set_color(plt.cm.jet(m[i]))
        for j in range(bits):
            if P[i, j]:
                cell_p[i][j].set_color('gray')

    return artists


def animate(it):
    """ Animation function."""

    # Overwritten on each step.
    global P
    global m

    f = it % 3    # 3 steps: competition, crossover and mutation.

    # Algorithm steps:
    if f == 0:    # Competition.
        P = comp(P, m)
        title1.set_text(r'$Generation$ $\#{0}$ $after$ '
                        '$competing$'.format(it // 3))
    elif f == 1:    # Crossover.
        P = cross(P)
        title1.set_text(r'$Generation$ $\#{0}$ $after$ '
                        '$crossover$'.format(it // 3))
    elif f == 2:    # Mutation.
        P = mut(P)
        if it // 3 < gen - 1:
            title1.set_text(r'$Generation$ $\#{0}$ $after$ '
                            '$mutation$'.format(it // 3))
        else:
            title1.set_text(r'$Generation$ $\#{0}$'.format(gen))
        title2.set_text(r'$Generation$ $\#{0}$'.format(it // 3 + 1))
    m = merit(P, AF)

    # Update population matrix graph.
    for i in range(pop):
        merit_p[i].set_color(plt.cm.jet(m[i]))
        for j in range(bits):
            if P[i, j]:
                cell_p[i][j].set_color('gray')
            else:
                cell_p[i][j].set_color('white')

    # Update line information.
    if it % 3 == 2:
        gen_v.append(it // 3 + 1)
        max_m.append(m.max())
        mean_m.append(m.sum() / m.size)
        max_l.set_data(gen_v, max_m)
        mean_l.set_data(gen_v, mean_m)

    plt.draw()    # For refreshing titles.

    return artists

# Animation object.
if blit:
    animation = ani.FuncAnimation(fig, animate, init_func=init, frames=gen * 3,
                                  interval=interval, blit=True, repeat=False)
else:
    animation = ani.FuncAnimation(fig, animate, init_func=init, frames=gen * 3,
                                  interval=interval, repeat=False)

# *************************************
# - Output file generation -

# If selected the output option, graphic window will not be shown.

# !!! <--droid> option added to have a fast way to watch this animations
#     in every android cell phone.
if filename:
    print('Generating animation...')
    animation.save(filename + '.mp4', fps=fps, writer='ffmpeg',
                   extra_args=['-vcodec', 'libx264'])
    print('Done!')
    if droid:
        print('Generating android compatible copy...')
        system('ffmpeg -i {0} -s 480x320 -vcodec mpeg4 -acodec aac '
               '-strict -2 -ac 1 -ar 16000 -r 13 -ab 32000 -aspect '
               '3:2 {1} -y -loglevel 0'.format(filename + '.mp4', filename +
                                               '_android.mp4'))
        print('Done!')
else:
    try:
        plt.show()
    except:    # Prevents unexpected error messages with low intervals in slow
        pass   # computers.

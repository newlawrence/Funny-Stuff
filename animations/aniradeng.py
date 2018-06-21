"""
    Radial Engine Animation (version 1.2.3)

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
        - NumPy 1.6.2
        - matplotlib 1.2.0

    External dependencies:

        - ffmpeg (tested under version 2.1.3)

    -----------------------------------------------------------------------

    Description:

        A simple radial engine animation showing piston strokes evolution
        with crankshaft rotation angle.

    -----------------------------------------------------------------------

    Special thanks to:

        - Pybonacci team (in special my friend, Juan Luis Cano), for their
        great work at promoting Python for scientific applications.
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

version = '1.2.3'
date = '19/March/2014'


# *************************************
# - Parsing input block -

# Default values will be displayed in the help menu in brackets.
# Each parameter is described in the help menu.

parser = argparse.ArgumentParser(description='Radial Engine Animation '
                                 '(version {0})'.format(version))
parser.add_argument('-v, --version', action='store_true', default=False,
                    dest='v', help='display script version')

# Geometric parameters (nondimesionalized using connecting rod's length):
parser.add_argument('-n, --number', action='store', type=int, default=5,
                    dest='n', help='set number of cylinders [5]', metavar='')
parser.add_argument('-l, --lambda', action='store', type=float, default=0.33,
                    dest='l', help='set crankpin/rod length ratio [0.33]',
                    metavar='')
parser.add_argument('-m, --mu', action='store', type=float, default=0.86,
                    dest='m', help='set secondary/primary rods length ratio '
                    '[0.86])', metavar='')

# Graphic details (nondimensionalized using crankpin length):
parser.add_argument('-w, --piston_w', action='store', type=float, default=1.5,
                    dest='w', help='set piston width/crankpin length ratio '
                    '[1.5]', metavar='')
parser.add_argument('-p, --piston_h', action='store', type=float, default=1.5,
                    dest='p', help='set piston height/crankpin length ratio '
                    '[1.5]', metavar='')
parser.add_argument('-t, --top', action='store', type=float, default=0.,
                    dest='t', help=('set cylinder height/crankpin length '
                                    'ratio [(PH+TDC)/crankpin length]'),
                    metavar='')
parser.add_argument('-c, --crankcase', action='store', type=float, default=0.,
                    dest='c', help='set crankcase radius/crankpin length '
                    'ratio [BDC/crank]', metavar='')

# Animation parameters:
parser.add_argument('-b, --blit', action='store_true', default=False,
                    dest='b', help='enable blitting')
parser.add_argument('-a, --AR', action='store', type=float, default=1.778,
                    dest='a', help='set animation aspect ratio [16/9]',
                    metavar='')
parser.add_argument('-f, --frames', action='store', type=int, default=720,
                    dest='f', help='set animation total frames [720]',
                    metavar='')
parser.add_argument('-i, --interval', action='store', type=int, default=50,
                    dest='i', help='set delay between frames in ms [50]',
                    metavar='')
parser.add_argument('-s, --fps', action='store', type=int, default=15,
                    dest='s', help='set output animation frames per '
                    'second [15]', metavar='')
parser.add_argument('-r, --revolutions', action='store', type=int, default=10,
                    dest='r', help='set output animation loops [10]',
                    metavar='')

# File saving parameters:
parser.add_argument('-o, --out', action='store', type=str, default='',
                    dest='o', help='save animation to file "<filename>.mp4"',
                    metavar='')
parser.add_argument('-d, --droid', action='store_true', default=False,
                    dest='d', help='create an android compatible copy')

parser = parser.parse_args()

# Cylinder height, crankcase radius, and version behaves the same:
# if not user defined, they will be zero until they're default values (which
# must be computed) are calculated.
version = 0. if not parser.v else version

# Passing parsed values to its corresponding program variables.

# Geometric parameters:
n = parser.n
l = parser.l
m = parser.m

# Graphic details:
PW = parser.w
PH = parser.p
t_radius = parser.t
c_radius = parser.c

# Animation parameters:
blit = parser.b
AR = parser.a
frames = parser.f
interval = parser.i
fps = parser.s
loops = parser.r

# File saving parameters:
filename = parser.o
droid = parser.d

# !!! No user input control has been made to prevent innapropiate values for
#     the parameters. Feel free to add your own control routines.


# *************************************
# - Version mode -

# If version flag is set, show's script version and exit.
if version:
    print('Radial Engine Animation (version {0})'.format(version))
    print('{0} by Alberto Lorenzo'.format(date))
    exit(0)

# Print animation info.
print('Radial Engine Animation')
print('Step = {0:.2f}º, Interval = {1} ms, Blitting = {2}'.format(360. *
      loops / frames, interval, blit))


# *************************************
# - Physics -

# All measures are nondimensionalized at last instance with crankpin length.
# Measures are irrelevant, so crankpink length has been taken as unitary.

# Step between axis.
theta = np.array([i * 2. * np.pi / n for i in range(1, n)])

# Secondary rods connection points radius.
e = (1. - m) / (1. - (l * np.sin(theta)) ** 2 / 2.)

# Angle between primary rod and primary piston to secondary rods connection
# points line.
delta = np.arcsin(np.sin(theta) * np.sqrt(1. - 2. * np.cos(theta) /
                  e + e ** -2) ** -1)

# The same mission as l for secondary pistons.
lb = l * np.sin(theta) * (m * np.sin(theta + delta)) ** -1

# Special point needed for secondary pistons position calculation.
OM = np.sin(theta) * (np.sin(theta + delta)) ** -1

# Cranckshaft rotation angle.
alpha = np.linspace(0., 2. * np.pi, frames // loops)

# Angle between primary rod and vertical axis.
betha = np.arcsin(l * np.sin(alpha))


def Bp(alpha):
    """ Primary piston stroke function. """

    return np.cos(alpha) + np.sqrt(1. - (l * np.sin(alpha)) ** 2) / l


def Bs(alpha):
    """ Secondary piston stroke function. """

    return e * Bp(alpha) + OM * (np.cos(alpha - (theta + delta)) +
                                 np.sqrt(1. - (lb * np.sin(alpha -
                                         (delta + theta))) ** 2) / lb)

# Pistons stroke evolution along crankshaft rotation angle.
OBs = np.array([Bs(a) for a in alpha]).transpose()
OBp = Bp(alpha)

# Points for drawing:
#    A = crankpin's end
#    Bp = primary piston stroke
#    Bs = secondary pistons stroke
#    C = secondary rods articulation point
x_OA = np.sin(alpha)
y_OA = np.cos(alpha)
x_OBp = np.zeros(OBp.shape)
y_OBp = OBp
x_OBs = np.array([OBs[i] * np.sin(theta[i]) for i in range(theta.size)])
y_OBs = np.array([OBs[i] * np.cos(theta[i]) for i in range(theta.size)])
x_OC = np.array([x_OA + e[i] * np.sin(theta[i] - betha) / l
                 for i in range(theta.size)])
y_OC = np.array([y_OA + e[i] * np.cos(theta[i] - betha) / l
                 for i in range(theta.size)])

# Notable points:
TDC = OBp.max()    # Top Dead Center
BDC = OBp.min()    # Bottom Dead Center
stroke = TDC - BDC    # Stroke


# *************************************
# - Drawing -

# Plotting parameters.
e_med = e.sum() / e.size if e.size else 0.
t_radius = PH + TDC if not t_radius else t_radius    # Cylinder height.
c_radius = BDC if not c_radius else c_radius    # Cranckcase radius.
space = 0.05    # Space between cylinder walls and pistons.
wall = 0.5 * PW + space    # Cylinder walls anchor.
union_angle = np.arcsin(wall / c_radius)
r_radius = c_radius * np.cos(union_angle)    # Cylinder and crankcase union.

# Setting up the animation figure.
FW = 8.125    # Figure default width in inches.
fig = plt.figure('Radial Engine Animation', figsize=(FW, FW / AR),
                 facecolor='white')
color = plt.cm.spectral(np.linspace(0., 0.9, n))    # Colormap for rods.

# Axes #1 for plotting the schematic drawing.
ax1 = fig.add_axes([0., 0., 0.5, 1.], aspect='equal', frameon=False)
ax1.set_xlim(- 1.1 * t_radius, 1.1 * t_radius)
ax1.set_ylim(- 1.1 * t_radius, 1.1 * t_radius)
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])

# Axes #2 for plotting the strokes graph.
ax2 = fig.add_axes([0.55, 0.2, 0.4, 0.4])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
ax2.set_xlabel(r'$\alpha$', fontsize=16)
ax2.set_xticks([0., np.pi / 2.0, np.pi, np.pi * 3. / 2., 2. * np.pi])
ax2.set_xticklabels(['0º', '90º', '180º', '270º', '360º'])
ax2.set_yticks([BDC, TDC])
ax2.set_yticklabels(['BDC', 'TDC'])
ax2.set_xlim(0., 2.0 * np.pi)
ax2.set_ylim(0., t_radius - PH * 0.5)
ax2.grid()

# Axes #3 for plotting some data.
ax3 = fig.add_axes([0.55, 0.65, 0.4, 0.3], frameon=False)
ax3.xaxis.set_ticks([])
ax3.yaxis.set_ticks([])
ax3.text(0.025, 0.8, 'Radial Engine Animation', fontsize=18)
ax3.text(0.2, 0.5, r'$n={0}$'.format(n), fontsize=16)
ax3.text(0.6, 0.5, r'$\lambda={0:.2f}$'.format(l), fontsize=16)
ax3.text(0.2, 0.3, r'$\overline{{\epsilon}}={0:.2f}$'.format(e_med),
         fontsize=16)    # Medium value of all e showed.
ax3.text(0.6, 0.3, r'$\mu={0:.2f}$'.format(m), fontsize=16)

# Cylinder axis arrays.
ax_p_x = np.array([0., 0.])
ax_p_y = np.array([0, t_radius])
ax_s_x = np.array([ax_p_y * np.sin(theta[i]) for i in range(theta.size)])
ax_s_y = np.array([ax_p_y * np.cos(theta[i]) for i in range(theta.size)])

# Cylinder walls.
ax_pwl_x = np.array([-wall, -wall])
ax_pwr_x = np.array([wall, wall])
ax_pw_y = np.array([r_radius, t_radius])
ax_sw_x = np.array([ax_pw_y * np.sin(theta[i]) for i in range(
                   theta.size)])
ax_sw_y = np.array([ax_pw_y * np.cos(theta[i]) for i in range(
                   theta.size)])
ax_swl_x = np.array([ax_sw_x[i] + np.sign(theta[i] - np.pi) *
                    np.cos(theta[i]) * wall
                    for i in range(theta.size)])
ax_swl_y = np.array([ax_sw_y[i] - np.sign(theta[i] - np.pi) *
                    np.sin(theta[i]) * wall
                    for i in range(theta.size)])
ax_swr_x = np.array([ax_sw_x[i] - np.sign(theta[i] - np.pi) *
                    np.cos(theta[i]) * wall
                    for i in range(theta.size)])
ax_swr_y = np.array([ax_sw_y[i] + np.sign(theta[i] - np.pi) *
                    np.sin(theta[i]) * wall
                    for i in range(theta.size)])
if not n % 2:    # With a pair number of cylinders, the bottom ones are
    ax_swl_x[n // 2 - 1] = ax_pwl_x    # problematic, so they're
    ax_swl_y[n // 2 - 1] = -ax_pw_y    # recalculated here.
    ax_swr_x[n // 2 - 1] = ax_pwr_x
    ax_swr_y[n // 2 - 1] = -ax_pw_y

# Plotting crankcase.
case = plt.Circle([0., 0.], c_radius, facecolor='white',
                  edgecolor='black', linewidth=2)
ax1.add_patch(case)

# White rectangles painted over crankcase as the cylinder insides.
wp = plt.Rectangle([-wall, 0.], PW + 2. * space, t_radius, color='white')
ws = [plt.Rectangle([-wall, 0.], PW + 2. * space, t_radius, color='white')
      for i in range(theta.size)]
ts = [mpl.transforms.Affine2D().rotate(-theta[i]) + ax1.transData
      for i in range(theta.size)]
ax1.add_patch(wp)
for i in range(theta.size):
    ws[i].set_transform(ts[i])
    ax1.add_patch(ws[i])

# Plotting cylinders axis.
ax1.plot(ax_p_x, ax_p_y, '--', color='gray')
for i in range(theta.size):
    ax1.plot(ax_s_x[i], ax_s_y[i], '--', color='gray')

# Plotting cylinder walls.
ax1.plot(ax_pwl_x, ax_pw_y, 'k', linewidth=2)
ax1.plot(ax_pwr_x, ax_pw_y, 'k', linewidth=2)
for i in range(theta.size):
    ax1.plot(ax_swl_x[i], ax_swl_y[i], 'k', linewidth=2)
    ax1.plot(ax_swr_x[i], ax_swr_y[i], 'k', linewidth=2)

# Setting up pistons.
pp = plt.Rectangle([0., 0.], PW, PH, color='gray')
ps = [plt.Rectangle([0., 0.], PW, PH, color='gray')
      for i in range(theta.size)]
ts = [mpl.transforms.Affine2D().rotate(-theta[i]) + ax1.transData
      for i in range(theta.size)]
ax1.add_patch(pp)
for i in range(theta.size):
    ps[i].set_transform(ts[i])
    ax1.add_patch(ps[i])

# Setting up rods and crankpin.
ep, = ax1.plot([], [], 'o-', linewidth=2, color=color[0])
es = [ax1.plot([], [], 'o-', linewidth=2, color=color[i + 1])[0]
      for i in range(theta.size)]
e0 = [ax1.plot([], [], 'ko-', linewidth=2)[0] for i in range(theta.size)]
ea, = ax1.plot([], [], 'ko-', linewidth=2)

# Setting up graph data.
cp, = ax2.plot([], [], linewidth=2, color=color[0])
cs = [ax2.plot([], [], linewidth=2, color=color[i + 1])[0]
      for i in range(theta.size)]


# *************************************
# - Animation routines -

# Changing objects list.
artists = (pp,) + tuple(ps) + (ep,) + tuple(es) + tuple(e0) + (ea,) + (cp,) + \
    tuple(cs)


def init():
    """ Base empty frame. Allows blitting. """

    # Since empty initialization for patches is imposible, draw them out from
    # axes limits (1.1 * t_radius).
    pp.set_xy([0., 2. * t_radius])
    for j in range(theta.size):
        ps[j].set_xy([0., 2. * t_radius])

    # Empty lines avoids drawing.
    ep.set_data([], [])
    for j in range(theta.size):
        es[j].set_data([], [])
    for j in range(theta.size):
        e0[j].set_data([], [])
    ea.set_data([], [])

    cp.set_data([], [])
    for j in range(theta.size):
        cs[j].set_data([], [])

    return artists


def animate(i):
    """ Animation main routine.

    As it can be seen, all calculations are already done, so there's no need to
    make them at the same time of compositing the animation. This will speed up
    the animation process. """

    k = i % alpha.size

    pp.set_xy([-PW * 0.5, OBp[k] - PH * 0.5])
    for j in range(theta.size):
        ps[j].set_xy([-PW * 0.5, OBs[j][k] - PH * 0.5])

    ep.set_data([x_OA[k], x_OBp[k]], [y_OA[k], y_OBp[k]])
    for j in range(theta.size):
        es[j].set_data([x_OC[j][k], x_OBs[j][k]], [y_OC[j][k], y_OBs[j][k]])
    for j in range(theta.size):
        e0[j].set_data([x_OA[k], x_OC[j][k]], [y_OA[k], y_OC[j][k]])
    ea.set_data([0., x_OA[k]], [0., y_OA[k]])

    cp.set_data(alpha[0:k], OBp[0:k])
    for j in range(theta.size):
        cs[j].set_data(alpha[0:k], OBs[j][0:k])

    return artists

if blit:
    animation = ani.FuncAnimation(fig, animate, frames=frames, init_func=init,
                                  interval=interval, blit=True)
else:
    animation = ani.FuncAnimation(fig, animate, frames=frames,
                                  interval=interval)


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

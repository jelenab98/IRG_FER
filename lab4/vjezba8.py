from pyglet.gl import *
import math

window = pyglet.window.Window(width=599, height=599)
triColor = [0.0, 0.0, 0.0]
mandelbrot = True
w, h = 599, 599


@window.event
def on_draw():
    global mandelbrot
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(8.0)
    glBegin(GL_POINTS)
    for x in range(0, w):
        for y in range(0, h):
            u = u_min + float(x * (u_max - u_min)) / w
            v = v_min + float(y * (v_max - v_min)) / h
            if mandelbrot:
                c_r, c_i = u, v
                z_r, z_i = 0, 0
            else:
                z_r, z_i = u, v
                c_r, c_i = cr, ci
            k = -1
            r = 0.0

            while k < m and r < eps:
                k += 1
                z_r_n1 = pow(z_r, 2) - pow(z_i, 2) + c_r
                z_i_n1 = 2*z_r*z_i + c_i
                z_r = z_r_n1
                z_i = z_i_n1
                r = math.sqrt(pow(z_r, 2) + pow(z_i, 2))

            if k < m/10:
                glColor3f(1 - k/m, 0.23-k/m, 0.4 - k/m)
            elif k < 2*m/5:
                glColor3f(0.55 + k/m, 0.5 - k/m, 0.78 - k/m)
            elif k < 3*m/5:
                glColor3f(0.21 + k/m, 0.7 - k/m, 1.0 - k/m)
            elif k < 4*m/5:
                glColor3f(0.2 + k/m, 0.69 - 4*k/(3*m), k/m)
            elif k == m:
                glColor3f(0.56, 0.0, 0.12)
            else:
                glColor3f(0.8, 0.1, 0.4)

            glVertex2i(x, y)
    glEnd()
    glFlush()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glFlush()


if __name__ == '__main__':
    datoteka = input('Unesite datoteku za citanje >> ')
    julie = input('Julie skup? [Y/N]: ')
    cr, ci = 0, 0
    with open(datoteka, 'r') as f:
        lines = f.readlines()
    eps = int(lines[0])
    m = int(lines[1])
    u_min = float(lines[2])
    u_max = float(lines[3])
    v_min = float(lines[4])
    v_max = float(lines[5])
    if julie.lower() == 'y':
        mandelbrot = False
        cr = float(lines[6])
        ci = float(lines[7])
    pyglet.app.run()

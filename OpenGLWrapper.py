from OpenGL.GL import *
from OpenGL.GLU import *


def draw_rect(rect, color):
    """First draft of a draw rectangle function."""
    x, y, w, h = rect
    r, g, b = color
    glBegin(GL_TRIANGLE_STRIP)
    # Set color
    glColor3f(r, g, b)
    # Bottom Left
    glVertex2f(x, y + h)
    # Top Left
    glVertex2f(x, y)
    # Bottom Right
    glVertex2f(x + w, y + h)
    # Top Right
    glVertex2f(x + w, y)
    glEnd()


def draw_point(x, y, scale, color):
    """Draw pretty much any shape anywhere."""
    glPushMatrix()
    glTranslate(x, y, 0)
    
    glPointSize(scale)
    glColor3f(*color)
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glEnd()

    glPopMatrix()


def draw_poly(x, y, vertices, color, draw_type=GL_TRIANGLES):
    """Draw pretty much any shape anywhere."""
    glPushMatrix()
    glTranslate(x, y, 0)
    glColor3f(*color)
    glBegin(draw_type)
    for v in vertices:
        glVertex2f(*v)
    glEnd()

    glPopMatrix()

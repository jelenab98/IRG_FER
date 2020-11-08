#include <windows.h>
#include <stdio.h>
#include <GL/glut.h>
#include <time.h>
#include <stdlib.h>

GLdouble Lx[2], Ly[2]; // pocetna i krajnja tocka linije
GLint Ix;   // oznaka stanja ovisno koliko je tocaka zadano
GLuint window;  // inicijalizacija prozora i zadavanje velicine
GLuint width = 600, height = 500;

int pamti = 0;
int promjena = 0;
int nacin = 0;

void myDisplay();
void myReshape(int width, int height);
void myMouse(int button, int state, int x, int y);
void myKeyboard(unsigned char theKey, int mouseX, int mouseY);
void myLine(GLint xa, GLint ya, GLint xb, GLint yb);
void pozitivni(GLint xa, GLint ya, GLint xb, GLint yb);
void negativni(GLint xa, GLint ya, GLint xb, GLint yb);
void crtajLD(GLint xa, GLint ya, GLint xb, GLint yb);
void crtajDL(GLint xa, GLint ya, GLint xb, GLint yb);
void crtajPrviNacin(GLint xa, GLint ya, GLint xb, GLint yb);
void crtajDrugiNacin(GLint xa, GLint ya, GLint xb, GLint yb);
void changeBackground();
void changeLine();
int main(int argc, char ** argv)
{
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(width, height);
	glutInitWindowPosition(100, 100);
	glutInit(&argc, argv);
    srand(time(0));
	window = glutCreateWindow("Vježba 2-Bresenhamov algoritam");
	glutReshapeFunc(myReshape);
	glutDisplayFunc(myDisplay);
	glutMouseFunc(myMouse);
	glutKeyboardFunc(myKeyboard);
	printf("Lijevom tipkom misa zadaj tocke - Bresenhamov algoritam\n");
	printf("Tipke r (red), g (green), b (blue), p (pink), k (black) i a (automatski) mijenjaju boju.\n");
	printf("Za automatsku promjenu boje pozadine stisnite q, a za zadrzavanje te pozadine jos jednom q.\n");
	printf("Za isprobavanje prvog ili drugog algoritma naizmjenicno pretisnite w.\n");

	glutMainLoop();
	return 0;
}
void myDisplay()
{
	printf("Pozvan myDisplay()\n");
	//glClearColor(r, g, b, 0.0f); //  boja pozadine
	//glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); //brisanje nakon svake iscrtane linije
	glFlush();
}
void myReshape(int w, int h)
{
	//printf("Pozvan myReshape()\n");
	width = w; height = h;               //promjena sirine i visine prozora
	Ix = 0;								//	indeks tocke 0-prva 1-druga tocka
	glViewport(0, 0, width, height);	//  otvor u prozoru

	glMatrixMode(GL_PROJECTION);		//	matrica projekcije
	glLoadIdentity();					//	jedinicna matrica
	gluOrtho2D(0, width, 0, height); 	//	okomita projekcija
	glMatrixMode(GL_MODELVIEW);			//	matrica pogleda
	glLoadIdentity();					//	jedinicna matrica

    //changeBackground();                 // promijeni boju pozadine preko moje funkcije
    glClearColor(1.0f, 1.0f, 1.0f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);
	glPointSize(1.5);					//	postavi velicinu tocke za liniju
	glColor3f(1.0f, 0.0f, 0.5f);		//	postavi boju linije
}

void changeBackground()
{
    float r, g, b;
	r = (float)(rand()%100)/100;
	g = (float)(rand()%100)/100;
	b = (float)(rand()%100)/100;
	//printf("%f %f %f",r,g,b);
    if (promjena == 1)
    {
	glClearColor(r, g, b, 0.0f); // boja pozadine
	glClear(GL_COLOR_BUFFER_BIT);
    }
    glRecti(width - 15, height - 15, width, height); // crta mali kvadrat u boji
	glFlush();
}

void changeLine()
{
    float r,g,b;
    r = (float)(rand()%100)/100;
	g = (float)(rand()%100)/100;
	b = (float)(rand()%100)/100;
	glColor3f(r,g,b);
}

//*********************************************************************************
//	Pojedinaèno rastavljene fukncije za doradu algoritma ovisno o tangensu.
//  Algoritam je raðen po primjeru iz knige gdje se provjerava
//  odnos toèaka, zamjenjuje poèenu i krajnju ukoliko je potrebno i iscrtava.
//  Ovakva dorada algoritma omoguæuje rad za sve kuteve i sve kvadrante.
//*********************************************************************************
void pozitivni(GLint xa, GLint ya, GLint xb, GLint yb)
{
    GLint x, y, a, d, k;
    if (yb-ya <= xb-xa)
    {
        a = 2*(yb-ya);
        y = ya;
        d = -(xb-xa);
        k = 2*d;
        glBegin(GL_POINTS);
        for(x = xa; x <= xb; x++)
        {
            glVertex2i(x,y);
            d += a;
            if (d >= 0)
            {
                d += k;
                y ++;
            }
        }
        glEnd();
    }
    else
    {
        a = 2*(xb-xa);
        y = xa;
        d = -(yb-ya);
        k = 2*d;
        glBegin(GL_POINTS);
        for(x = ya; x <= yb; x++)
        {
            glVertex2i(y,x);
            d += a;
            if (d >= 0)
            {
                d += k;
                y++;
            }
        }
        glEnd();

    }
}

void negativni(GLint xa, GLint ya, GLint xb, GLint yb)
{
    GLint x, y, a, d, k;
    if (-(yb-ya) <= xb-xa)
    {
        a = 2*(yb-ya);
        y = ya;
        d = xb-xa;
        k = 2*d;
        glBegin(GL_POINTS);
        for(x = xa; x <= xb; x++)
        {
            glVertex2i(x,y);
            d += a;
            if (d <= 0)
            {
                d += k;
                y--;
            }
        }
        glEnd();
    }
    else
    {
        a = 2*(xa-xb);
        y = xb;
        d = ya-yb;
        k = 2*d;
        glBegin(GL_POINTS);
        for(x = yb; x <= ya; x++)
        {
            glVertex2i(y,x);
            d += a;
            if (d <= 0)
            {
                d += k;
                y--;
            }
        }
        glEnd();
        }
}
void crtajLD(GLint xa, GLint ya, GLint xb, GLint yb)
{
    GLint x, y=ya, dx=xb-xa, dy=yb-ya, yi=1, D;

    if (dy < 0)
    {
        yi = -1;
        dy = -dy;
    }

    D = 2*dy - dx;

    glBegin(GL_POINTS);
    for(x=xa; x<=xb; x++)
    {
        glVertex2i(x,y);
        if (D > 0)
        {
            y += yi;
            D -= 2*dx;
        }
        D += 2*dy;
    }
    glEnd();
}
void crtajDL(GLint xa, GLint ya, GLint xb, GLint yb)
{
    GLint x=xa, y, xi=1, dx = xb-xa, dy=yb-ya, D;

    if (dx < 0)
    {
        xi = -1;
        dx = -dx;
    }

    D = 2*dx - dy;

    glBegin(GL_POINTS);
    for(y=ya; y<=yb;y++)
    {
        glVertex2i(x,y);
        if(D > 0)
        {
            x += xi;
            D -= 2*dy;
        }
        D += 2*dx;
    }
    glEnd();
}
void crtajPrviNacin(GLint xa, GLint ya, GLint xb, GLint yb)
{
    // implementacija algoritma iz knjige, nesto steka kod vertikalnih crta.
    if (xa <= xb)
    {
        if (ya <= yb)
        {
            pozitivni(xa, ya, xb, yb);
        }
        else
        {
            negativni(xa, ya, xb, yb);
        }
    }
    else
    {
        if (ya >= yb)
        {
            pozitivni(xb, yb, xa, ya);
        }
        else
        {
            negativni(xb, yb, xa, ya);
        }
    }
}
void crtajDrugiNacin(GLint xa, GLint ya, GLint xb, GLint yb)
{
    //druga verzija implementacije algoritma u kojima se drukcije ispituje odnos tocaka i
    // i onda se pozivaju funkcije ovisno o tome treba li crtati s L-D ili D-L
    if (abs(yb-ya) < abs(xb-xa))
    {
        if (xa > xb)
        {
            crtajLD(xb,yb,xa,ya);
        }
        else
        {
            crtajLD(xa,ya,xb,yb);
        }
    }
    else
    {
        if (ya > yb)
        {
            crtajDL(xb,yb,xa,ya);
        }
        else
        {
            crtajDL(xa,ya,xb,yb);
        }
    }
}
void myLine(GLint xa, GLint ya, GLint xb, GLint yb)
{
    changeBackground();                     // iscrtava se samo jedna linija i svaki put se promijeni boja ako je ukljuceno
	glBegin(GL_LINES);
	{
		glVertex2i(xa, ya + 20);			//	crtanje gotove linije
		glVertex2i(xb, yb + 20);
	}
	glEnd();

    if (nacin == 0) crtajPrviNacin(xa, ya, xb, yb);
    else crtajDrugiNacin(xa, ya, xb, yb);
}
void myMouse(int button, int state, int x, int y)
{
	//	Lijeva tipka - crta pocetnu tocku ili liniju.
	if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN)

	{
		//	Pamti krajnju tocke linije.
		Lx[Ix] = x;							//	upisi tocku
		Ly[Ix] = height - y;
		Ix = Ix ^ 1;						//	flip - druga tocka

											//	Crta prvu tocku ili liniju do druge tocke.
		if (Ix == 0)
        {
            if (pamti == 0) changeLine();
            myLine((int)Lx[0], (int)Ly[0], (int)Lx[1], (int)Ly[1]);
		}
		else
        {
            glVertex2i(x, height - y);
        }
		printf("Koordinate tocke %d: %d %d \n", Ix ^ 1, x, y);
		//printf("Linije: r-crveno, g-zeleno, b-plavo, p-rozo, k-crno, a-automatski.\nPozadine: q-automatski.\nNacin: w-promjena.\n");
		glFlush();
	}

	//	Desna tipka - brise canvas.
	else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN)
	{
		myReshape(width, height);
	}
}
void myKeyboard(unsigned char theKey, int mouseX, int mouseY)
{
	switch (theKey)
	{
	case 'r':
		glColor3f(1, 0, 0);
		pamti = 1;
		break;

	case 'g':
		glColor3f(0, 1, 0);
		pamti = 1;
		break;

	case 'b':
		glColor3f(0, 0, 1);
		pamti = 1;
		break;

	case 'k':
		glColor3f(0, 0, 0);
        pamti = 1;
        break;

    case 'p':
        glColor3f(1, 0, 0.5);
        pamti = 1;
        break;

    case 'a':
        pamti = (pamti+1)%2;
        changeLine();
        break;

    case 'q':
        promjena = (promjena+1)%2;
        break;

    case 'w':
        nacin = (nacin+1)%2;
	}
	glRecti(width - 15, height - 15, width, height); // crta mali kvadrat u boji
	glFlush();
}

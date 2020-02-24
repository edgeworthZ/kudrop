def FindQuadArea(p1,p2,h):
    area = 0.5 * (p1+p2) * h
    return area

w = float(input('Input w: '))
h = float(input('Input h: '))
a = float(input('Input a: '))
b = float(input('Input b: '))
c = float(input('Input c: '))

area = (w*h) - (2*FindQuadArea(b,c,a)+FindQuadArea(2*b,2*c,a))
print(f'Area: {area:.2f}')

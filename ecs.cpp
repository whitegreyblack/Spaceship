#include <stdio.h>
#include <iostream>

int globid = 0;

typedef struct { 
  int x, y; 
} Point;

typedef struct { 
  char symbol; 
  char foreground[8]; 
  char background[8]; 
} Render;

class Entity {
  int id;
  public:
    Entity(int id) : id(id) { globid++; }
    void print() const { std::cout << "Entity: " << id << std::endl; }
};

int main()
{
  Point p = {0, 1};
  printf("Point(x=%d, y=%d)\n", p.x, p.y);
  Render r = {'@', "#ffffff", "#000000"};
  printf("Render(s=%c, f=%s, b=%s)\n", r.symbol, r.foreground, r.background);
  Entity e(globid);
  e.print();
  Entity f(globid);
  f.print();
  return 0;
}

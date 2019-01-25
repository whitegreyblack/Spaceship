#include <stdio.h>
#include <iostream>

static int globid = 0;

typedef struct { 
  int x, y;
  void print() const { 
    std::cout << "Point(x=" << x << ", y=" << y << ")" << std::endl; 
  }
} Point;

typedef struct { 
  char symbol; 
  char foreground[8]; 
  char background[8]; 
  void print() const { 
    std::cout << "Render(s=" << symbol << ", f=" << foreground;
    std::cout << ", b=" << background << ")" << std::endl;
  }
} Render;

class Entity {
  int id;
  public:
    Entity(int id) : id(id) { globid++; }
    void print() const { 
      std::cout << "Entity: " << id << std::endl;
    }
};

int main()
{
  Point p = {0, 1};
  p.print();
  Render r = {'@', "#ffffff", "#000000"};
  r.print();
  Entity e(globid);
  e.print();
  Entity f(globid);
  f.print();
  printf("%p, %p, %p, %p\n", (void*)&p, (void*)&r, (void*)&e, (void*)&f);
  return 0;
}

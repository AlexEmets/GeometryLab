#include<iostream>
#include<vector>
#include<algorithm>
#include<fstream>

using namespace std;

struct pt {
	double x, y;
};

bool cmp (pt a, pt b) {
	return a.x < b.x || a.x == b.x && a.y < b.y;
}

bool cw (pt a, pt b, pt c) {
	return a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y) < 0;
}

bool ccw (pt a, pt b, pt c) {
	return a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y) > 0;
}

void convex_hull (vector<pt> & a) {
	if (a.size() == 1)  return;
	sort (a.begin(), a.end(), &cmp);
	pt p1 = a[0],  p2 = a.back();
	vector<pt> up, down;
	up.push_back (p1);
	down.push_back (p1);
	for (size_t i=1; i<a.size(); ++i) {
		if (i==a.size()-1 || cw (p1, a[i], p2)) {
			while (up.size()>=2 && !cw (up[up.size()-2], up[up.size()-1], a[i]))
				up.pop_back();
			up.push_back (a[i]);
		}
		if (i==a.size()-1 || ccw (p1, a[i], p2)) {
			while (down.size()>=2 && !ccw (down[down.size()-2], down[down.size()-1], a[i]))
				down.pop_back();
			down.push_back (a[i]);
		}
	}
	a.clear();
	for (size_t i=0; i<up.size(); ++i)
		a.push_back (up[i]);
	for (size_t i=down.size()-2; i>0; --i)
		a.push_back (down[i]);
}

int main()
{
    std::vector<pt> points;
    std::cout << "Ви хочете взяти множину точок з файлу чи з консольного вводу?(file,console)\n";
    std::string input_option;
    cin >> input_option;
    if(input_option == "file")
    {

    }
    if(input_option == "console")
    {
        int N;
        std::cout << "Введіть кількість точок:\n";
        std::cin >> N;
        
        for(int i = 0; i < N; i++)
        {
            double x,y;
            cin >> x >> y;
            points.push_back({x,y});
        }

    }
    else
    {
        std::cout << "Неправильний аргумент\n";
        return 0;
    }

    convex_hull(points);
    std::ofstream out("/home/oleksandryemets/Documents/University/GeometryLabs/GeometryLab/generated-polygon.csv");
    out << "SimpleFormat\nx,y\n";
    for(auto it: points)
    {
        out << it.x << "," << it.y << ", 0" << std::endl;
    }
}
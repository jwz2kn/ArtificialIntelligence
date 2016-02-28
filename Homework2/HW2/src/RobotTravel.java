import java.awt.Point;
import java.util.*;
import world.*;
public class RobotTravel extends Robot{
	Point start;
	Point destination;
	boolean uncertainty;
	int cols;
	int rows;
	Queue<Coordinate> coordinates;
	int[][] map;
	public RobotTravel(Point st, Point dest, boolean u) {
		super();
		start = st;
		destination = dest;
		uncertainty = u;
		coordinates = new LinkedList();
		map = new int[rows][cols];
	}
	
	@Override
	public void travelToDestination() {
		if (!uncertainty) {
//			super.getPosition();
//			System.out.println("travelToDestinaton is called");
//			System.out.println("Destination Coordinate: "
//					+"(" +destination.getX() + ", " + destination.getY() + 
//					") Destination String: "+super.pingMap(destination));
//			super.pingMap(destination);
//			System.out.println(super.pingMap(new Point(2,2)));
			
			
		}
		else {
			
		}
	}

	public int getCols() {
		return cols;
	}

	public void setCols(int cols) {
		this.cols = cols;
	}

	public int getRows() {
		return rows;
	}

	public void setRows(int rows) {
		this.rows = rows;
	}
	
	public void AStar(Point st, Point go) {
		List<Point> evaluated = new LinkedList<Point>();
		List<Point> notEvaluated = new LinkedList<Point>();
		notEvaluated.add(st);
		Map<Point, Point> cameFrom = new HashMap<Point, Point>();
		Map<Point, Double> gScore = new HashMap<Point, Double>();
		gScore.put(st, 0.0);
		Map<Point, Double> fScore = new HashMap<Point, Double>();
		fScore.put(st, heuristic(st, destination));
		while (!notEvaluated.isEmpty()) {
			double lowestCurrentScore = Collections.min(fScore.values());
			Point current = (Point) getKeyFromValue(fScore, lowestCurrentScore);
			if (current.equals(destination)) {
				reconstructPath(current, destination);
				return;
			}
			notEvaluated.remove(current);
			evaluated.add(current);
			
			//Generate adjacents
			List<Point> adj = new ArrayList<Point>();
			Point nw = new Point((int) current.getX() - 1, (int) current.getY() - 1);
			Point ne = new Point((int)current.getX() - 1, (int)current.getY() + 1);
			Point n = new Point((int)current.getX() - 1, (int)current.getY());
			Point w = new Point((int)current.getX(), (int)current.getY() - 1);
			Point sw = new Point((int)current.getX() + 1, (int)current.getY() - 1);
			Point s = new Point((int)current.getX() + 1, (int)current.getY());
			Point se = new Point((int)current.getX() + 1, (int)current.getY() + 1);
			Point ea = new Point((int)current.getX(), (int)current.getY() + 1);
			adj.add(nw); adj.add(ne); adj.add(n); adj.add(w);
			adj.add(sw); adj.add(s); adj.add(se); adj.add(ea);
			for (Point el : adj) {
				if (super.pingMap(new Point((int)el.getX(), (int)el.getY())) != null ||
					super.pingMap(new Point((int)el.getX(), (int)el.getY())).equals("X")){
					adj.remove(el);
				}
			} //Allowable adjacents fully generated
			
			//Now, for each neighbor of adjacent
			double tentative_gScore;
			for (Point neighbor: adj) {
				if (evaluated.contains(neighbor)) continue;
				tentative_gScore = gScore.get(current) + current.distance(neighbor);
				if (!notEvaluated.contains(neighbor)) {
					notEvaluated.add(neighbor);
				}
				else if (tentative_gScore > gScore.get(neighbor)) {
					continue;
				}
				cameFrom.put(neighbor, current);
				gScore.put(neighbor, tentative_gScore);
				fScore.put(neighbor, gScore.get(neighbor) + heuristic(current, neighbor));
			}
		}
		//return failure;
		return;
	}
	public void reconstructPath(Point cameFrom, Point current) {
		return;
	}
	
	//Modified Manhattan distance allowing for diagonal
	public Double heuristic(Point p, Point d) {
		double dx = Math.abs(p.getX() - d.getX());
		double dy = Math.abs(p.getY() - d.getY());
		return dx + dy - Math.min(dx, dy);
	}
//	public Double distBetween(Point current, Point neighbor) {
//		current.distance(neighbor);
//		return current.distance(neighbor);
//	}
	//Taken from Stackoverflow: 
	//http://stackoverflow.com/questions/1383797/java-hashmap-how-to-get-key-from-value/28415495#28415495
	public static Object getKeyFromValue(Map hm, Object value) {
        for (Object o : hm.keySet()) {
          if (hm.get(o).equals(value)) {
            return o;
          }
        }
        return null;
    }
    
}

//Coordinate end = new Coordinate((int) destination.getX(), (int)destination.getY(), 0);
//coordinates.add(end);
//System.out.println(coordinates.element().toString());
//for (Coordinate e : coordinates) {
//	List<Coordinate> adj = new ArrayList<Coordinate>();
//	Coordinate nw = new Coordinate(e.getX() - 1, e.getY() - 1, e.getCounter() + 1);
//	Coordinate ne = new Coordinate(e.getX() - 1, e.getY() + 1, e.getCounter() + 1);
//	Coordinate n = new Coordinate(e.getX() - 1, e.getY(), e.getCounter() + 1);
//	Coordinate w = new Coordinate(e.getX(), e.getY() - 1, e.getCounter() + 1);
//	Coordinate sw = new Coordinate(e.getX() + 1, e.getY() - 1, e.getCounter() + 1);
//	Coordinate s = new Coordinate(e.getX() + 1, e.getY(), e.getCounter() + 1);
//	Coordinate se = new Coordinate(e.getX() + 1, e.getY() + 1, e.getCounter() + 1);
//	Coordinate ea = new Coordinate(e.getX(), e.getY() + 1, e.getCounter() + 1);
//	if (super.pingMap(new Point(nw.getX(), nw.getY())) != null) {
//		adj.add(nw);
//	}
//	if (super.pingMap(new Point(ne.getX(), ne.getY())) != null) {
//		adj.add(ne);
//	}
//	if (super.pingMap(new Point(n.getX(), n.getY())) != null) {
//		adj.add(n);
//	}
//	if (super.pingMap(new Point(w.getX(), w.getY())) != null) {
//		adj.add(w);
//	}
//	if (super.pingMap(new Point(sw.getX(), sw.getY())) != null) {
//		adj.add(sw);
//	}
//	if (super.pingMap(new Point(s.getX(), s.getY())) != null) {
//		adj.add(s);
//	}
//	if (super.pingMap(new Point(se.getX(), se.getY())) != null) {
//		adj.add(se);
//	}
//	if (super.pingMap(new Point(ea.getX(), ea.getY())) != null) {
//		adj.add(ea);
//	}
//	for (Coordinate el : adj) {
//		if (super.pingMap(new Point(el.getX(), el.getY())).equals("X")){
//			adj.remove(el);
//		}
//		for (Coordinate a: coordinates) {
//			if (a.getX() == el.getX() && a.getY() == el.getY()
//					&& a.getCounter() > el.getCounter()) {
//				adj.remove(el);
//				break;
//			}
//		}
//	}
//	for (Coordinate el : adj) {
//		coordinates.add(el);
//	}
//}

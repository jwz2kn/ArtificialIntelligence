import java.awt.Point;
import java.util.*;
import world.*;

public class RobotTravel extends Robot{
	// Fields
	private Point start;
	private Point destination;
	private boolean uncertainty;
	private int cols;
	private int rows;
	private Map<Point, Point> cameFrom;
	private static List<Point> evaluated;
	private static List<Point> notEvaluated;

	// Constructor
	public RobotTravel(Point st, Point dest, boolean u, int c, int r) {
		//We'll the info for start, destination, uncertainty, columns, and rows to generate a path.
		super();
		start = st;
		destination = dest;
		uncertainty = u;
		cols = c;
		rows = r;
	}
	
	@Override
	public void travelToDestination() {
		if (!uncertainty) {
			//Generate a path as a list of points to travel to.
			long startTime = System.nanoTime();
			List<Point> path = AStar(start, destination);
			long estimatedTime = System.nanoTime() - startTime;
			System.out.println("Time it took to generate path: " + Math.pow(10,-9)*estimatedTime + " s");
			if (!path.isEmpty() && path != null) {
				for(int i = 0; i < path.size(); i++) {
					super.move(path.get(i));
				}
			} else {
				System.out.println("You were either at the destination already or there wasn't a valid path to get there!");
			}
			
		}
		else {
			long startTime = System.nanoTime();
			List<Point> path = AStar(start, destination);
			long estimatedTime = System.nanoTime() - startTime;
			System.out.println("Time it took to generate path: " + Math.pow(10,-9)*estimatedTime + " s");
			if (!path.isEmpty() && path != null) {
				for(int i = 0; i < path.size(); i++) {
					super.move(path.get(i));
				}
			} else {
				System.out.println("You were either at the destination already or there wasn't a valid path to get there!");
			}
		}
	}
	
	public List<Point> AStar(Point st, Point go) {
		//Based on pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm

		//Lists of evaluated and not evaluated Points (which are the nodes in this case)
		evaluated = new ArrayList<Point>();
		notEvaluated = new ArrayList<Point>();
		notEvaluated.add(st);

		//Key Value pairs of Point to Point. IE, when this is full, it essentially has the moves the robot should make.
		cameFrom = new HashMap<Point, Point>();
		
		//Map of g scores, initialized to postive infinity for every Point
		Map<Point, Double> gScore = new HashMap<Point, Double>();
		//Put default value of positive infinity into map
		for (int i = 0; i < rows; i++) { //x axis
			for (int j = 0; j < cols; j++) { //y axis
				gScore.put(new Point(i, j), Double.POSITIVE_INFINITY);
			}
		}
		//Cost of start going to start is zero.
		gScore.put(st, 0.0);
		
		//Map of f scores, initialized to positive infinity for every point
		Map<Point, Double> fScore = new HashMap<Point, Double>();
		//Put default value of positive infinity into map
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				fScore.put(new Point(i, j), Double.POSITIVE_INFINITY);
			}
		}
		//Cost of start going to goal as estimated by the heuristic initially.		
		fScore.put(st, heuristic(st, go));
		
		// While there's still nodes to be evaluated, keep evaluating.
		while (notEvaluated.isEmpty() == false) {
			
			// Find node with the lowest score.
			// Go to the method getKeyFromValue for more detail.
			double lowestCurrentScore = Collections.min(fScore.values());
			Point current = (Point) getKeyFromValue(fScore, lowestCurrentScore);
			
			// If the current point doesn't exist, something's really wrong! Break. 
			if (current == null) { 
				break; 
			}
			
			// If current node is equals goal, then we've generated a full path, and can go reconstruct it into a list.
			if ((int) current.getX() == (int) go.getX() && (int) current.getY() == (int) go.getY()) {
				return reconstructPath(cameFrom, go);
			}
			
			// Add current node to evaluated and take it from notEvaluated.
			if (notEvaluated.contains(current)) notEvaluated.remove(current);
			if (!evaluated.contains(current)) evaluated.add(current);
			
			//Generate adjacent nodes of current node.
			List<Point> adj = generateAdjacents(current);

			//Now, for each adjacent node to the current, evaluate the fScores and gScores.
			double tentative_gScore;
			int counter = 0;
			for (Point neighbor: adj) {
				if (evaluated.contains(neighbor)) {
					continue;
				}

				tentative_gScore = gScore.get(current) + heuristic(current, neighbor);

				if (!notEvaluated.contains(neighbor)) {
					notEvaluated.add(neighbor);
				}
				else if (tentative_gScore >= gScore.get(neighbor)) {
					continue;
				}
				if (uncertainty){
					if (!walls.contains(neighbor)) {
						if (!notEvaluated.contains(neighbor)) notEvaluated.add(neighbor);
						cameFrom.put(neighbor, current);	
						gScore.put(neighbor, tentative_gScore);
						double h = gScore.get(neighbor) + heuristic(neighbor, go);
						//Tiebreaking. This reduces this current path's fScore, because it's the most efficient thus far.
						while (fScore.values().contains(h))
							h *= 0.999;
						fScore.put(neighbor, h);
					}

				}
				else {
					if (!super.pingMap(neighbor).equals("X")) {
						if (!notEvaluated.contains(neighbor)) notEvaluated.add(neighbor);
						cameFrom.put(neighbor, current);
						gScore.put(neighbor, tentative_gScore);
						double h = gScore.get(neighbor) + heuristic(neighbor, go);
						//Tiebreaking. This reduces this current path's fScore, because it's the most efficient thus far.
						while (fScore.values().contains(h))
							h *= 0.999;
						fScore.put(neighbor, h);
					}
				}
			}

			fScore.remove(current);
		}
		// No path generated, return empty list.
		return new ArrayList<Point>();
	}

	//Generate adjacent points--- Doesn't remove walls, but does remove nulls.
	public List<Point> generateAdjacents(Point current) {
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
		
		// Remove the nodes that return null upon pinging--- Those are outside the boundaries of the map.
		Iterator<Point> i = adj.iterator();
		while (i.hasNext()) {
			Point el = i.next();
			if (el.getX() >= rows || el.getY() >= cols || el.getX() < 0 || el.getY() < 0) {
				i.remove();
			}
		} //Allowable adjacents fully generated
		return adj;
	}


	//Take a Map of Point to Point (which theoretically would include all the mappings of node to node for correct path)
	// and construct a list from that Map up until the passed in current point.
	public List<Point> reconstructPath(Map<Point, Point> cameFrom, Point current) {
		List<Point> totalPath = new ArrayList<Point>();
		totalPath.add(current);
		while (cameFrom.keySet().contains(current)) {
			current = cameFrom.get(current);
			totalPath.add(current);
		}
		Collections.reverse(totalPath);
		return totalPath;
	}
	
	// Modified Manhattan distance allowing for diagonal, where the cost of moving diagonally is slightly greater than moving straight, but is not Euclidean in cost,
	// not Chebyshev distance, or pure, unmodified Manhattan distance.
	// http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
	private List<Point> walls = new ArrayList<Point>();
	private List<Point> nonWalls = new ArrayList<Point>();
	public Double heuristic(Point p, Point d) {
		double dx = Math.abs(p.getX() - d.getX());
		double dy = Math.abs(p.getY() - d.getY());
		if (uncertainty && !walls.contains(d) && !nonWalls.contains(d)) {
			int numOfX = 0;
			int numPings = (int) Math.pow(Math.max(cols, rows), 2);
			for (int i = 0; i < numPings; i++) {
				String current = super.pingMap(d);
				if (current.equals("X")) numOfX++;
				if (numOfX > numPings/2 ) { walls.add(d); return 10000.0; }
			}
			nonWalls.add(d);
		}
		return dx + dy + (-0.6)*Math.min(dx, dy);
	}

	//Adapted from Stackoverflow: 
	//http://stackoverflow.com/questions/1383797/java-hashmap-how-to-get-key-from-value/28415495#28415495
	// Look in a map and find a Point based on the Double value. In this case, that means we look through fScore table for a certain fScore
	// and find the point associated.
	public static Object getKeyFromValue(Map<Point, Double> hm, Object value) {
        for (Object o : hm.keySet()) {
          if (hm.get(o).equals(value)) {
        	  if (!evaluated.contains(o)) {
        		  return o;
        	  }
          }
        }
        return null;
    }
}
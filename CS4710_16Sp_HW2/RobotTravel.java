import java.awt.Point;
import java.util.*;
import world.*;

//Please read the DStarLite method, the computeShortestPath, and updateVertex methods.
//Sourced from http://pub1.willowgarage.com/~konolige/cs225b/dlite_tro05.pdf
	//Top of page 3 describing U, and page 4.
//Also looked at insights from https://www.cs.cmu.edu/afs/cs.cmu.edu/Web/People/maxim/files/hsplanguide_icaps05ws.pdf

//Currently, our code is getting stuck in an infinite loop in computeShortestPath. We think it might be to do with the movement to a wall, or maybe incorrect assumptions
//about what constitutes a predecessor or successor node.

public class RobotTravel extends Robot{
	// Fields
	Point start;
	Point destination;
	boolean uncertainty;
	int cols;
	int rows;
	Map<Point, Point> cameFrom;
	static List<Point> evaluated;
	static List<Point> notEvaluated;

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
			System.out.println("Path: " + path.toString());
			if (!path.isEmpty() && path != null) {
				for(int i = 0; i < path.size(); i++) {
					super.move(path.get(i));
				}
			} else {
				System.out.println("You were either at the destination already or there wasn't a valid path to get there!");
			}
			
		}
		else {
			DStarLite();
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
		System.out.println("gScores: " + gScore.toString());
		
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
		System.out.println("fScores: " + fScore.toString());
		
		//Switch != and == to turn loop on and off
		int bigWhile = 0;
		// While there's still nodes to be evaluated, keep evaluating.
		while (notEvaluated.isEmpty() == false) {
			
			//System.out.println(notEvaluated.toString());
			System.out.println("----------------------------------------------------------------");
			System.out.println("Iteration of big while loop: " + bigWhile++);
			System.out.println("Came From: " + cameFrom.toString());
			System.out.println("Start: " + st.toString());
			
			// Find node with the lowest score. Currently, this is part of what's causing us problems with test cases that have walls.
			// Go to the method getKeyFromValue for more detail.
			double lowestCurrentScore = Collections.min(fScore.values());
			Point current = (Point) getKeyFromValue(fScore, lowestCurrentScore);
			
			// If the current point doesn't exist, something's really wrong! Break. 
			// Considering removing this statement, but we're getting errors unless we keep it in. Might modify getKeyFromValue further...
			if (current == null) { 
				System.out.println("Lowest current fScore: " + lowestCurrentScore);
				System.out.println("fScores: " + fScore.toString());
				System.out.println("Current is null"); break; 
			}
			System.out.println("Lowest current fScore: " + lowestCurrentScore);
			System.out.println("fScores: " + fScore.toString());
			//current.equals(destination)
			
			// If current node is equals goal, then we've generated a full path, and can go reconstruct it into a list.
			if ((int) current.getX() == (int) go.getX() && (int) current.getY() == (int) go.getY()) {
				return reconstructPath(cameFrom, go);
			}
			
			// Add current node to evaluated and take it from notEvaluated.
			if (notEvaluated.contains(current)) notEvaluated.remove(current);
			if (!evaluated.contains(current)) evaluated.add(current);
			System.out.println("Current: " + current.toString());
			
			//Generate adjacent nodes of current node.
			List<Point> adj = generateAdjacents(current);
			System.out.println("Allowable adjacents fully generated.");
			System.out.println("Allowable adjacents: " + adj.toString());

			//Now, for each adjacent node to the current, evaluate the fScores and gScores.
			double tentative_gScore;
			int counter = 0;
			for (Point neighbor: adj) {
				System.out.println(counter++);
				System.out.println(heuristic(current, neighbor));

				// Here we tried multiple ways of writing the algorithm, and multiple ways of dealing with the walls.

				if (evaluated.contains(neighbor)) {
					System.out.println("Neighbor already evaluated!");
					continue;
				}
				//Pseudocode from wikipedia:
				// The distance from start to goal passing through current and the neighbor.
        		//tentative_gScore := gScore[current] + dist_between(current, neighbor)

				//Based this section on https://en.wikipedia.org/wiki/Talk:A*_search_algorithm#Dubious
				//tentative_gScore = gScore.get(current) + manhattan(current, neighbor);

				//The more we weight pure manhattan and less we weight the modified manhattan here, the more our path tends to be straight.
				//But we've noticed that weighting towards manhattan increases the number of pings.
				//This becomes a matter of optimizing between number of pings and how straight/natural looking you want the path to be!
				//It really doesn't affect the number of moves much.
				//tentative_gScore = gScore.get(current) + current.distance(neighbor);
				//tentative_gScore = gScore.get(current) + 0.3*heuristic(current, neighbor) + 0.7*manhattan(current, neighbor);
				//tentative_gScore = gScore.get(current) + manhattan(current, neighbor);

				//Can also just change the heuristic such that diagonals are weighted more heavily. Which, again, the more you weight diagonals, 
				//in a lot of cases, the more pings. In our case, we chose the cost of the diagonal to be 1.4 and cost of straight move to be 1.
				tentative_gScore = gScore.get(current) + heuristic(current, neighbor);
				System.out.println("Tentative gScore of " + neighbor.toString() + ": "+tentative_gScore);
				if (!notEvaluated.contains(neighbor)) {
					System.out.println("Neighbor added to notEvaluated.");
					notEvaluated.add(neighbor);
				}
				else if (tentative_gScore >= gScore.get(neighbor)) {
					System.out.println("tentative_gScore >= neighbor gScore");
					continue;
				}
				if (!super.pingMap(neighbor).equals("X")) {
					if (!notEvaluated.contains(neighbor)) notEvaluated.add(neighbor);
					//tentative_gScore = gScore.get(current) + heuristic(current, neighbor);
					cameFrom.put(neighbor, current);
					//cameFrom.put(current, neighbor);
					gScore.put(neighbor, tentative_gScore);
					double h = gScore.get(neighbor) + heuristic(neighbor, go);
					//Tiebreaking. This reduces this current path's fScore, because it's the most efficient thus far.
					while (fScore.values().contains(h))
						h *= 0.999;
					fScore.put(neighbor, h);
					
					System.out.println("fScore of neighbor: " + fScore.get(neighbor).toString());
				}
			}
			System.out.println("Not Evaluated Nodes: " + notEvaluated.toString());
			System.out.println("Evaluated Nodes: " + evaluated.toString());

			fScore.remove(current);
		}
		System.out.println("While loop exited, with failure.");

		// No path generated, return empty list.
		return new ArrayList<Point>();
	}

	//Generate adjacent points--- Doesn't remove walls, but does remove walls.
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
		System.out.println("All adj before removing invalids: " + adj.toString());

		// Remove the nodes that return null upon pinging--- Those are outside the boundaries of the map.
		Iterator<Point> i = adj.iterator();
		while (i.hasNext()) {
			Point el = i.next();
			//if (super.pingMap(new Point((int)el.getX(), (int)el.getY())) == null) {
			if (el.getX() >= rows || el.getY() >= cols || el.getX() < 0 || el.getY() < 0) {
				System.out.println(el.toString());
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
			System.out.println("Path Reconstructing...");
		}
		Collections.reverse(totalPath);
		return totalPath;
	}
	
	// Modified Manhattan distance allowing for diagonal, where the cost of moving diagonally is slightly greater than moving straight, but is not Euclidean in cost,
	// not Chebyshev distance, or pure, unmodified Manhattan distance.
	// http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
	public Double heuristic(Point p, Point d) {
		double dx = Math.abs(p.getX() - d.getX());
		double dy = Math.abs(p.getY() - d.getY());
		//return dx + dy + (-1)*Math.min(dx, dy);
		return dx + dy + (-0.6)*Math.min(dx, dy);
		//return Math.max(dx, dy);
		//return p.distance(d);
	}

	//Pure Manhattan distance.
	public Double manhattan(Point p, Point d) {
		double dx = Math.abs(p.getX() - d.getX());
		double dy = Math.abs(p.getY() - d.getY());
		return dx + dy;
	}

	//Adapted from Stackoverflow: 
	//http://stackoverflow.com/questions/1383797/java-hashmap-how-to-get-key-from-value/28415495#28415495
	// Look in a map and find a Point based on the Double value. In this case, that means we look through fScore table for a certain fScore
	// and find the point associated.
	public static Object getKeyFromValue(Map<Point, Double> hm, Object value) {
        for (Object o : hm.keySet()) {
          if (hm.get(o).equals(value)) {
          	  // So, here's some of the problem: We originially were stuck in an infinite loop because getKeyFromValue kept on
          	  // finding the nodes that had already been evaluated. We added this if statement to prevent that loop, and test case 1 worked!

              // Unfortunately, what's happening now is that when we're dealing with a wall, in test cases 2, 3, and 4, we end up not finding
          	  // a Point associated with the fScore values, so we return null, and thus can't properly construct a path with points.

          	  // Have tried several different ways of doing the A* algorithm, to no avail.
        	  if (!evaluated.contains(o)) {
        		  return o;
        	  }

          }
        }
        return null;
    }

    //-------------------------------------------------------------------------------------------------------------------------------
    private Map<Point, Double> g;
	private Map<Point, Double> f;
	private Map<Point, Vector<Double>> U;
    private Map<Point, Double> rhs;
    private Double[][] edgeC;

    //Tried to implement according to top of page 4 at http://pub1.willowgarage.com/~konolige/cs225b/dlite_tro05.pdf
    public void DStarLite() {
    	initialize();
    	computeShortestPath();
    	int counter = 0;
    	System.out.println("While loop started!");

	// while start != destination
    	while(start.getX() != destination.getX() || start.getY() != destination.getY()) {
    		System.out.println("Iteration: " + counter++);
    		List<Point> succ = generateAdjacents(start);
    		double minOfSucc = Double.POSITIVE_INFINITY;

		// looping through list of adjacents
    		for (Point s: succ) {
    			if (heuristic(start, s) + g.get(s) < minOfSucc) {
    				minOfSucc = heuristic(start, s) + g.get(s);
    				start = s;
    			}
    		}
    		Point currentPosition = super.getPosition();
    		Point movement = super.move(start);
    		//Pseudocode:
    		//if movement == currentPosition, then move did not work. Change the edge cost of start to infinity.
    		//else movement worked. edge costs might still change? in any case, do the necessary changes, scan graph for changes
	    		//No, it's if the cost of any node to another node has changed. IE, if move worked?
			boolean edgeCostChanged = false;
			if (movement.equals(currentPosition)) {
			    edgeC[(int) currentPosition.getX()][(int) currentPosition.getY()] = Double.POSITIVE_INFINITY;
			    edgeCostChanged = true;
			}
    
    		// Map<Vector<Point>, Double> changedEdgeCosts = new HashMap<Vector<Point>, Double>();
    		if (edgeCostChanged) {
		    // Update the edge cost = heuristic (first element, second element)
		    updateVertex(movement); 
    			for (Point s: U.keySet()) { // NOT SURE IF THIS WOULD WORK, DUE TO CONCURRENCY ISSUES
    				U.put(s, calcKey(s));
    			}
    			computeShortestPath();
    		}
    	}
    	return;
	}

    // initialize and populate global variables with initial data
    public void initialize() {
		// g maps each point to its start heuristic cost estimates
		g = new HashMap<Point, Double>();

		// rhs maps each point to its start heuristic cost estimates based on the g values of its predecessors
		rhs = new HashMap<Point, Double>();

		// 
		//f = new HashMap<Point, Double>();

		// U maps each point to a vector containing the minimum of g(s) and (rhs(s) + h(s,s_goal)), and the minimum of g(s) and rhs(s)
		// This acts as a priority queue that stores those vectors for each point on the map. Priority between vectors is described further in findMinVector
		U = new HashMap<Point, Vector<Double>>();

		// array containing the edge costs of each point, which is 1.0 unless the point is a wall.
		// This is our attempt to "scan the graph" for changes in edge costs
		edgeC = new Double[rows][cols];

		// populating g, rhs, and edgeC
		for (int i = 0; i < rows; i++) { //x axis
		    for (int j = 0; j < cols; j++) { //y axis
			g.put(new Point(i, j), Double.POSITIVE_INFINITY);
			rhs.put(new Point(i, j), Double.POSITIVE_INFINITY);
			edgeC[i][j] = 1.0;
		    }
		}
		rhs.put(destination, 0.0);
		U.put(destination, calcKey(destination));
    }

    public void updateVertex(Point current) {
		if (!(current.getX() == destination.getX() && current.getY() == destination.getY())) {
		    double min = Double.POSITIVE_INFINITY;
		    List<Point> succ = generateAdjacents(current);
		    for (Point s_prime : succ) {
				if (g.get(s_prime) + heuristic(current, s_prime) < min) min = g.get(s_prime) + heuristic(current, s_prime);
		    }
		    rhs.put(current, min);
		}
		if (U.keySet().contains(current)) U.remove(current);
		if (g.get(current) != rhs.get(current)) U.put(current, calcKey(current));
    }

	// public double findMinInVector(Map<Point, Vector<Double>> map) {
	// 	double min = Double.POSITIVE_INFINITY;

 //        for (Vector<Double> v : map.values()) {
 //          if (Math.max(v.get(0), v.get(1)) < min) {	
 //        	min = Math.max(v.get(0), v.get(1));
 //          }
 //        }
	// 	return min;
	// }

    // returns minimum vector in map according to lexiconographic ordering
	public Vector<Double> findMinVector(Map<Point, Vector<Double>> map) {
		Vector<Double> minVec = new Vector<Double>();
		minVec.add(Double.POSITIVE_INFINITY);
		minVec.add(Double.POSITIVE_INFINITY);
		for (Vector<Double> v: map.values()) {
			if (vectorLessThan(v, minVec)) minVec = v;
		}
		return minVec;
	}

    // returns whether vector a is less than vector b according to lexicographic ordering
	public boolean vectorLessThan(Vector<Double> a, Vector<Double> b) {
		boolean result = false;
		if (a.get(0) < b.get(0)) result = true;
		if (a.get(0) == b.get(0) && a.get(1) <= b.get(1)) result = true;
		return result;
	}

    // returns whether two vectors are equal
	public boolean vectorEqual(Vector<Double> a, Vector<Double> b) {
		boolean result = false;
		if (a.get(0) == b.get(0) && a.get(1) == b.get(1)) result = true;
		return result;
	}

	public Point getVectorKeyFromValue(Map<Point, Vector<Double>> hm, Vector<Double> v) {
        for (Point p : hm.keySet()) {
          if (vectorEqual(hm.get(p), v)) {
        		  return p;
          }
        }
        return null;
    }

    // Compute the shortest path to take. This assumes that predecessors are the adjacent(neighboring) nodes. Not sure if that is a correct assumption.
	public void computeShortestPath() {
		int counter = 0;
		// while (Math.min(U.get((Point) getVectorKeyFromValue(U, findMinInVector(U))).get(0), U.get((Point) getVectorKeyFromValue(U, findMinInVector(U))).get(1) )
		// 	< Math.min(calcKey(start).get(0), calcKey(start).get(1)) ||
		// 	rhs.get(start) != g.get(start)) {
		// while (Math.min(U.get((Point) getVectorKeyFromValue(U, findMinInVector(U))).get(0), U.get((Point) getVectorKeyFromValue(U, findMinInVector(U))).get(1) )
		// 	< Math.min(U.get(start).get(0), U.get(start).get(1)) ||
		// 	rhs.get(start) != g.get(start)) {
		while (vectorLessThan(findMinVector(U), calcKey(start)) || rhs.get(start) != g.get(start)) {

			System.out.println("Iteration of computeShortestPath: " + counter++);
			System.out.println("U.TopKey: " + findMinVector(U) + " calcKey(s_start): " + calcKey(start));

			Point current = (Point) getVectorKeyFromValue(U, findMinVector(U));
			U.remove(current);

			System.out.println("Current point: " + current);

			if (g.get(current) > rhs.get(current)) {
				g.put(current, rhs.get(current));
				List<Point> pred = generateAdjacents(current);
				for (Point s: pred) {
					updateVertex(s);
				}
			}
			else {
				g.put(current, Double.POSITIVE_INFINITY);
				List<Point> pred = generateAdjacents(current);
				pred.add(current);
				for (Point s: pred) {
					updateVertex(s);
				}				
			}
		}
	}

	// rhs = 0 or rhs = min of those values. See middle of page 3 at http://pub1.willowgarage.com/~konolige/cs225b/dlite_tro05.pdf
	public Double calcRhs(Point current) {
		double min = Double.POSITIVE_INFINITY;
		if (current.getX() == destination.getX() && current.getY() == destination.getY()) min = 0;		
		else {
			List<Point> pred = generateAdjacents(current);
			for (Point s_prime : pred) {
				if (g.get(s_prime) + heuristic(s_prime, current) < min) min = g.get(s_prime) + heuristic(s_prime, current);
			}
		}
		return min;
	}

	// Calculate the key to be stored in the map U.
	public Vector<Double> calcKey(Point current) {
		Vector<Double> result = new Vector<Double>();
		result.add(Math.min(g.get(current), calcRhs(current) + heuristic(current, destination)));
		result.add(Math.min(g.get(current), calcRhs(current)));
		return result;
	}

	// https://en.wikipedia.org/wiki/Iterative_deepening_A*
	//	private Point current;


	// private List<Point> successors = new ArrayList<Point>();
	// private double bound;

	// public void idaStar(Point st) {
	// 	//bound = heuristic(st);

	// }
    
}

//public Double distBetween(Point current, Point neighbor) {
//current.distance(neighbor);
//return current.distance(neighbor);
//}

//public int getCols() {
//return cols;
//}
//
//public void setCols(int cols) {
//this.cols = cols;
//}
//
//public int getRows() {
//return rows;
//}
//
//public void setRows(int rows) {
//this.rows = rows;
//}


				//Pseudocode from wikipedia:
				// The distance from start to goal passing through current and the neighbor.
        		//tentative_gScore := gScore[current] + dist_between(current, neighbor)

				//Based this section on https://en.wikipedia.org/wiki/Talk:A*_search_algorithm#Dubious
				//tentative_gScore = gScore.get(current) + manhattan(current, neighbor);

				//The more we weight pure manhattan and less we weight the modified manhattan here, the more our path tends to be straight.
				//But we've noticed that weighting towards manhattan increases the number of pings.
				//This becomes a matter of optimizing between number of pings and how straight/natural looking you want the path to be!
				//It really doesn't affect the number of moves much.
				// tentative_gScore = gScore.get(current) + 0.2*heuristic(current, neighbor) + 0.8*manhattan(current, neighbor);
				// if (notEvaluated.contains(neighbor) && tentative_gScore < gScore.get(neighbor)) {
				// 	notEvaluated.remove(neighbor);
				// 	//if(!evaluated.contains(neighbor)) evaluated.add(neighbor);
				// 	continue;
				// }
				// else if (evaluated.contains(neighbor) && tentative_gScore < gScore.get(neighbor)) {
				// 	evaluated.remove(neighbor);
				// 	//if(!notEvaluated.contains(neighbor)) notEvaluated.add(neighbor);
				// 	continue;
				// }

				// else if (!notEvaluated.contains(neighbor) && !evaluated.contains(neighbor) && !super.pingMap(neighbor).equals("X")) {
				// 	// https://en.wikipedia.org/wiki/A*_search_algorithm
				// 	// This path is the best until now. Record it!
				// 	System.out.println("Being run");
					
				// 	//tentative_gScore = gScore.get(current) + heuristic(current, neighbor);
				// 	cameFrom.put(neighbor, current);
				// 	gScore.put(neighbor, tentative_gScore);
				// 	double h = gScore.get(neighbor) + heuristic(neighbor, go);
				// 	//Tiebreaking. This reduces this current path's fScore, because it's the most efficient thus far. Helps differientiate it.
				// 	while (fScore.values().contains(h))
				// 		h *= 0.999;
				// 	fScore.put(neighbor, gScore.get(neighbor) + heuristic(neighbor, go));
				// 	notEvaluated.add(neighbor);
				// }
				// else {
				// 	notEvaluated.add(neighbor);
				// }

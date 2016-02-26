import java.awt.Point;

import world.*;
public class RobotTravel extends Robot{
	Point start;
	Point destination;
	
	public RobotTravel(Point st, Point dest) {
		super();
		start = st;
		destination = dest;
	}
	
	@Override
	public void travelToDestination() {
		super.pingMap(new Point(2, 2));
		super.getPosition();
		System.out.println(destination.toString());
		super.pingMap(destination);
	}
}

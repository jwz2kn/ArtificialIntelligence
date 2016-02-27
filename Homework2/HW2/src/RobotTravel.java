import java.awt.Point;

import world.*;
public class RobotTravel extends Robot{
	Point start;
	Point destination;
	boolean uncertainty;
	
	public RobotTravel(Point st, Point dest, boolean u) {
		super();
		start = st;
		destination = dest;
		uncertainty = u;
	}
	
	@Override
	public void travelToDestination() {
		if (!uncertainty) {
			super.pingMap(new Point(2, 2));
			super.getPosition();
			System.out.println(destination.toString());
			super.pingMap(destination);
		}
		else {
			
		}
	}
}

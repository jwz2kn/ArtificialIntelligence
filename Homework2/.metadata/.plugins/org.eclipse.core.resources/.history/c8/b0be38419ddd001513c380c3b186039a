import world.*;

public class RobotTravelTester {

	public static void main(String[] args) {
		try {
			//https://en.wikipedia.org/wiki/Pathfinding#Algorithms_used_in_pathfinding
			/*
			* Create a world. Pass the input filename first.
			* Second parameter is whether or not the world is uncertain.
			*/
			boolean uncertainty = false;
			World myWorld = new World ("myInputFile1.txt", uncertainty );
			System.out.println("monkey dicks");
			/* Create a robot that will run around in myWorld */
			RobotTravel myRobot 
				= new RobotTravel(myWorld.getStartPos(), myWorld.getEndPos(), uncertainty);
			myRobot.addToWorld (myWorld);
			// Tell the robot to travel to the destination .
			// You will be implementing this method yourself !
			myRobot.travelToDestination();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}

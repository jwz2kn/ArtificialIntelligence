import world.*;

public class RobotTravelTester {

	public static void main(String[] args) {
		try {
			//https://en.wikipedia.org/wiki/A*_search_algorithm

			/*
			* Create a world. Pass the input filename first.
			* Second parameter is whether or not the world is uncertain.
			*/

			boolean uncertainty =  false;
			String input = "TestCases/myInputFile1.txt";

			World myWorld = new World (input, uncertainty );
			
			/* Create a robot that will run around in myWorld */
			RobotTravel myRobot 
				= new RobotTravel(myWorld.getStartPos(), myWorld.getEndPos(), 
						myWorld.getUncertain(), myWorld.numCols(), myWorld.numRows());
			myRobot.addToWorld (myWorld);

			int GUImult = Integer.parseInt(input.replaceAll("[\\D]", ""));
			myWorld.createGUI(GUImult*280, GUImult*200, 300 - 20*(GUImult-1));
			// Tell the robot to travel to the destination.
			// You will be implementing this method yourself !
			myRobot.travelToDestination();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}

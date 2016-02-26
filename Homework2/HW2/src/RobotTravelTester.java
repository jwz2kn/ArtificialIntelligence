import world.World;

public class RobotTravelTester {

	public static void main(String[] args) {
		try {
			/*
			* Create a world . Pass the input filename first .
			* Second parameter is whether or not the world is uncertain .
			*/
			World myWorld = new World ("myInputFile.txt ", false );
			/* Create a robot that will run around in myWorld */
			RobotTravel myRobot = new RobotTravel() ;
			myRobot.addToWorld ( myWorld );
			// Tell the robot to travel to the destination .
			// You will be implementing this method yourself !
			myRobot.travelToDestination () ;
		} catch ( Exception e) {
			e.printStackTrace () ;
		}

	}

}

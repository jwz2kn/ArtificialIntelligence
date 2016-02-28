
public class Coordinate {
	protected int x;
	protected int y;
	protected int counter;
	public Coordinate() {
		x = 0;
		y = 0;
		counter = 0;
	}
	public Coordinate(int x, int y) {
		this.x = x;
		this.y = y;
	}
	public Coordinate(int x, int y, int c) {
		this.x = x;
		this.y = y;
		this.counter = c;
	}
	public int getX() {
		return x;
	}
	public void setX(int x) {
		this.x = x;
	}
	public int getY() {
		return y;
	}
	public void setY(int y) {
		this.y = y;
	}
	public int getCounter() {
		return counter;
	}
	public void incCounter() {
		this.counter++;
	}
	@Override
	public String toString() {
		return "Coordinate (" + x + ", " + y + "), counter = " + counter;
	}
}

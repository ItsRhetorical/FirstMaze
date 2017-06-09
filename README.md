# FirstMaze
Simple maze solving program to learn python/git

Run maze MazeSolver.py to get started

Note currently path will enter on top and exit on bottom
brute forcing whitespace works, but takes forever to animate I recommend keeping all paths to 1 wide until optimized
cannot travel diagonally

This was an attempt at reteaching myself OO programming and python
many enhancements could be done
- Cleaning up the class structure/referencing/duplication data
- Implementing other path finding algorithms: shortest, A*, Dijkstra's, etc,
- Handling whitespace better by grouping adjacent nodes
-- paths with only 2 exits pulled into single node
-- "blobs" aggregated into a single node
- animating in loop instead of storing and then outputting animation path
- Using a better IO / maybe interfacing with js/html for a web page version

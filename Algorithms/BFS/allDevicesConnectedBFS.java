// Tuguldur Gantumur (22677666) , Jasmine Ngiam Yi Chen (22739879)

import java.util.*;

/**
 *
 * For each of the below functions, a specification of the structure of the network is passed as an 
 * int[][] argument called adjlist. 
 * A device with id v is considered adjacent to a device with id u if they are physically linked 
 * such that u is able to transmit a packet directly to v. 
 * The array adjlist[u] is a list of all the device ids that are adjacent to u. 
 * For example, if adjlist[1] is the array {0, 2}, this means that device 1 is able to transmit packets 
 * to devices 0 and 2.
 * 
 */


public class MyProject implements Project 
{

    public MyProject(){}

    /** Determine if all of the devices in the network are connected to the network. 
     * Devices are considered to be connected to the network if they can transmit 
     * (including via other devices) to every other device in the network. 
     * If all devices in the network are connected, then return true , and return false otherwise.
     * 
     * @param  adjlist = the structure of the network
     * 
     * @return true if all devices in the network are connected.
     * @return false otherwise.
    */
    public boolean allDevicesConnected(int[][] adjlist) 
    {

        //if there is no device in the network structure
        if(adjlist.length == 0)
        {
            return false;
        }

        //array to store number of each device
        int[]keys = new int[adjlist.length];
        //array to indicate whether each vertice has been visited
        boolean [] visited = new boolean[adjlist.length];

        //initialize array to false
        Arrays.fill(visited, Boolean.FALSE);

        // A queue to store the device to be searched for its connected devices.
        Queue<Integer> q = new LinkedList<Integer>();

        //store every device id in the network
        for (int row = 0; row < adjlist.length; row++)
        {
            keys[row] = row;
        }

        int start = 0;
        
        //offer the first device in the network to our queue
        q.offer(start);
        while(!q.isEmpty())
        {
            //remove and retrieve the head of the queue
            int vert = q.poll();

            if(visited[vert] != false)
            {
                continue;
            }

            //traverse through the 2d array adjlist
            for(int row = 0; row < adjlist.length; row++)
            {
                for(int col = 0; col < adjlist[row].length; col++)
                {
                    if(keys[vert] == adjlist[row][col])
                    {
                        q.offer(row);
                    }
                }
            }
        visited[vert] = true;
        }

        for(boolean b : visited)
        {
            if(!b)
            {
                return false; //one unreachable or trivial disconnected
            }
        }
        return true;
    }


    /**Determine the number of different paths a packet can take in the network to get from a
     * transmitting device to a receiving device. 
     * A device will only transmit a packet to a device that is closer to the destination, 
     * 
     * where the distance to the destination is the minimum number of hops between a device 
     * and the destination.
     * 
     * @param adjlist = structure of a network
     * @param src = device id of the transmitting device
     * @param dst = the device id of the receiving device
     * 
     * @return int numpaths, the number of possible paths in the network 
     * that a packet may take from source (src) to destination (dst)
     * @return 1, if the source (src) is the same as the destination (dst)
     */
    public int numPaths(int[][] adjlist, int src, int dst) 
    {

        //if the src is the same as the dst, 
        //the number of possible paths is 1
        if (src == dst)  return 1;

        //initialize the number of paths from src to dst to 0.
        int numpaths = 0;

        //An array to indicate whether the vertice has been visited
        //initialize the array to false.
        boolean[] visited = new boolean[adjlist.length];
        Arrays.fill(visited, Boolean.FALSE);

        // A queue to store the device to be searched for its connected devices.
        Queue<Integer> queue = new LinkedList<Integer>();

        //offer the starting device to the array
        queue.offer(src);
        //indicate the device as visited.
        visited[src] = true;
        while (!queue.isEmpty()) 
        {
            int seen = queue.poll();
            for (int j = 0; j < adjlist[seen].length;j++) 
            {
                // If the next connected device is the receiving device, it is a path.
                if (adjlist[seen][j] == dst) 
                {
                    numpaths++;
                }

                if (!visited[adjlist[seen][j]]) 
                {
                    visited[adjlist[seen][j]] = true;
                    queue.offer(adjlist[seen][j]);
                }
            }
        }
        return numpaths;
    }


    /**A private method that determines if the current address does contain the specified query
     * 
     * @param addrs 
     * @param queries
     * 
     * @return true if the specified IP addrs does contain a subnet
     * @return false, otherwise
     */
    private boolean isSubnet(short[] addrs, short[] queries) 
    {
        return Arrays.equals(addrs, 0, queries.length, queries, 0, queries.length);
    }


    /**Compute the minimum number of hops required to reach a device in each subnet query. 
     * Each device has an associated IP address.
     * Each query specifies a subnet address
     * An IP address is considered to be in a subnet if the subnet address is a prefix of the IP address 
     * for example, {192, 168, 1, 1} is in subnet {192, 168} but not in {192, 168, 2} 
     * 
     * @param adjlist = the structure of the network
     * @param addrs =  a short [][] array of IP addresses (device id i has address addrs[i])
     * @param src = the device id of the transmitting device
     * @param queries = a short [][] array of queries where each query is a subnet prefix
     * 
     * @return Integer.MAX_VALUE, if no device in that subnet is reachable (hoops[i] = Integer.MAX_VALUE) 
     * @return int [] containing the number of hops required to reach each subnet from src.
     */
    public int[] closestInSubnet(int[][] adjlist, short[][] addrs, int src, short[][] queries) 
    {
        
        int[] hoops = new int[queries.length];
        int[] choops = bfshoops(adjlist, src);
        boolean subnetPrefixFound = false;

        for (int i = 0; i < queries.length; i++) 
        {
            //There are no subnet queries
            if (queries[i].length < 1) 
            {
                hoops[i] = 0;
            }
            else
            {
                for (int j = 0; j < addrs.length; j++) 
                {
                    if (!subnetPrefixFound) 
                    {
                        //if the addrs contains the subnet prefix
                        if (isSubnet(addrs[j], queries[i])) 
                        {
                            hoops[i] = choops[j];
                            subnetPrefixFound = true;
                        }
                        //no device in that subnet is reachable
                        if ((j == addrs.length-1) && (!isSubnet(addrs[j], queries[i]))) 
                        {
                            hoops[i] = Integer.MAX_VALUE;
                        }
                    }
                }
            }
            subnetPrefixFound = false;
        } 
        return hoops;
    }


    /**A private method which conducts a Breadth First Search (BFS) for the closestInSubnet() method.
     * 
     * 
     * @param adjlist =  the structure of the network
     * @param src =  the device id of the transmitting device
     * 
     * @return int [] array containing the number of hops required from @param src
     */
    private int[] bfshoops(int[][] adjlist, int src) 
    {
        //Create an array indicating the number of hops required from src
        int[] hoops = new int[adjlist.length];
        Arrays.fill(hoops, Integer.MAX_VALUE);

        //An array to indicate if an IP address has been visited
        boolean[] visited = new boolean[adjlist.length];
        Arrays.fill(visited, Boolean.FALSE);

        //A queue to store subnet prefix to be searched for in addrs
        Queue<Integer> q = new LinkedList<Integer>();

        q.offer(src);
        visited[src] = true;
        hoops[src] = 0;

        while (!q.isEmpty()) {
            int current = q.poll();
            for (int i = 0; i < adjlist[current].length; i++) {
                if (!visited[adjlist[current][i]]) {
                    hoops[adjlist[current][i]] = hoops[current] + 1;
                    visited[adjlist[current][i]] = true;
                    q.offer(adjlist[current][i]);
                }
            }
        }
        return hoops;
    }


    /**A private method which implements a Breadth First Search (BFS) required for the
     * public method maxDownloadSpeed()
     * 
     * @param adjlist = the structure of the network
     * @param residual = the residual list containing the maximum speeds
     * @param start = the device id of the transmitting device
     * @param dest = the device id of the receiving device
     * @param parent = an int[] array which contains the parent device id of each device
     * 
     * @return true if the BFS successfully reached the desination (dst)
     * @return false, if the destination is not reachable from the transmitting device @param src
     */
    private boolean bfs(int[][] adjlist, int[][] residual, int start, int dest, int[] parent) {
        boolean[] visited = new boolean[adjlist.length];
        Arrays.fill(visited, Boolean.FALSE);
        
        //Create a queue, enqueue source vertex and mark it as visited
        LinkedList<Integer> queue = new LinkedList<Integer>();
        queue.add(start);
        visited[start] = true;
        parent[start] = -1;

        //Standard BFS
        while(!queue.isEmpty()) {
            int u = queue.poll();
            for(int v = 0; v < adjlist[u].length; v++) {
                if(visited[adjlist[u][v]] == false && residual[u][adjlist[u][v]] > 0) {
                // IF we find a connection to the destination node
                // then there is no point in BFS anymore
                // we just have to set its parent and return true
                    if(adjlist[u][v] == dest) {
                        parent[adjlist[u][v]] = u;
                        return true;
                    }
                    //destination not reached from start node
                    queue.add(adjlist[u][v]);
                    parent[adjlist[u][v]] = u;
                    visited[adjlist[u][v]] = true;
                }
            }
        }
        return false;
    }


    /**Compute the maximum possible download speed from a transmitting device to a receiving 
     * device. 
     * The download may travel through more than one path simultaneously, 
     * and you canassume that there is no other traffic in the network.
     * 
     * Uses Edmond Karps' max flow algorithm
     * 
     * @param adjlist = the structure of a network
     * @param speeds = The maximum speed of each link in the network
     * @param src = the device id of the transmitting device
     * @param dst = the device id of the receiving device 
     * 
     * @return -1 if the transmitting and receiving devices are the same
     */
    public int maxDownloadSpeed(int[][] adjlist, int[][] speeds, int src, int dst) 
    {
        //initialize the max speed to 0.
        int max = 0;
        int u = 0;
        //the transmitting and receiving devices are the same.
        if (src == dst) return -1;
        
        //Create a residual 2d array which indicates the capacity of edges.
        int[][] residual = new int[adjlist.length][adjlist.length];

        for (int i = 0; i < adjlist.length; i++) 
        {
            for (int j = 0; j < adjlist[i].length; j++) 
            {
                int dest = adjlist[i][j];
                residual[i][dest] = speeds[i][j];
            }
        }

        //Array to be filled by the BFS and to store paths
        int[] parent = new int[adjlist.length];

        //Augment the flow while there is a path from src -> dst
        while (bfs(adjlist, residual, src, dst, parent)) 
        {
            //Find the minimum flow through the path found
            int pathflow = Integer.MAX_VALUE;
            for (int i = dst; i != src; i = parent[i]) 
            {
                u = parent[i];
                pathflow = Math.min(pathflow, residual[u][i]);
            }

            //update the residual capacities of the edges and reverse edges along the way.
            for (int i = dst; i != src; i = parent[i]) {
                u = parent[i];
                residual[u][i] -= pathflow;
                residual[i][u] += pathflow;
            }
            //add the speed from the path to the max speed.
            max += pathflow;
        }
        //return the overall max speed
        return max;
    }
    
}

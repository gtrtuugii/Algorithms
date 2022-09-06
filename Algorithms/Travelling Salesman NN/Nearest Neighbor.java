import java.util.*;

/**
     * Returns the shortest tour found by exercising the NN algorithm 
     * from each possible starting city in table.
     * table[i][j] == table[j][i] gives the cost of travel between City i and City j.
     */
    public static int[] tspnn(double[][] table)
    {
        // COMPLETE THIS METHOD
        
        // num of cities 
        int num = table[0].length;
        
        // init optimal path distance
        double opt_path = -1.0;
        
        // init optimal path
        int [] result = new int[num];
        
        // Nearest Neighbor Algo
        // loop for every vertex
        for(int i = 0; i < num; i++)
        {
            int[] test_res = new int[num];
            
            // to indicate whether we visited the city
            boolean[] visited = new boolean[num];
            
            // set array to false
            Arrays.fill(visited, false);
            
            // set 1st city to true
            visited[0] = true;
            
            // weight of each edge visited
            double weight = 0;
            // pointer to current position
            int ptr = i;
            // will use this var to traverse the tables array
            int count = 1; 
            
            
            // loop to visit every city
            while(count < num)
            {
                int index = -1;
                double tempdist = -1.0;
                double dist[] = table[ptr];
                
                for(int j = 0; j < num; j++)
                {
                    // check if not visited yet
                    if(visited[j] == false)
                    {

                        double currdist = dist[j];
                        
                        // check if its the first node
                        // or if the current node has  less distance
                        if(index < 0 && tempdist < 0  || currdist < tempdist)
                        {
                            tempdist = currdist;
                            index = j;
                        }
                    }
                }
                // Move the counter to next val
                // add the last weight 
                // mark the current node as visited
                weight = weight + tempdist;
                test_res[count] = index;
                ptr = index;
                visited[index] = true;
                
                
                count++;
                
 
            }
            
            // Compare distances
            if(opt_path < 0  || weight > opt_path)
            {
                result = test_res;
                opt_path = weight;
            }
        }
        return result;
        
    }
    /*
    * Uses 2-OPT repeatedly to improve cs, choosing the shortest option in each iteration.
    * You can assume that cs is a valid tour initially.
    * table[i][j] == table[j][i] gives the cost of travel between City i and City j.
    */
 

    public static int[] tsp2opt(int[] cs, double[][] table)
    {
        // COMPLETE THIS METHOD
        
        // array to modify
        int[] temp_res = cs;
        double[][] temp_table = table;
        
        
        int n = cs.length;
        int dist = distCalc(temp_res, temp_table);
        boolean foundImprovement = true;
        
        while(foundImprovement)
        {
            for(int i = 0; i < n - 2; i++)
            {
                for(int j = i + 1; j <= n - 1; j++)
                {
                    int[] temp_tour = tsp2optswap(temp_res,i,j);
                    int temp_dist = distCalc(temp_tour, temp_table);
                    
                    if(temp_dist < dist)
                    {
                        dist = temp_dist;
                        temp_res = temp_tour;
                        foundImprovement = false;
                        
                    }
                    if(j == n - 1)
                    {
                        foundImprovement = false;
                    }
                }
                if(i == n - 2)
                {
                    foundImprovement = false;
                }
            }
            
            
        }
        return temp_res;
        
        

        
    }
    
    public static int[] tsp2optswap(int[] tour, int i, int k)
    {
        int [] result = new int[tour.length];
        // 1. take route[0] to route[v1] and add them in order to new_route
        for(int a = 0; a <= i - 1; a++)
        {
            result[a] = tour[a];
        }
        // 2. take route[v1+1] to route[v2] and add them in reverse order to new_route
        for(int a = i; a <= k; a++)
        {
            for(int b = k; b >= k; b--)
            {
                result[a] = tour[b];
            }
        }
        // 3. take route[v2+1] to route[end] and add them in order to new_route
        for(int a = k + 1; a < tour.length; a++)
        {
            result[a] = tour[a];
        }
        return result;
    }
    
    public static int distCalc(int[] tour, double[][] dists)
    {
        
        int sumdist = 0;
        
        for(int i = 0; i < tour.length - 2; i++)
        {
            for(int j = i + 1; j < tour.length - 1; j++)
            {
                sumdist += dists[i][j];
            }
        }
        // end to beginning
        sumdist += dists[0][tour.length - 1];
        
        return sumdist;
        
    }

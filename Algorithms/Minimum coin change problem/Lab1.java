/**
 * Apply the greedy algorithm to calculate coin change.
 * @param amount a non-negative integer which is required to be made up.
 * @param denominations the available coin types (unique positive integers)
 * @return a map of each denomination to the number of times it is used in the solution.
 * **/

public static Map<Integer,Integer> greedyChange(int amount, int[] denominations)
{
         //fill in code here
         // stragety is to use the bigger coins first
         Map<Integer, Integer> result = new HashMap<Integer, Integer>();
         int size = denominations.length;
         int count = 0;
         
         // sort the array in ascending order
         Arrays.sort(denominations);
         
         // traverse the array
         for(int i = size - 1; i >= 0; i--)
         {
            if(amount >= denominations[i])
            {
                while(amount >= denominations[i])
                {
                    amount -= denominations[i];
                    count++;
                    result.put(denominations[i], count);
                }
                // have to reset counter
                count = 0;
                
            }
            // if the coins weren't used
            else{
                result.put(denominations[i], 0);
            }

         }
         return result;
}
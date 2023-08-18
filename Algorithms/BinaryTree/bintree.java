import CITS2200.BinaryTree;
import CITS2200.Iterator;
import CITS2200.OutOfBounds;
import java.util.LinkedList;

/**
 * LAB5  - Bintree
 * @author Tuguldur Gantumur 
 * sid: 22677666
 * https://teaching.csse.uwa.edu.au/units/CITS2200/Labs/labsheet05.html
 * */
 
 
public class BinTree<E> extends BinaryTree<E> {

  public BinTree() 
  {
    super();
  }

  public BinTree(E item, BinaryTree<E> ltree, BinaryTree<E> rtree) 
  {
    super(item, ltree, rtree);
  }
  
	
  /**
  * @return true if both binary trees have exactly the same structure,
  * false otherwise
  * @Override the equals() in Objects
  **/
  @Override
  public boolean equals(Object object) 
  {
	//not a BinaryTree or child of binary tree.
    if(!(object instanceof CITS2200.BinaryTree) || object == null)
            return false; 
    //Check if both trees are empty
    if(this.isEmpty() && ((BinaryTree)object).isEmpty()) 
            return true;
    if(this.isEmpty() | ((BinaryTree)object).isEmpty())
            return false;
    if(this.getItem().equals( ((BinaryTree)object).getItem() )) 
            return this.getLeft().equals(((BinaryTree)object).getLeft()) && this.getRight().equals(((BinaryTree)object).getRight());
    return false;
    }

 /**
 * @return an instance of CITS2200.Iterator 
 * that returns every element 
 * stored in the tree exactly once
 * 
 **/
  public Iterator<E> iterator() 
  {
    // TODO: Implement iterator
    // NOTE: You may need to create an inner class to implement the iterator
    return new QueueIterator<E>(this);
  }
  
 /**
 * Subclass for iterator 
 * @SuppressWarnings to run
 **/
 @SuppressWarnings("unchecked")
 private class QueueIterator<E> implements CITS2200.Iterator<E>
    {
        private LinkedList<BinaryTree<E>> l = new LinkedList<BinaryTree<E>>();
        private int index = 0; //pointer

        /**
         * Constructor for the iterator, add items to the queue,
         * traverse
         * uses offer() to append items to queue
        **/
        
        public QueueIterator(BinTree<E> b)
        {
            if(!b.isEmpty()) l.offer(b); //if empty add root 'b'
            while(index < l.size()){ //while index doesnt reach end of linkedlist
                if(!l.get(index).getLeft().isEmpty())
                {
                    l.offer(l.get(index).getLeft()); //add to LinkedList
                }
                if(!l.get(index).getRight().isEmpty())
                {
                    l.offer(l.get(index).getRight());
                }
                index ++;
            }
            index = 0;
        }

        /**
         * Check if there is a next item to return
         * @return true if there is another element and 
         * false otherwise
         * 
        **/
        public boolean hasNext()
        {
            return index < l.size();
        }

        /**
         * Moves the iterator to the next element
         * @return the next element
         * @throws OutOfBounds if there is no next element
        **/
        
        public E next()
        {
            if(hasNext())
            {
                return  l.get(index++).getItem();
            }
            else throw new OutOfBounds("no more items");
        }
            
    }
}

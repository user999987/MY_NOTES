Generic types in Java are invariant, meaning that `List<String>` is not subtype of `List<Object>`. If List were not invariant, it would have been no better than Java's arrays:
```java
List<String> strs = new ArrayList<String>();
List<Object> objs = strs; // !!! A compile-time error here saves us from a runtime exception later.
objs.add(1); // Put an Integer into a list of Strings
String s = strs.get(0); // !!! ClassCastException: Cannot cast Integer to String
```
Java prohibits such things in order to guarantee run-time safety, but it brings other implications. 
For example, consider the addAll() method from the Collection interface. What's the signature of this method? Intuitively, you'd write it this way:
```java
interface Collection<E>...{
    void addAll(Collection<E> items);
}

void copyAll(Collection<Object> to, Collection<String> from){
    to.addAll(from)
    // !!! Would not compile with the naive declaration of addAll:
    // Collection<String> is not a subtype of Collection<Object>
}
```
So the actual signature of addAll() is the following:
```java
interface Collection<E> ... {
    void addAll(Collection<? extends E> items);
}
```
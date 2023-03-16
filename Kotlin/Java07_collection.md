## Collection
Java标准库自带的java.util包提供了集合类：Collection，它是除Map外所有其他集合类的根接口.Java的java.util包主要提供了以下三种类型的集合：

* List：一种有序列表的集合，例如，按索引排列的Student的List；
* Set：一种保证没有重复元素的集合，例如，所有无重复名称的Student的Set；
* Map：一种通过键值（key-value）查找的映射表集合，例如，根据Student的name查找对应Student的Map。

Java集合的设计有几个特点：
1. 一是实现了接口和实现类相分离，例如，有序表的接口是List，具体的实现类有`ArrayList`，`LinkedList`等
2. 二是支持泛型

我们考察List<E>接口，可以看到几个主要的接口方法：

1. 在末尾添加一个元素：boolean add(E e)
2. 在指定索引添加一个元素：boolean add(int index, E e)
3. 删除指定索引的元素：E remove(int index)
4. 删除某个元素：boolean remove(Object e)
5. 获取指定索引的元素：E get(int index)
6. 获取链表大小（包含元素的个数）：int size()

## iterating collection
```java
import java.util.Iterator;
import java.util.List;
public class Main {
    public static void main(String[] args) {
        List<String> list = List.of("apple", "pear", "banana");
        // 正规写法
        for (Iterator<String> it = list.iterator(); it.hasNext(); ) {
            String s = it.next();
            System.out.println(s);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        List<String> list = List.of("apple", "pear", "banana");
        // java for each写法
        for (String s : list) {
            System.out.println(s);
        }
    }
}
```

## convert bewteen array and list
Array -> List
```java
//1 给toArray(T[])传入一个类型相同的Array，List内部自动把元素复制到传入的Array中：
List<Integer> list = List.of(12, 34, 56);
Integer[] array = list.toArray(new Integer[3]);
//2 通过List接口定义的T[] toArray(IntFunction<T[]> generator)方法：
Integer[] array = list.toArray(Integer[]::new);
```

List -> Array
```java
// List.of(T...)
Integer[] array = { 1, 2, 3 };
List<Integer> list = List.of(array);
```

## equals()
```java
public boolean equals(Object o) {
    if (o instanceof Person) {
        Person p = (Person) o;
        return Objects.equals(this.name, p.name) && this.age == p.age;
    }
    return false;
}
```

## Map
```java
import java.util.HashMap;
import java.util.Map;
public class Main {
    public static void main(String[] args) {
        Student s = new Student("Xiao Ming", 99);
        Map<String, Student> map = new HashMap<>();
        map.put("Xiao Ming", s); // 将"Xiao Ming"和Student实例映射并关联
        Student target = map.get("Xiao Ming"); // 通过key查找并返回映射的Student实例
        System.out.println(target == s); // true，同一个实例
        System.out.println(target.score); // 99
        Student another = map.get("Bob"); // 通过另一个key查找
        System.out.println(another); // 未找到返回null
    }
}

class Student {
    public String name;
    public int score;
    public Student(String name, int score) {
        this.name = name;
        this.score = score;
    }
}
```

## iterate map
```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        map.put("apple", 123);
        map.put("pear", 456);
        map.put("banana", 789);
        // for (Integer value : map.values())
        // for (String key: map.keySet())
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            String key = entry.getKey();
            Integer value = entry.getValue();
            System.out.println(key + " = " + value);
        }
    }
}
```


## Treemap
SortedMap在遍历时严格按照Key的顺序遍历，最常用的实现类是TreeMap；

作为SortedMap的Key必须实现Comparable接口，或者传入Comparator；

要严格按照compare()规范实现比较逻辑，否则，TreeMap将不能正常工作。

## properties
Java默认配置文件以.properties为扩展名，每行以key=value表示，以#课开头的是注释

# read properties
```java
# setting.properties

last_open_file=/data/hello.txt
auto_save_interval=60

//可以从文件系统读取这个.properties文件：

String f = "setting.properties";
Properties props = new Properties();
props.load(new java.io.FileInputStream(f));

String filepath = props.getProperty("last_open_file");
String interval = props.getProperty("auto_save_interval", "120");
```
可见，用Properties读取配置文件，一共有三步：

1. 创建Properties实例；
2. 调用load()读取文件；
3. 调用getProperty()获取配置。

调用getProperty()获取配置时，如果key不存在，将返回null。我们还可以提供一个默认值，这样，当key不存在的时候，就返回默认值。

# write properties
如果通过setProperty()修改了Properties实例，可以把配置写入文件，以便下次启动时获得最新配置。写入配置文件使用store()方法：
```java
Properties props = new Properties();
props.setProperty("url", "http://www.liaoxuefeng.com");
props.setProperty("language", "Java");
props.store(new FileOutputStream("C:\\conf\\setting.properties"), "这是写入的properties注释");
```
## 反射
Reflection in Java is an API(Application Programming Interface) that is used at runtime to analyze or change classes, methods, and interfaces. It is a process of examining or modifying the run time behavior of a class at run time<br>
Java的反射是指程序在运行期可以拿到一个对象的所有信息

## Class 类
class是由JVM在执行过程中动态加载的。JVM在第一次读取到一种class类型时，将其加载进内存。每加载一种class，JVM就为其创建一个Class类型的实例，并关联起来。注意：这里的Class类型是一个名叫Class的class。它长这样：
```java
public final class Class {
    private Class() {}
}
```
以String类为例，当JVM加载String类时，它首先读取String.class文件到内存，然后，为String类创建一个Class实例并关联起来：
```java
Class cls = new Class(String);
```
这个Class实例是JVM内部创建的，如果我们查看JDK源码，可以发现Class类的构造方法是private，只有JVM能创建Class实例，我们自己的Java程序是无法创建Class实例的。

所以，JVM持有的每个Class实例都指向一个数据类型（class或interface）
```
┌───────────────────────────┐
│      Class Instance       │──────> String
├───────────────────────────┤
│name = "java.lang.String"  │
└───────────────────────────┘
┌───────────────────────────┐
│      Class Instance       │──────> Random
├───────────────────────────┤
│name = "java.util.Random"  │
└───────────────────────────┘
┌───────────────────────────┐
│      Class Instance       │──────> Runnable
├───────────────────────────┤
│name = "java.lang.Runnable"│
└───────────────────────────┘
```
一个Class实例包含了该class的所有完整信息：
```
┌───────────────────────────┐
│      Class Instance       │──────> String
├───────────────────────────┤
│name = "java.lang.String"  │
├───────────────────────────┤
│package = "java.lang"      │
├───────────────────────────┤
│super = "java.lang.Object" │
├───────────────────────────┤
│interface = CharSequence...│
├───────────────────────────┤
│field = value[],hash,...   │
├───────────────────────────┤
│method = indexOf()...      │
└───────────────────────────┘
```
由于JVM为每个加载的class创建了对应的Class实例，并在实例中保存了该class的所有信息，包括类名、包名、父类、实现的接口、所有方法、字段等，因此，如果获取了某个Class实例，我们就可以通过这个Class实例获取到该实例对应的class的所有信息。

这种通过Class实例获取class信息的方法称为反射（Reflection）

## 获取一个 class 的 Class 实例
1. 直接通过 class 的静态变量 class
```java
Class cls = String.class
```
2. 通过实例变量提供的 getClass 方法
```java
String s = "Hello"
Class cls = s.getClass()
```
3. 通过静态方法 Class.forName 配合 class 完整类名
```java
Class cls = Class.forName("java.lang.String")
```

因为Class实例在JVM中是唯一的，所以，上述方法获取的Class实例是同一个实例。可以用==比较两个Class实例：
```java
Class cls1 = String.class;

String s = "Hello";
Class cls2 = s.getClass();

boolean sameClass = cls1 == cls2; // true
```

## 动态加载
JVM在执行Java程序的时候，并不是一次性把所有用到的class全部加载到内存，而是第一次需要用到class时才加载

通过Class实例获取class信息的方法称为反射（Reflection）；

JVM总是动态加载class，可以在运行期根据条件来控制加载class。
```java
// Commons Logging优先使用Log4j:
LogFactory factory = null;
if (isClassPresent("org.apache.logging.log4j.Logger")) {
    factory = createLog4j();
} else {
    factory = createJdkLog();
}

boolean isClassPresent(String name) {
    try {
        Class.forName(name);
        return true;
    } catch (Exception e) {
        return false;
    }
}
```

## 字段 field
Class类提供了以下几个方法来获取字段：

* Field getField(name)：根据字段名获取某个public的field（包括父类）
* Field getDeclaredField(name)：根据字段名获取当前类的某个field（不包括父类）
* Field[] getFields()：获取所有public的field（包括父类）
* Field[] getDeclaredFields()：获取当前类的所有field（不包括父类
```java
public class Main {
    public static void main(String[] args) throws Exception {
        Class stdClass = Student.class;
        // 获取public字段"score":
        System.out.println(stdClass.getField("score"));
        // 获取继承的public字段"name":
        System.out.println(stdClass.getField("name"));
        // 获取private字段"grade":
        System.out.println(stdClass.getDeclaredField("grade"));
    }
}

class Student extends Person {
    public int score;
    private int grade;
}

class Person {
    public String name;
}
//public int Student.score
//public java.lang.String Person.name
//private int Student.grade
```

## Filed 对象
getName()：返回字段名称，例如，"name"；
getType()：返回字段类型，也是一个Class实例，例如，String.class；
getModifiers()：返回字段的修饰符，它是一个int，不同的bit表示不同的含义。
```java
public class Main {

    public static void main(String[] args) throws Exception {
        Object p = new Person("Xiao Ming");
        Class c = p.getClass();
        Field f = c.getDeclaredField("name");
        // get field value
        Object value = f.get(p);
        //f.set(p, "Xiao Hong");
        System.out.println(value); // "Xiao Ming"
    }
}

class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }
}
```
运行代码，如果不出意外，会得到一个IllegalAccessException，这是因为name被定义为一个private字段，正常情况下，Main类无法访问Person类的private字段。要修复错误，可以将private改为public，或者，在调用Object value = f.get(p);前，先写一句：
```java
//修改非public字段，需要首先调用setAccessible(true)
f.setAccessible(true);
```
此外，setAccessible(true)可能会失败。如果JVM运行期存在SecurityManager，那么它会根据规则进行检查，有可能阻止setAccessible(true)。例如，某个SecurityManager可能不允许对java和javax开头的package的类调用setAccessible(true)，这样可以保证JVM核心库的安全

## Method 对象
```java
public class Main {
    public static void main(String[] args) throws Exception {
        // String对象:
        String s = "Hello world";
        // 获取String substring(int)方法，参数为int:
        Method m = String.class.getMethod("substring", int.class);
        // 在s对象上调用该方法并获取结果:
        // invoke的第一个参数是对象实例，即在哪个实例上调用该方法，后面的可变参数要与方法参数一致
        String r = (String) m.invoke(s, 6);
        // 调用该静态方法并获取结果:
        // Integer n = (Integer) m.invoke(null, "12345");
        // 打印调用结果:
        System.out.println(r);
    }
}
```
和 Field 对象 相似, 通过设置setAccessible(true)来访问非public方法。<br>
一个Person类定义了hello()方法，并且它的子类Student也覆写了hello()方法，那么，从Person.class获取的Method，作用于Student实例时,调用的还是实际类型覆写的方法

## constructor对象
```java
Person p = new Person();

Person p = Person.class.newInstance();
```
调用Class.newInstance()的局限是，它只能调用该类的public无参数构造方法。如果构造方法带有参数，或者不是public，就无法直接通过Class.newInstance()来调用。

为了调用任意的构造方法，Java的反射API提供了Constructor对象，它包含一个构造方法的所有信息，可以创建一个实例。Constructor对象和Method非常类似，不同之处仅在于它是一个构造方法，并且，调用结果总是返回实例：

```java
public class Main {
    public static void main(String[] args) throws Exception {
        // 获取构造方法Integer(int):
        Constructor cons1 = Integer.class.getConstructor(int.class);
        // 调用构造方法:
        Integer n1 = (Integer) cons1.newInstance(123);
        System.out.println(n1);

        // 获取构造方法Integer(String)
        Constructor cons2 = Integer.class.getConstructor(String.class);
        Integer n2 = (Integer) cons2.newInstance("456");
        System.out.println(n2);
    }
}
```
通过Class实例的方法可以获取Constructor实例：
* getConstructor(Class...)：获取某个public的Constructor；
* getDeclaredConstructor(Class...)：获取某个Constructor；
* getConstructors()：获取所有public的Constructor；
* getDeclaredConstructors()：获取所有Constructor。

## 获取继承关系
```java
public class Main {
    public static void main(String[] args) throws Exception {
        Class i = Integer.class;
        Class n = i.getSuperclass();
        System.out.println(n);
        Class o = n.getSuperclass();
        System.out.println(o);
        System.out.println(o.getSuperclass());
    }
}
//class java.lang.Number
//class java.lang.Object
//null
```

## 获取 interface
```java
public class Main {
    public static void main(String[] args) throws Exception {
        Class s = Integer.class;
        Class[] is = s.getInterfaces();
        for (Class i : is) {
            System.out.println(i);
        }
    }
}
//interface java.lang.Comparable
//interface java.lang.constant.Constable
//interface java.lang.constant.ConstantDesc

System.out.println(java.io.Closeable.class.getSuperclass()); 
// null，对接口调用getSuperclass()总是返回null，获取接口的父接口要用getInterfaces()
```
当我们判断一个实例是否是某个类型时，正常情况下，使用instanceof<br>
如果是两个Class实例，要判断一个向上转型是否成立，可以调用isAssignableFrom()
```java
// Integer i = ?
Integer.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Integer
// Number n = ?
Number.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Number
// Object o = ?
Object.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Object
// Integer i = ?
Integer.class.isAssignableFrom(Number.class); // false，因为Number不能赋值给Integer
```
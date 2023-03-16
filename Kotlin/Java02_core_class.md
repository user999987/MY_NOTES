## String
Java字符串的一个重要特点就是字符串不可变。这种不可变性是通过内部的private final char[]字段，以及没有任何修改char[]的方法实现的<br>
当我们想要比较两个字符串是否相同时，要特别注意，我们实际上是想比较字符串的内容是否相同。必须使用equals()方法而不能用==。
```java
var s1="hello"
var s2="hello"
s1==s2
//true
//从表面上看，两个字符串用==和equals()比较都为true，但实际上那只是Java编译器在编译期，会自动把所有相同的字符串当作一个对象放入常量池，自然s1和s2的引用就是相同的。
```
```java
String s1 = "hello";
String s2 = "HELLO".toLowerCase();
System.out.println(s1 == s2);
System.out.println(s1.equals(s2));
// false
// true
```
format output
```java
String s = "Hi %s, your score is %d!";
System.out.println(s.formatted("Alice", 80));
System.out.println(String.format("Hi %s, your score is %.2f!", "Bob", 59.5));
```

# utf-8 <-> string
```java
byte[] b = "Hello".getBytes("UTF-8"); 

String s = new String(b, StandardCharsets.UTF_8)
```

## StringBuilder
```java
String s = "";
for (int i = 0; i < 1000; i++) {
    s = s + "," + i;
}
```
虽然可以直接拼接字符串，但是，在循环中，每次循环都会创建新的字符串对象，然后扔掉旧的字符串。这样，绝大部分字符串都是临时对象，不但浪费内存，还会影响GC效率

为了能高效拼接字符串，Java标准库提供了StringBuilder，它是一个可变对象，可以预分配缓冲区，这样，往StringBuilder中新增字符时，不会创建新的临时对象：

```java
StringBuilder sb = new StringBuilder(1024);
for (int i = 0; i < 1000; i++) {
    sb.append(',');
    sb.append(i);
}
String s = sb.toString();

sb.append("Mr ")
          .append("Bob")
          .append("!");
//链式操作可以实现的原因是定义的append()方法会返回this，这样，就可以不断调用自身的其他方法
```
一般情况下的 a+b+c+d jvm会自动优化为 StringBuilder 进行操作

## StringJoiner
```java
String[] names = {"Bob", "Alice", "Grace"};
var s = String.join(", ", names); //String.join()在内部使用了StringJoiner来拼接字符串
//如果需要指定开头和结尾
var sj = new StringJoiner(", ", "Hello ", "!");
for (String name : names) {
    sj.add(name);
}
System.out.println(sj.toString());
```

## Wrapper Class
```
基本类型	对应的引用类型
boolean	java.lang.Boolean
byte	java.lang.Byte
short	java.lang.Short
int	java.lang.Integer
long	java.lang.Long
float	java.lang.Float
double	java.lang.Double
char	java.lang.Character
```


## JavaBean
```java
public class Person {
    private String name;
    private int age;

    public String getName() { return this.name; }
    public void setName(String name) { this.name = name; }

    public int getAge() { return this.age; }
    public void setAge(int age) { this.age = age; }
}
```
如果读写方法符合以下这种命名规范：
```java
// 读方法:
public Type getXyz()
// 写方法:
public void setXyz(Type value)
```
那么这种class被称为JavaBean

## enum
```java

enum Weekday {
    SUN, MON, TUE, WED, THU, FRI, SAT;
}

Weekday x = Weekday.SUN; 
```
引用类型的比较永远记得使用 equals
但enum类型可以例外, 这是因为enum类型的每个常量在JVM中只有一个唯一实例，所以可以直接用==比较

enum定义的类型就是class，只不过它有以下几个特点：
* 定义的enum类型总是继承自java.lang.Enum，且无法被继承；
* 只能定义出enum的实例，而无法通过new操作符创建enum的实例；
* 定义的每个实例都是引用类型的唯一实例；

```java
public enum Color {
    RED, GREEN, BLUE;
}
//编译器编译出的class大概就像这样：
public final class Color extends Enum { // 继承自Enum，标记为final class
    // 每个实例均为全局唯一:
    public static final Color RED = new Color();
    public static final Color GREEN = new Color();
    public static final Color BLUE = new Color();
    // private构造方法，确保外部无法调用new操作符:
    private Color() {}
}
```
编译后的enum类和普通class并没有任何区别。但是我们自己无法按定义普通class那样来定义enum，必须使用enum关键字，这是Java语法规定的。

因为enum是一个class，每个枚举的值都是class实例，因此，这些实例有一些方法
```java
String s = Weekday.SUN.name(); // "SUN"
int n = Weekday.MON.ordinal(); // 1
```

## Record类
就和 Kotlin 的 Data class一样

## BigDecimal

sacle()表示小数位

```java
BigDecimal d1 = new BigDecimal("123.45");
BigDecimal d2 = new BigDecimal("123.4500");
BigDecimal d3 = new BigDecimal("1234500");
System.out.println(d1.scale()); // 2,两位小数
System.out.println(d2.scale()); // 4
System.out.println(d3.scale()); // 0
//BigDecimal的stripTrailingZeros()方法，可以将一个BigDecimal格式化为一个相等的，但去掉了末尾0的BigDecimal
```

对BigDecimal做加、减、乘时，精度不会丢失，但是做除法时，存在无法除尽的情况，这时，就必须指定精度以及如何进行截断：
```java
BigDecimal d1 = new BigDecimal("123.456");
BigDecimal d2 = new BigDecimal("23.456789");
BigDecimal d3 = d1.divide(d2, 10, RoundingMode.HALF_UP); // 保留10位小数并四舍五入
BigDecimal d4 = d1.divide(d2); // 报错：ArithmeticException，因为除不尽
//还可以对BigDecimal做除法的同时求余数
```

在比较两个BigDecimal的值是否相等时，要特别注意，使用equals()方法不但要求两个BigDecimal的值相等，还要求它们的scale()相等, 必须使用compareTo()方法来比较，它根据两个值的大小分别返回负数、正数和0，分别表示小于、大于和等于
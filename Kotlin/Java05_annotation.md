## Annotation
可以被编译器打包进入class文件，因此，注解是一种用作标注的“元数据”。从JVM的角度看，注解本身对代码逻辑没有任何影响，如何使用注解完全由工具决定。

最常用的元注解是@Target。使用@Target可以定义Annotation能够被应用于源码的哪些位置：
* 类或接口：ElementType.TYPE；
* 字段：ElementType.FIELD；
* 方法：ElementType.METHOD；
* 构造方法：ElementType.CONSTRUCTOR；
* 方法参数：ElementType.PARAMETER。

1. @interface 定义注解
```java
public @interface Report {
}
```
2. 添加参数和默认值
```java
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}
```
3. 元注解配置注解
```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}
```

@Retention定义了Annotation的生命周期：
* RetentionPolicy.SOURCE类型的注解在编译期就被丢掉了；
* RetentionPolicy.CLASS类型的注解仅保存在class文件中，它们不会被加载进JVM；
* RetentionPolicy.RUNTIME类型的注解会被加载进JVM，并且在运行期可以被程序读取。
如何使用注解完全由工具决定。SOURCE类型的注解主要由编译器使用，因此我们一般只使用，不编写。CLASS类型的注解主要由底层工具库使用，涉及到class的加载，一般我们很少用到。只有RUNTIME类型的注解不但要使用，还经常需要编写。

因为注解定义后也是一种class，所有的注解都继承自java.lang.annotation.Annotation，因此，读取注解，需要使用反射API。

Java提供的使用反射API读取Annotation的方法包括：

1. 判断某个注解是否存在于Class、Field、Method或Constructor：

* Class.isAnnotationPresent(Class)
* Field.isAnnotationPresent(Class)
* Method.isAnnotationPresent(Class)
* Constructor.isAnnotationPresent(Class)
```java
// 判断@Report是否存在于Person类:
Person.class.isAnnotationPresent(Report.class);
```
2. 使用反射API读取Annotation：

* Class.getAnnotation(Class)
* Field.getAnnotation(Class)
* Method.getAnnotation(Class)
* Constructor.getAnnotation(Class)
```java
// 获取Person定义的@Report注解:
Report report = Person.class.getAnnotation(Report.class);
int type = report.type();
String level = report.level();
```

2.1 先判断Annotation是否存在，如果存在，就直接读取

```java
    Class cls = Person.class;
if (cls.isAnnotationPresent(Report.class)) {
    Report report = cls.getAnnotation(Report.class);
    ...
}
```
2.2 直接读取Annotation，如果Annotation不存在，将返回null

```java
    Class cls = Person.class;
Report report = cls.getAnnotation(Report.class);
if (report != null) {
   ...
}
```

读取方法、字段和构造方法的Annotation和Class类似。但要读取方法参数的Annotation就比较麻烦一点，因为方法参数本身可以看成一个数组，而每个参数又可以定义多个注解，所以，一次获取方法参数的所有注解就必须用一个二维数组来表示。例如，对于以下方法定义的注解：
```java
public void hello(@NotNull @Range(max=5) String name, @NotNull String prefix) {
}
//要读取方法参数的注解，我们先用反射获取Method实例，然后读取方法参数的所有注解
// 获取Method实例:
Method m = ...
// 获取所有参数的Annotation:
Annotation[][] annos = m.getParameterAnnotations();
// 第一个参数（索引为0）的所有Annotation:
Annotation[] annosOfName = annos[0];
for (Annotation anno : annosOfName) {
    if (anno instanceof Range) { // @Range注解
        Range r = (Range) anno;
    }
    if (anno instanceof NotNull) { // @NotNull注解
        NotNull n = (NotNull) anno;
    }
}
```
## 使用 annotation
注解如何使用，完全由程序自己决定。例如，JUnit是一个测试框架，它会自动运行所有标记为@Test的方法。

我们来看一个@Range注解，我们希望用它来定义一个String字段的规则：字段长度满足@Range的参数定义：

```java
// Person.java
package com.itranswarp.learnjava;

public class Person {

	@Range(min = 1, max = 20)
	public String name;

	@Range(max = 10)
	public String city;

	@Range(min = 1, max = 100)
	public int age;

	public Person(String name, String city, int age) {
		this.name = name;
		this.city = city;
		this.age = age;
	}

	@Override
	public String toString() {
		return String.format("{Person: name=%s, city=%s, age=%d}", name, city, age);
	}
}
```

```java
//Range.java
package com.itranswarp.learnjava;

import java.lang.annotation.ElementType;
import java.lang.annotation.RetentionPolicy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface Range {

	int min() default 0;

	int max() default 255;

}
```

```java
// Main.java
package com.itranswarp.learnjava;

import java.lang.reflect.Field;

/**
 * Learn Java from https://www.liaoxuefeng.com/
 * 
 * @author liaoxuefeng
 */
public class Main {

	public static void main(String[] args) throws Exception {
		Person p1 = new Person("Bob", "Beijing", 20);
		Person p2 = new Person("", "Shanghai", 20);
		Person p3 = new Person("Alice", "Shanghai", 199);
		for (Person p : new Person[] { p1, p2, p3 }) {
			try {
				check(p);
				System.out.println("Person " + p + " checked ok.");
			} catch (IllegalArgumentException e) {
				System.out.println("Person " + p + " checked failed: " + e);
			}
		}
	}

	static void check(Person person) throws IllegalArgumentException, ReflectiveOperationException {
		for (Field field : person.getClass().getFields()) {
			Range range = field.getAnnotation(Range.class);
			if (range != null) {
				Object value = field.get(person);
				// TODO:
			}
		}
	}
}
```

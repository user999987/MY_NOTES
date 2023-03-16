## 包 package

小明的Person类存放在包ming下面，因此，完整类名是ming.Person；

小红的Person类存放在包hong下面，因此，完整类名是hong.Person；

小军的Arrays类存放在包mr.jun下面，因此，完整类名是mr.jun.Arrays；

JDK的Arrays类存放在包java.util下面，因此，完整类名是java.util.Arrays。

```java
package ming; // 申明包名ming

public class Person {
}

package mr.jun; // 申明包名mr.jun

public class Arrays {
}
```

在Java虚拟机执行的时候，JVM只看完整类名，因此，只要包名不同，类就不同。\
包可以是多层结构，用.隔开。例如：java.util。\
<span style="color:red">**要特别注意：包没有父子关系。java.util和java.util.zip是不同的包，两者没有任何继承关系。**</span> 

组织文件结构时候 要根据 包 的层次组织结构

## 包作用域

<span style="color:red">位于同一个包的类</span>，可以访问包作用域的字段和方法。不用public、protected、private修饰的字段和方法就是包作用域。\
注意，包名必须完全一致，包没有父子关系，com.apache和com.apache.abc是不同的包。
例如，Person类定义在hello包下面：

```java
package hello;

public class Person {
    // 包作用域:
    void hello() {
        System.out.println("Hello!");
    }
}
```

## import 

在一个类中 引用其他的类。例如， 小明的 ming.Person 类， 如果要引用小军的 mr.jun.Arrays 有 3 种写法

1. 不停的写类的全名

```java
// Person.java
package ming;

public class Person {
    public void run() {
        mr.jun.Arrays arrays = new mr.jun.Arrays(); // mr.jun.Arrays 写类的全名
    }
}
```

2. import 语句导入后，写简单类名

```java
import mr.jun.Arrays;
Arrays arrays = new Arrays();
```

3. import static 可以导入一个类的静态字段和静态方法。基本没啥用

```java
package main;

// 导入System类的所有静态字段和静态方法:
import static java.lang.System.*;

public class Main {
    public static void main(String[] args) {
        // 相当于调用System.out.println(…)
        out.println("Hello, world!");
    }
}
```

如果有两个class名称相同，例如，mr.jun.Arrays和java.util.Arrays，那么只能import其中一个，另一个必须写完整类名。

## 最佳实践

为了避免名字冲突，我们需要确定唯一的包名。推荐的做法是使用倒置的域名来确保唯一性。

```
oop-package
└── src
    └── com
        └── itranswarp
            ├── sample
            │   └── Main.java
            └── world
                └── Person.java
```

## classpath 

classpath 是JVM用到的一个环境变量，它用来指示JVM如何搜索class。
cp = classpath
```bash
java -cp .:/usr/shared:/usr/local/bin:/home/liaoxuefeng/bin
java -classpath .:/usr/shared:/usr/local/bin:/home/liaoxuefeng/bin
// 没有设置系统环境变量，也没有传入-cp参数，那么JVM默认的classpath为.，即当前目录
java abc.xyz.Hello
```

## jar包

假设编译输出的目录结构是这样
```
package_sample
└─ bin
   ├─ hong
   │  └─ Person.class
   │  ming
   │  └─ Person.class
   └─ mr
      └─ jun
         └─ Arrays.class
```

jar包里的第一层目录，不能是bin，而应该是hong、ming、mr，框起来然后压缩成 zip 把后缀改成 jar 就是 jar 包了\
jar包还可以包含一个特殊的/META-INF/MANIFEST.MF文件，MANIFEST.MF是纯文本，可以指定Main-Class和其它信息。JVM会自动读取这个MANIFEST.MF文件，如果存在Main-Class，我们就不必在命令行指定启动的类名，而是用更方便的命令：

```bash
java -jar hello.jar
```

jar包还可以包含其它jar包，这个时候，就需要在MANIFEST.MF文件里配置classpath了。

在大型项目中，不可能手动编写MANIFEST.MF文件，再手动创建zip包。Java社区提供了大量的开源构建工具，例如Maven，可以非常方便地创建jar包
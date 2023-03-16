```java
                     ┌───────────┐
                     │  Object   │
                     └───────────┘
                           ▲
                           │
                     ┌───────────┐
                     │ Throwable │
                     └───────────┘
                           ▲
                 ┌─────────┴─────────┐
                 │                   │
           ┌───────────┐       ┌───────────┐
           │   Error   │       │ Exception │
           └───────────┘       └───────────┘
                 ▲                   ▲
         ┌───────┘              ┌────┴──────────┐
         │                      │               │
┌─────────────────┐    ┌─────────────────┐┌───────────┐
│OutOfMemoryError │... │RuntimeException ││IOException│...
└─────────────────┘    └─────────────────┘└───────────┘
                                ▲
                    ┌───────────┴─────────────┐
                    │                         │
         ┌─────────────────────┐ ┌─────────────────────────┐
         │NullPointerException │ │IllegalArgumentException │...
         └─────────────────────┘ └─────────────────────────┘
```
Error和Exception，Error表示严重的错误，程序对此一般无能为力，例如：

OutOfMemoryError：内存耗尽
NoClassDefFoundError：无法加载某个Class
StackOverflowError：栈溢出
而Exception则是运行时的错误，它可以被捕获并处理。

某些异常是应用程序逻辑处理的一部分，应该捕获并处理。例如：

NumberFormatException：数值类型的格式错误
FileNotFoundException：未找到文件
SocketException：读取网络失败

必须捕获的异常，包括Exception及其子类，但不包括RuntimeException及其子类，这种类型的异常称为Checked Exception<br>
注意：编译器对RuntimeException及其子类不做强制捕获要求，不是指应用程序本身不应该捕获并处理RuntimeException。是否需要捕获，具体问题具体分析。

## catch multiple types expcetion
```java
public static void main(String[] args) {
    try {
        process1();
        process2();
        process3();
    } catch (IOException e) {
        System.out.println("Bad input");
    } catch (NumberFormatException e) {
        System.out.println("Bad input");
    } catch (Exception e) {
        System.out.println("Unknown error");
    }
}
// 因为处理IOException和NumberFormatException的代码是相同的，所以我们可以把它两用|合并到一起：

catch (IOException | NumberFormatException e) 
```

## throw a exception

```java
throw new NullPointerException();
```
printStackTrace()可以打印出方法的调用栈<br>
异常可以人为类型转换 然而 e.printStackTrace()会丢失最初异常信息
```java
public class Main {
    public static void main(String[] args) {
        try {
            process1();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static void process1() {
        try {
            process2();
        } catch (NullPointerException e) {
            //如下 为了能追踪到完整的异常栈，在构造异常的时候，把原始的Exception实例传进去，新的Exception就可以持有原始Exception信息
            throw new IllegalArgumentException(e);
        }
    }

    static void process2() {
        throw new NullPointerException();
    }
}
```
在catch中抛出异常，不会影响finally的执行。JVM会先执行finally，然后抛出异常

## Suppressed Exception
```java
public class Main {
    public static void main(String[] args) {
        try {
            Integer.parseInt("abc");
        } catch (Exception e) {
            System.out.println("catched");
            throw new RuntimeException(e);
        } finally {
            System.out.println("finally");
            throw new IllegalArgumentException();
        }
    }
}
```
finally抛出异常后，原来在catch中准备抛出的异常就“消失”了，因为只能抛出一个异常。没有被抛出的异常称为“被屏蔽”的异常(Suppressed Exception)

在极少数的情况下，我们需要获知所有的异常。如何保存所有的异常信息？方法是先用origin变量保存原始异常，然后调用Throwable.addSuppressed()，把原始异常添加进来，最后在finally抛出：

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Exception origin = null;
        try {
            System.out.println(Integer.parseInt("abc"));
        } catch (Exception e) {
            origin = e;
            throw e;
        } finally {
            Exception e = new IllegalArgumentException();
            if (origin != null) {
                e.addSuppressed(origin);
            }
            throw e;
        }
    }
}
```

## Custom Exception
在一个大型项目中，可以自定义新的异常类型，但是，保持一个合理的异常继承体系是非常重要的。

一个常见的做法是自定义一个BaseException作为“根异常”，然后，派生出各种业务类型的异常。

BaseException需要从一个适合的Exception派生，通常建议从RuntimeException派生
```java
public class BaseException extends RuntimeException {
}
```
其他业务类型的异常就可以从BaseException派生：
```java
public class UserNotFoundException extends BaseException {
}

public class LoginFailedException extends BaseException {
}
```

## NullPointerException
空指针异常, 俗称NPE. 如果一个对象为null，调用其方法或访问其字段就会产生NullPointerException，这个异常通常是由JVM抛出的<br>
NullPointerException是一种代码逻辑错误，遇到NullPointerException，遵循原则是早暴露，早修复，严禁使用catch来隐藏这种编码错误：
```java
// 错误示例: 捕获NullPointerException
try {
    transferMoney(from, to, amount);
} catch (NullPointerException e) {
}
```
Java 14新增的功能 `java -XX:+ShowCodeDetailsInExceptionMessages Main.java`
```java
public class Main {
    public static void main(String[] args) {
        Person p = new Person();
        System.out.println(p.address.city.toLowerCase());
    }
}

class Person {
    String[] name = new String[2];
    Address address = new Address();
}

class Address {
    String city;
    String street;
    String zipcode;
}
//能准确看到那哪里引起的NPE
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.toLowerCase()" because "<local1>.address.city" is null
at Main.main(Main.java:5)
```

调用方一定要根据null判断，比如返回null表示文件不存在，那么考虑返回Optional<T>
```java
public Optional<String> readFromFile(String file) {
    if (!fileExist(file)) {
        return Optional.empty();
    }
    ...
}
```
这样调用方必须通过Optional.isPresent()判断是否有结果。

## Assertion
断言失败，抛出AssertionError
使用assert语句时，还可以添加一个可选的断言消息：
```java
assert x >= 0 : "x must >= 0";
```
对可恢复的错误不能使用断言，而应该抛出异常 <br>
断言很少被使用，更好的方法是编写单元测试
```java
public class Main {
    public static void main(String[] args) {
        int x = -1;
        assert x > 0;
        System.out.println(x);
    }
}
```
执行上述代码，发现程序并未抛出AssertionError，而是正常打印了x的值. 这是因为JVM默认关闭断言指令，即遇到assert语句就自动忽略了，不执行。<br>
要执行assert语句，必须给Java虚拟机传递-enableassertions（可简写为-ea）参数启用断言。所以，上述程序必须在命令行下运行才有效果
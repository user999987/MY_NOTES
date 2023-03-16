1. 多态
```java
class AA {
    public int i=10;

    public int getResult(){
        return i+10;
    }
}

class BB extends AA {
    public int i =20;

    // public int getResult(){
    //     return i+20;
    // }
}

// 多态 一个对象的多种形态
AA aa = new BB()
// 动态绑定机制 JVM 在执行 对象的成员方法时，会将这个方法和对象的实际内存进行绑定然后调用，
// 动态绑定机制和变量没有关系，只和方法有关系
aa.getResult()

>>>20
```

2. 重载
```java
public class Main {
    public static void main(final String[] args){
        // System.out.println(Arrays.toString(args));
        // int a = 1; int b = a++; int c = ++b;
        // int[] x= {a,b,c};
        // System.out.println(Arrays.toString(x));
        B a= new C();
        a.a();
        //System.out.println(a.getClass());
        test(a);
    }
    public static void test(C c){
        System.out.println(c.getClass());
        System.out.println("ccc");
    }
    public static void test(B b){
        System.out.println(b.getClass());
        System.out.println("bbb");
    }
}
interface A{
    void a();
}
class B implements A{
    public void a(){
        System.out.println('b');
    }
}
class C extends B {}

>>>class C
>>>bbb
```


```java
public class Main {
    public static void main(final String[] args){
        // System.out.println(Arrays.toString(args));
        // int a = 1; int b = a++; int c = ++b;
        // int[] x= {a,b,c};
        // System.out.println(Arrays.toString(x));
        byte a= 10;
        a.a();
        //System.out.println(a.getClass());
        test(a);
    }
    // 8bits
    public static void test(byte b){
        System.out.println("bbb");
    }
    //16bits
    public static void test(short b){
        System.out.println("ssss");
    }
    //16bits 这个不会被调用因为你 char 没有负数
     public static void test(char c){
        System.out.println("cccc");
    }
    //32bits
     public static void test(int i){
        System.out.println("iiii");
    }
}

```
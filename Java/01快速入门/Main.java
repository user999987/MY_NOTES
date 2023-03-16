import java.util.Arrays;
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





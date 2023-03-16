import java.util.Scanner;
import java.util.Arrays;
import java.util.Collections;

public class Hello {
    public static void main(final String[] args){
        final Scanner scanner = new Scanner(System.in); // 创建Scanner对象
        System.out.print("Input your name: "); // 打印提示
        final String name = scanner.nextLine(); // 读取一行输入并获取字符串
        System.out.print("Input your age: "); // 打印提示
        final int age = scanner.nextInt(); // 读取一行输入并获取整数
        System.out.printf("Hi, %s, you are %d\n", name, age); // 格式化输出
        System.out.println("hello, world!");
        // nomral for loop
        final String[] ns = { "1", "4", "9", "16", "25" };
        for (int i=0; i<ns.length; i++) {
            final String n = ns[i];
            System.out.println(n);
        }
        // enhanced for loop
        for (final String n : ns) {
            System.out.println(n);
        }
        // print array content
        final Integer[] ns1 = { 1, 1, 2, 3, 5, 8 };
        System.out.println(Arrays.toString(ns1));
        Arrays.sort(ns1, Collections.reverseOrder());
        System.out.println(Arrays.toString(ns1));
        //三位数组
        int[][][] ns2 = {
            {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
            },
            {
                {10, 11},
                {12, 13}
            },
            {
                {14, 15, 16},
                {17, 18}
            }
        };
        for (int[][] arr2d : ns2) {
            for (int[] arr1d: arr2d) {
                for(int n: arr1d){
                    System.out.print(n);
                    System.out.print(", ");
                }
            }
            System.out.println();
        }
        System.out.println(Arrays.deepToString(ns2));
    }
}
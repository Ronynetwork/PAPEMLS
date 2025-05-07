import java.util.concurrent.atomic.AtomicInteger;

public class AtomicExample {
    public static void main(String[] args) {
        AtomicInteger a1 = new AtomicInteger(5);
        AtomicInteger a2 = new AtomicInteger(5);

        boolean equal = a1.equals(a2);  // Noncompliant - Sonar Rule 2204
        System.out.println("Equal? " + equal);
    }
}

import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;
        BigDecimal bd1 = new BigDecimal(d);    // Noncompliant: Problema de precisão
    }
}

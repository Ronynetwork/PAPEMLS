import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;

        BigDecimal bd1 = new BigDecimal(d);    // Noncompliant: Problema de precisão
        BigDecimal bd2 = new BigDecimal(1.1);  // Noncompliant: Problema de precisão
        BigDecimal bd3 = new BigDecimal(f);    // Noncompliant: Problema de precisão
    }
}

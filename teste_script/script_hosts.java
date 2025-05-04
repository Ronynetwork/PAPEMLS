import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;

        BigDecimal bd = new BigDecimal(d);
        BigDecimal bd2 = new BigDecimal(f);

        System.out.println(bd.equals(bd2)); // Verifica se os valores são iguais
    }
}


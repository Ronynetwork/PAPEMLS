import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;
        BigDecimal bd1 = new BigDecimal(d);
        // BigDecimal.valueOf() não é necessário em Java 7+ e pode causar problemas
        // com precisão de float (float é menor que double, então não é possível usar BigDecimal)
        // Para evitar problemas, podemos usar BigDecimal.valueOf(f) aqui
    }
}


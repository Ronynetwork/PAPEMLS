import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;

        // Corrigir a declaração de bd1 para evitar o uso de um local não usado.
        BigDecimal bd1 = new BigDecimal(d);
        
        // Verificar que BD1 não contenha valor nulo
        if (bd1 != null) {
            System.out.println("BD1 " + bd1);
        } else {
            System.out.println("BD1 é nuló");
        }
    }
}


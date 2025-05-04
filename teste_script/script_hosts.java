import java.math.BigDecimal;

public class TesteBigDecimalErro {
    public static void main(String[] args) {
        double d = 1.1;
        float f = 2.2f;
        
        // Utilizar BigDecimal.valueOf() para obter a representação decimal específica de f
        BigDecimal bd1 = new BigDecimal(f);
        
        // Para evitar problemas com precisão de float, podemos usar BigDecimal.valueOf(f) aqui.
    }
}


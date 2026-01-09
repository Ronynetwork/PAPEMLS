import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;

import java.io.File;

public class XXEVulnerable {

    public static void main(String[] args) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        // ❌ Configuração insegura (XXE habilitado por padrão)
        DocumentBuilder builder = factory.newDocumentBuilder();

        Document document = builder.parse(new File("input.xml"));
        document.getDocumentElement().normalize();

        System.out.println("Root element: " + document.getDocumentElement().getNodeName());
    }
}

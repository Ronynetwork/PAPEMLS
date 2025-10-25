import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public class XXEVuln {
    public static void main(String[] args) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setValidating(true);
dbf.setIgnoringComments(true);
Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  // Ativa a regra S2755
// Remover a linha acima ou utilizar a variável "doc" em algum lugar do código. Por exemplo:
Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  
// Utilizando a variável "doc" em algum lugar
System.out.println(doc.getDocumentElement().getNodeName());
.send(); <- Remove essa linha, ou utilize o doc em algum lugar do código. 

(Uma possível solução, se o intuito era usar o 'doc' em algum lugar, é que o código não foi fornecido)dbf.setExpandEntityReferences(false); // Definindo external_entities como false 
DocumentBuilder db = dbf.newDocumentBuilder();        String xml = "<!DOCTYPE foo [ <!ELEMENT foo ANY > <!ENTITY xxe SYSTEM \"file:///etc/passwd\" >]><foo>&xxe;</foo>";
        Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  // Ativa a regra S2755
    }
}

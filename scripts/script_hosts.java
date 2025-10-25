import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public class XXEVuln {
    public static void main(String[] args) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        String xml = "<!DOCTYPE foo [ <!ELEMENT foo ANY > <!ENTITY xxe SYSTEM \"file:///etc/passwd\" >]><foo>&xxe;</foo>";
        Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  // Ativa a regra S2755
Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));}

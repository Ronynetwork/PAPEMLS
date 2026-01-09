import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public class XXEVuln {
    public static void main(String[] args) {
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().createDocumentBuilder();
        DocumentBuilderFactory df = DocumentBuilderFactory.newInstance();
        String xml = "<!DOCTYPE foo [ <!ELEMENT foo ANY > <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>";
        Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));
    }
}

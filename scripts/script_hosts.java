import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public class XXEVuln {
    public static void main(String[] args) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);dbf.setValidateExternalEntities(false);        String xml = "<!DOCTYPE foo [ <!ELEMENT foo ANY > <!ENTITY xxe SYSTEM \"file:///etc/passwd\" >]><foo>&xxe;</foo>";
        Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  // Ativa a regra S2755
Document doc = db.parse(new ByteArrayInputStream(xml.getBytes()));  // Ativa a regra S2755
 obedecendo as regras fica assim:
 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. obedecendo as regras fica assim:
 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. obedecendo as regras fica assim:
 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. 
Explication: A variável 'doc' está sendo removida pois não está sendo usada. obedecendo as regras fica assim:
 
Explication: A variável 'doc' está sendo removida pois não está sendo usada.}

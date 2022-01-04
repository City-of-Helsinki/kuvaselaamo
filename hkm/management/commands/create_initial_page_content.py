# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from hkm.models.models import PageContent
from hkm.models.models import Collection
from hkm.models.models import Record
from hkm.models.models import User
from hkm.models.models import PrintProduct

pages = [{
    "name": u"About",
    "identifier": u"hkm_siteinfo_about",
    "texts": [
        {
            "language": u"fi",
            "title": u"Tietoa palvelusta",
            "content": u"""
                <p>Helsinkikuvia.fi-palvelu tarjoaa Helsinki-aiheisia valokuvia Helsingin kaupunginmuseon kokoelmista. Valokuvia voi ladata omalle laitteelleen korkearesoluutioisina eli painokelpoisina tai pienempinä, verkkoon sopivina kuvina.</p>
                <p>Kuvat on julkaistu CC BY 4.0 -lisenssillä. Se merkitsee, että kuvia voi käyttää haluamallaan tavalla maksutta, kunhan mainitsee kuvan yhteydessä kuvaajan nimen ja Helsingin kaupunginmuseon. Lisenssi sallii myös kuvien kaupallisen käytön, jos lainsäädäntö ei sitä estä. Esimerkiksi henkilökuvien käyttö markkinoinnissa ja mainonnassa on kielletty ilman kuvassa olevan henkilön suostumusta.</p>
                <p>Helsinkikuvia.fi-palvelussa voi hakea kuvia erilaisilla hakusanoilla, selata museon luomia kuva-albumeita eri aiheista tai luoda omia albumeita ja lisätä niihin suosikkikuviaan.</p>
                <p>Helsinkikuvia.fi-palvelussa on julkaistu Helsingin kaupunginmuseon valokuvakokoelman kaikki digitoidut kuvat, tällä hetkellä noin 65 000 kuvaa. Lisää tulee saataville sitä mukaa kuin kuvien digitointi etenee. Jos kaipaat kuvaa, jota ei löydy Helsinkikuvia.fi-palvelusta, ota yhteys Helsingin kaupunginmuseon Kuvaselaamoon.</p>
                <p>Helsinkikuvia.fi-palvelun kuvat ovat saatavilla myös kansallisessa Finna-palvelussa osoitteessa hkm.finna.fi. Valokuvien lisäksi Finnassa voi tutkia muutakin Helsinki-aiheista aineistoa muovipusseista hiustenkuivajiin ja matkalipuista taideteoksiin. Sieltä voi myös hakea tietoa helsinkiläisten rakennusten historiasta.</p>
            """
        }, {
            "language": u"en",
            "title": u"Information about the service",
            "content": u"""
                    <p>Helsinkiphotos.fi is an image service that provides a user-friendly way to access the Helsinki City Museum’s vast collection of photographs. At Helsinkiphotos.fi, anyone can browse, search and download detailed, high resolution photographs suitable for print materials or lower resolution images more suitable for web and social media use.</p>
                    <p>The photographs in the service are published under Creative Commons BY 4.0 license. In brief, CC BY means that you may use and edit the photographs for any purpose as long as you credit the source of the photograph, in this case Helsinki City Museum and the photographer. The photographs may be used commercially, with certain restrictions. For instance, a person’s right to decide on the commercial use of their name, photograph or other identifiable part of their identity, privacy protection rights and moral rights may limit the use of the material.</p>
                    <p>The Helsinkiphotos.fi service also allows users to conduct Finnish-language searches, browse curated photo albums or create their own albums by logging into the service.</p>
                    <p>Currently, the service has approximately 65,000 digitized photographs. More images are being digitized and added to the system constantly. If you need a digital image that is not currently found in the Helsinkiphotos.fi service, please contact the museum’s Picture Browsery.</p>
                    <p>The photographs of the Helsinki City Museum collection are still available in the national Finna service at hkm.finna.fi. In addition to photographs, you can also browse other material related to Helsinki in Finna, everything from plastic bags to hairdryers and bus tickets to works of art. You can also search the history of the buildings of Helsinki.</p>
            """
        }, {
            "language": u"sv",
            "title": u"Information om tjänsten",
            "content": u"""
                    <p>Helsingfors stadsmuseums foton från olika tidsperioder med Helsingfors som tema kan användas fritt i och med att tjänsten Helsingforsbilder.fi öppnas. Bland fotona finns bland annat alla Signe Branders älskade bilder på Helsingfors för hundra år sedan samt Simo och Eeva Ristas omfattande och betydelsefulla samling om en föränderlig stad på 1970-talet.</p>
                    <p>Museet har bilder ända från 1840-talet, så det är till exempel möjligt att gå igenom spårvagnarnas historia i bilder ända från 1800-talet till 2000-talet. Nu presenteras cirka 65 000 bilder för allmänheten, och fler blir tillgängliga i och med att digitaliseringen framskrider. Endast en bråkdel av bilderna i museets samlingar är digitaliserade.</p>
                    <p>Museet lämnar ut bilderna med CC BY 4.0 licens. Man kan ladda ner bilder och använda dem fritt och utan avgift på nätet och i olika applikationer, och även till exempel i böcker, presentartiklar eller tryckta på tapet, bara man anger fotografens namn och Helsingfors stadsmuseum i samband med bilden. Licensen tillåter kommersiell användning av bilderna om lagstiftningen inte hindrar detta. Till exempel är det förbjudet att använda bilder på personer i marknadsföring och reklam utan tillåtelse av personer som är med på bilden.</p>
                    <p>Tjänsten omfattar i praktiken alla bilder som stadsmuseet har digitaliserat, dvs. omvandlat till digital form. Om du behöver en digital version av en bild som inte har digitaliserats, kan du beställa den via stadsmuseets Bildapotek. För digitaliseringar uppbärs en avgift enligt museets prislista. Den bild som du beställt publiceras oftast med en liten fördröjning i tjänsten Helsingforsbilder.fi och är efter det tillgänglig för alla.</p>
                    <p>Helsingfors stadsmuseums bilder finns fortfarande också i den nationella tjänsten Finna på adressen hkm.finna.fi. Utöver bilder kan man i Finna även bekanta sig med annat material med Helsingfors som tema, från plastpåsar till hårtorkar och från resebiljetter till konstverk. Man kan också söka information om byggnadernas historia i Helsingfors.</p>
            """
        }
    ]
}, {
    "name": u"QA",
    "identifier": u"hkm_siteinfo_QA",
    "texts": [
            {
                "language": "fi",
                "title": u"Kysymyksiä ja vastauksia",
                "content": u"""
                    <h1 class="section-title">Helsinkikuvia.fi-palvelun käyttäminen</h1>
                
                    <p class="question">Mitä Helsinkikuvia.fi-palvelussa voi tehdä?</p>
                    <p>Helsinkikuvia.fi-palvelussa voi hakea valokuvia erilaisilla hakusanoilla, selata museon luomia kuva-albumeita eri aiheista tai luoda omia albumeita ja lisätä niihin suosikkikuviaan. Valokuvia voi ladata omalle laitteelleen korkearesoluutioisina eli painolaatuisina tai pienempinä, verkkolaatuisina kuvina.</p>
                    <p class="question">Mitä kuvia palvelussa on?</p>
                    <p>Helsinkikuvia.fi-palvelussa on kymmeniä tuhansia Helsinkiin liittyviä valokuvia 1840-luvulta nykypäivään asti. Kuvat ovat peräisin Helsingin kaupunginmuseon kokoelmista.</p>
                    <p class="question">Voiko palvelua käyttää muilla kielillä?</p>
                    <p>Kyllä, ruotsiksi ja englanniksi. Valokuvien kuvailutiedot ja asiasanat ovat kuitenkin ainoastaan suomeksi, mikä vaikeuttaa hakujen tekemistä muilla kielillä.</p>
                    <p class="question">Mitä hyödyn kirjautumisesta Helsinkikuvia.fi-palveluun?</p>
                    <p>Kun kirjaudut, voit luoda palvelussa omia albumeja ja lisätä niihin suosikkikuviasi.</p>
                    <p class="question">Mitä tarkoittaa korkearesoluutioinen kuva? Miten osaan valita, minkälaisen kuvan laitteelleni lataan?</p>
                    <p>Korkearesoluutioinen kuva on sellainen, jota voi käyttää laadukkaassa painotuotteessa, esimerkiksi julisteessa. Pienempiresoluutioisia eli verkkolaatuisia kuvia voi käyttää esimerkiksi verkkosivuilla tai sosiaalisessa mediassa.</p>
                    <p class="question">Miten voin tilata kuvatuotteen?</p>
                    <p>Voit tilata kuvatuotteen Kuvaselaamon sivuilta löytävällä <a href="https://www.helsinginkaupunginmuseo.fi/kuvia-esineita-helsinkia/kuva-arkisto/" target="_blank">verkkolomakkeella</a>. Kuvien toimitusaika on noin viikko.</p>
                
                    <h1 class="section-title">Valokuvien käyttö</h1>
                
                    <p class="question">Paljonko kuvan lataaminen tai käyttö maksaa?</p>
                    <p>Valokuvien lataaminen ja käyttö eivät maksa mitään.</p>
                    <p class="question">Mitä kaikkea palvelusta löytyvillä valokuvilla voi tehdä?</p>
                    <p>Melkein mitä vain! Kunhan muistaa mainita kuvan yhteydessä kuvaajan nimen ja Helsingin kaupunginmuseon, kuvia voi käyttää monipuolisesti. Kuvia voi esimerkiksi jakaa sosiaalisessa mediassa, käyttää verkkosivuilla tai sovelluksissa. Kuvista voi tehdä tai teettää vapaasti myös tauluja, kirjoja, lehtiä, lahjatavaroita tai vaikka tapetteja. Mahdollisuus tutkia hyvinkin tarkkoja yksityiskohtia helpottaa myös opetus- ja tutkimuskäyttöä. Myös kaupallinen käyttö on sallittua tietyin rajoituksin.</p>
                    <p class="question">Millä tavalla kaupunginmuseo ja kuvaajan nimi on mainittava kuvan yhteydessä?</p>
                    <p>Vaikkapa näin: 'Kuva: Helsingin kaupunginmuseo / Kuvaajan Nimi'. Jos kuvaajan nimeä ei ole tiedossa, riittää pelkkä Helsingin kaupunginmuseo. Esimerkiksi Twitterissä riittää maininta @kaupunginmuseo sekä kuvaajan nimi, jos se on tiedossa.</p>
                    <p class="question">Eivätkö tekijänoikeudet tai henkilötietolaki aseta rajoituksia kuvien julkaisulle?</p>
                    <p>Tekijänoikeudet, henkilötietolaki ja intimiteettisuoja otetaan huomioon kuvia julkaistaessa. Julkaisemme palvelussa vain valokuvia, joiden oikeuksista Helsingin kaupunginmuseo on sopinut tai jotka ovat jo niin vanhoja, että tekijänoikeuden rajoitukset eivät niitä koske. Lisäksi tietyt teemat arvioidaan perusteellisesti ennen verkossa julkaisemista. Tällaisia ovat esimerkiksi lapsikuvat, alastomuus tai henkilön poliittisen suuntautuneisuuden paljastavat kuvat.</p>
                    <p class="question">Onko kuvien kaupalliseen käyttöön rajoituksia?</p>
                    <p>Kyllä. Esimerkiksi henkilökuvien käyttö markkinoinnissa ja/tai mainonnassa on kielletty ilman kuvassa olevan henkilön suostumusta. Lisäksi on mainittava Helsingin kaupunginmuseo ja kuvaajan nimi.</p>
                    <p class="question">Mitä tarkoittaa, että kuvat on julkaistu lisenssillä CC BY 4.0?</p>
                    <p>Helsingin kaupunginmuseon julkaisemat kuvat Helsinkikuvia.fi-palvelussa on lisensoitu 'Creative Commons Nimeä 4.0 Kansainvälinen' eli CC BY 4.0 -lisenssillä. Lyhyesti ilmaistuna se tarkoittaa, että kuvia voi käyttää ja muunnella missä tarkoituksessa tahansa, kunhan mainitsee kuvalähteen. Lisenssi ei poista käyttäjän vastuuta. Esimerkiksi henkilön oikeus määrätä nimensä, kuvansa tai henkilönsä muun tunnistettavan osan kaupallisesta käytöstä, yksityisyyden suojaa koskevat oikeudet tai moraaliset oikeudet voivat rajoittaa aineiston käyttöä.</p>
                
                    <h1 class="section-title">Kaipaan lisätietoa tai lisää kuvia</h1>
                
                    <p class="question">Mistä saan lisätietoa kuvista, tietystä aineistosta tai Helsingin historiasta?</p>
                    <p>Voit ottaa yhteyttä Helsingin kaupunginmuseon Kuvaselaamoon. Jos haluat tutkia tiettyä aineistoa tai tarvitset muita kuva-arkistopalveluja, käyntiaika ja aineistot on varattava etukäteen.</p>
                    <p class="question">Mitä teen, jos en löydä sopivaa kuvaa Helsinkikuvia.fi-palvelusta?  Jos Helsinkikuvia.fi-palvelussa ei kerran ole kaikkia kuvianne, miten niitä muita pääsee tutkimaan?</p>
                    <p>Palvelussa on käytännössä kaikki kaupunginmuseon digitoidut eli sähköiseen muotoon saatetut kuvat. Lisää tulee saataville sitä mukaa kuin kuvien digitointi etenee. Museon kokoelmien kuvista on digitoitu vasta murto-osa. Jos et löydä Helsinkikuvia.fi-palvelusta sopivaa kuvaa, voit ottaa yhteyttä Helsingin kaupunginmuseon Kuvaselaamoon. Jos haluat tutkia tiettyä aineistoa tai tarvitset muita kuva-arkistopalveluja, käyntiaika ja aineistot on varattava etukäteen.</p>
                    <p class="question">Lisäättekö palveluun pyynnöstä digitoimattomia kuvianne? Onko se maksullista?</p>
                    <p>Helsinkikuvia.fi-palvelussa on käytännössä kaikki Helsingin kaupunginmuseon digitoidut valokuvat. Jos tarvitset digitaalisen version kuvasta, jota ei ole digitoitu, voit tilata sen kaupunginmuseon Kuvaselaamoon. Asiakkaan tilaamista digitoinneista veloitetaan museon hinnaston mukainen maksu. Tilaamasi kuva tulee usein pienellä viiveellä Helsinkikuvia.fi-palveluun kaikkien nähtäväksi ja käytettäväksi.</p>
                    <p class="question">Kuvan tiedoissa on mielestäni virhe, mihin voin korjata sen?</p>
                    <p>Voit ottaa yhteyttä Helsingin kaupunginmuseon Kuvaselaamoon.</p>
                    <p class="question">Mistä kaupunginmuseo on saanut kuvat? Kenen kuvia ne oikein ovat?</p>
                    <p>Kaupunginmuseon kokoelmissa on lähes miljoona valokuvaa Helsingistä ja helsinkiläisten arjesta 1840-luvulta nykypäivään. Kokoelmiin tulee uusia kuvia pääsääntöisesti lahjoituksina ja museon omien tai museon palkkaamien kuvaajien kuvaamina. Valokuvakokoelman kartuttamisen aloitti kaupunginmuseon edeltäjä, Helsingin muinaismuistolautakunta, vuonna 1906. Helsinki-kuvistaan tunnettu Signe Brander palkattiin tallentamaan muuttuvaa kaupunkia vuonna 1907. Branderin ottamat kuvat muodostavat kaupunginmuseon valokuvakokoelmien perustan.</p>
                    <p class="question">Onko kuvianne edelleen Finna-palvelussa? Onko Finnassa samat kuvat kuin Helsinkikuvia.fi-palvelussa?</p>
                    <p>Helsingin kaupunginmuseon valokuvat ovat edelleen myös kansallisessa Finna-palvelussa osoitteessa hkm.finna.fi. Valokuvien lisäksi Finnassa voi tutkia muutakin Helsinki-aiheista aineistoa muovipusseista hiustenkuivaajiin ja matkalipuista taideteoksiin. Sieltä voi myös hakea tietoa helsinkiläisten rakennusten historiasta.</p>
                """
            },
        {
                "language": "en",
                "title": u"Questions and answers",
                "content": u"""
                    <h1 class="section-title">The use of Helsinkiphotos.fi service</h1>
                
                    <p class="question">What can I do in the Helsinkiphotos.fi service?</p>
                    <p>In the Helsinkiphotos.fi service, you can search for photographs with different search words, browse albums created by the museum or create albums of your own. You can download images on your own device in high resolution, or as smaller versions that are more convenient to use online.</p>
                    <p class="question">What kind of photographs can I find in the service?</p>
                    <p>The Helsinkiphotos.fi service includes tens of thousands of photographs related to Helsinki from the 1840s to modern days. The photographs are from the Helsinki City Museum’s collections.</p>
                    <p class="question">Can I use the service in a language other than Finnish?</p>
                    <p>Yes, in Swedish and English. However, the descriptions and keywords of the photographs are only in Finnish, which will make searching for photographs difficult in other languages.</p>
                    <p class="question">What will I get from creating an account in the Helsinkiphotos.fi service?</p>
                    <p>When you log in, you can create your own albums in the service and add your own favorite images to them.</p>
                    <p class="question">What do you mean by a high resolution image? How do I know what kind of an image I should download on my device?</p>
                    <p>A high resolution image can be used in high-quality print products, such as posters. Smaller resolution images are more convenient for online use.</p>
                    <p class="question">How do I order picture prints?</p>
                    <p>You can order picture prints using <a href="https://www.helsinginkaupunginmuseo.fi/en/pictures-objects-helsinki/picture-browsery/" target="_blank">the online form</a> found on City Museum’s website. The delivery time is about a week.</p>
                
                    <h1 class="section-title">Using the photographs</h1>
                
                    <p class="question">How much does it cost to download or use the images?</p>
                    <p>Downloading and using the images is free.</p>
                    <p class="question">What can I do with the photographs I find from the service?</p>
                    <p>Almost anything! As long as you remember to credit the photographer and Helsinki City Museum in connection with the photograph, you can use it in a variety of ways. You can share them on social media or use them on your website and in different applications. You can also freely use the photographs in your magazines, gift products or as posters or even wallpaper. The high level of detail in the images allows for research and teaching use. Commercial use of the images is allowed within certain restrictions.</p>
                    <p class="question">How do I mention the Helsinki City Museum and the photographer’s name in connection with the photograph?</p>
                    <p>Here’s one way of doing it: 'Photo: Helsinki City Museum / Name of the photographer.' If the photographer’s name isn’t mentioned in the image data, you can simply credit Helsinki City Museum. On Twitter, for instance, it’s enough to mention @kaupunginmuseo / name of the photographer.</p>
                    <p class="question">Do copyright or the Personal Data Act limit publishing the photographs?</p>
                    <p>Copyright, the Personal Data Act and Protection of Privacy are taken into consideration when publishing the photographs. In the service, we only publish photographs with copyright agreed upon with the Helsinki City Museum or photographs that are so old that the copyright restrictions no longer apply to them. In addition, certain themes are thoroughly assessed before publishing the photographs online. These themes include photographs of children, nudity or photographs revealing for example private political opinions.</p>
                    <p class="question">Are there any restrictions on the commercial use of the images?</p>
                    <p>Yes. For instance, it is prohibited to use portraits or other identity-depicting images in marketing and/or advertising without the person’s consent. In addition, you must always credit Helsinki City Museum and the photographer.</p>
                    <p class="question">What does it mean that the photographs have been published with a Creative Commons BY 4.0 license?</p>
                    <p>What does it mean that the photographs have been published with a Creative Commons BY 4.0 license? Answer</p>
                
                    <h1 class="section-title">I need more information or more photographs</h1>
                
                    <p class="question">Where can I get more information about the photographs or the history of Helsinki?</p>
                    <p>You can contact Helsinki City Museum’s Picture Browsery. If you would like to look at specific material or you need other photo archive services, you must book an appointment and reserve the material in advance.</p>
                    <p class="question">What should I do if I cannot find the appropriate photograph from the Helsinkiphotos.fi service? If the Helsinkiphotos.fi service does not have all your photographs, how can I study the rest?</p>
                    <p>This service contains practically all of the digitized photographs of the Helsinki City Museum. More photographs are digitized constantly. Thus far, only a fraction of the photographs in the entire museum collection has been digitized. If you can’t find the right photograph from the Helsinkiphotos.fi service, you can contact Helsinki City Museum’s Picture Browsery</p>
                    <p class="question">Will you add photographs that have not yet been digitised to the service upon request? Is that subject to a charge?</p>
                    <p>If you need a digital version of a photograph that has not yet been digitized, you can order it from the City Museum’s Picture Browsery. We charge a fee according to the museum price list on digitized photographs. The photograph you order for digitization will possibly be available at the Helsinkiphotos.fi service with a small delay for everyone to see and use.</p>
                    <p class="question">I think there is an error in an image’s data, whom can I contact?</p>
                    <p>You can contact Helsinki City Museum’s Picture Browsery.</p>
                    <p class="question">Where did the City Museum get all these photographs? Whose photographs are they?</p>
                    <p>The City Museum’s collection has almost one million photographs of Helsinki and the everyday life of its inhabitants from the 1840s until today. New photographs are added to the collection mainly as donations or are taken by photographers commissioned by the museum. The City Museum’s predecessor, the Helsinki Board of Antiquities, began accumulating the collection in 1906. Signe Brander, known for her Helsinki photography, was commissioned to record the changing city in 1907. Brander’s photographs are the foundation of the City Museum’s photography collections.</p>
                    <p class="question">Is the Finna service still in use? Can I still find images from Helsinki City Museum in Finna?</p>
                    <p>The photographs of Helsinki City Museum collection are still available in the national Finna service at hkm.finna.fi. In addition to photographs, you can browse the museum’s object collections, from plastic bags to hairdryers and works of art. In Finna you can also find information about the buildings of Helsinki.</p>
                """
            }, {
                "language": "sv",
                "title": u"Frågor och svar",
                "content": u"""            
                    <h1 class="section-title">Användning av tjänsten Helsingforsbilder.fi</h1>
                    
                    <p class="question">Vad kan man göra i tjänsten Helsingforsbilder.fi?</p>
                    <p>I tjänsten Helsingforsbilder.fi kan man söka efter foton med olika sökord, bläddra i museets album med olika teman eller skapa egna album och lägga till sina egna favoritbilder i dem. Man kan också ladda ned bilder till sin egen enhet. Bilderna är tillgängliga både som högupplösta och som mindre versioner, vilket gör att de kan användas såväl i trycksaker som på webben.</p>
                    <p class="question">Vilka bilder finns i tjänsten?</p>
                    <p>I tjänsten Helsingforsbilder.fi finns tiotusentals foton med anknytning till Helsingfors, från 1840-talet till i dag. Bilderna hör till Helsingfors stadsmuseums samlingar.</p>
                    <p class="question">Kan man använda tjänsten på andra språk?</p>
                    <p>Ja, på finska och engelska. Eftersom bildernas metadata och nyckelord endast finns på finska, är det lättare att göra sökningar på finska.</p>
                    <p class="question">Varför lönar det sig att logga in i tjänsten Helsingforsbilder.fi?</p>
                    <p>Om du loggar in kan du skapa egna album i tjänsten och lägga till dina favoritbilder i dem.</p>
                    <p class="question">Vad betyder en högupplöst bild? Hur vet jag vilken version jag ska ladda ned?</p>
                    <p>En högupplöst bild kan användas i högklassiga trycksaker, t.ex. på affischer. Bilder med lägre upplösning lämpar sig för att användas t.ex. på webbplatser eller i sociala medier.</p>
                    <p class="question">Hur beställer jag en bildprodukt?</p>
                    <p>Du kan beställa en bildprodukt med hjälp av <a href="https://www.helsinginkaupunginmuseo.fi/sv/bilder-foremal-helsingfors/fotoapoteket/" target="_blank">formuläret</a> som finns på stadsmuseets hemsida under rubriken Bildapoteket. Leveranstiden för bilderna är ca en vecka.</p>
                    
                    <h1 class="section-title">Användning av fotografier</h1>
                    
                    <p class="question">Vad kostar det att ladda ned eller använda en bild?</p>
                    <p>Att ladda ned och använda bilder kostar ingenting.</p>
                    <p class="question">Vad kan man göra med bilderna i tjänsten?</p>
                    <p>Nästan vad som helst! Man kan fritt använda bilderna, bara man kommer ihåg att nämna fotografens namn och Helsingfors stadsmuseum i anslutning till bilden. Man kan till exempel dela bilder i sociala medier eller använda dem på webbplatser eller i applikationer. Bilderna kan också användas för att göra t.ex. tavlor, böcker, tidningar, presentartiklar eller tapeter. Tack vare möjligheten att undersöka mycket exakta detaljer lämpar sig bilderna också för undervisnings- och forskningsbruk. Även kommersiellt bruk är tillåtet med vissa begränsningar.</p>
                    <p class="question">Hur ska stadsmuseet och fotografens namn nämnas i anslutning till bilden?</p>
                    <p>Till exempel så här: 'Bild: Helsingfors stadsmuseum/Fotografens namn'. Om fotografens namn inte är känt, räcker det att man nämner Helsingfors stadsmuseum. Till exempel på Twitter räcker det med hänvisningen @kaupunginmuseo och fotografens namn (om detta är känt).</p>
                    <p class="question">Utgör inte upphovsrätten eller personuppgiftslagen begränsningar för publicering av bilder?</p>
                    <p>Upphovsrätten, personuppgiftslagen och integritetsskyddet beaktas vid publicering av bilder. I tjänsten publicerar vi endast bilder som vi har rätt att använda eller som redan är så gamla att upphovsrätten har upphört. Dessutom finns det vissa teman som gör att vi noggrant överväger om bilden ska publiceras på nätet eller inte. Sådana är t.ex. bilder på barn eller nakna människor eller bilder som avslöjar en persons politiska ståndpunkt.</p>
                    <p class="question">Finns det några begränsningar gällande kommersiellt bruk av bilderna?</p>
                    <p>Ja. Det är förbjudet att t.ex. använda bilder på personer i marknadsföring eller reklam utan att ha fått tillåtelse av personerna i fråga. Man ska också nämna Helsingfors stadsmuseum och fotografens namn.</p>
                    <p class="question">Vad betyder att bilderna har publicerats med licensen CC BY 4.0?</p>
                    <p>Helsingfors stadsmuseums bilder i tjänsten Helsingforsbilder.fi är licensierade med licensen 'Creative Commons Erkännande 4.0 Internationellt', dvs. CC BY 4.0 . Kort sagt betyder det att man fritt kan använda och bearbeta bilderna, bara man anger källan. Licensen befriar inte användaren från ansvar. Till exempel personens rätt att bestämma om kommersiellt bruk av hans eller hennes namn, bild eller andra identifierbara uppgifter, rättigheter som gäller integritetsskydd samt moraliska rättigheter kan begränsa användningen av materialet.</p>
                    
                    <h1 class="section-title">Jag behöver mer information eller fler bilder</h1>
                    
                    <p class="question">Var får jag mer information om bilderna, ett visst material eller Helsingfors historia?</p>
                    <p>Du kan kontakta Helsingfors stadsmuseums Bildapotek. Om du letar efter specifikt material eller behöver andra bildarkivstjänster måste du boka en besökstid och beställa materialet på förhand.</p>
                    <p class="question">Vad gör jag om jag inte hittar en lämplig bild i tjänsten Helsingforsbilder.fi? Hur får man tillgång till de bilder som ni inte har publicerat i tjänsten?</p>
                    <p>Tjänsten omfattar i praktiken alla bilder som stadsmuseet har digitaliserat, dvs. omvandlat till digital form. Fler bilder blir tillgängliga i och med att digitaliseringen framskrider. Endast en bråkdel av bilderna i museets samlingar är digitaliserade. Om du inte hittar en lämplig bild i tjänsten Helsingforsbilder.fi, kan du kontakta Helsingfors stadsmuseums Bildapotek. Om du letar efter specifikt material eller behöver andra bildarkivstjänster måste du boka en besökstid och beställa materialet på förhand.</p>
                    <p class="question">Lägger ni till bilder som inte ännu digitaliserats i tjänsten på begäran? Kostar det någonting?</p>
                    <p>Tjänsten omfattar i praktiken alla bilder som stadsmuseet har digitaliserat, dvs. omvandlat till digital form. Om du behöver en digital version av en bild som inte har digitaliserats, kan du beställa den via stadsmuseets Bildapotek. För digitaliseringar uppbärs en avgift enligt museets prislista. Den bild som du beställt publiceras oftast med en liten fördröjning i tjänsten Helsingforsbilder.fi och är efter det tillgänglig för alla.</p>
                    <p class="question">Jag tycker att det finns ett fel i bildens uppgifter, hur kan jag rätta det?</p>
                    <p>Du kan kontakta Helsingfors stadsmuseums Bildapotek.</p>
                    <p class="question">Varifrån har stadsmuseet fått bilderna? Vems bilder är de?</p>
                    <p>Stadsmuseets samlingar innehåller nästan en miljon bilder av Helsingfors och helsingforsarnas vardag från 1840-talet till i dag. Museet får nya bilder till sina samlingar i regel som donationer, men nya bilder tas även av museets egna fotografer och frilansfotografer. Fotosamlingen påbörjades av stadsmuseets föregångare, Helsingfors fornminnesnämnd, år 1906. Signe Brander, som var känd för sina bilder från Helsingfors, anställdes år 1907 för att föreviga den föränderliga staden. Branders bilder utgör grunden för stadsmuseets fotosamlingar.</p>
                    <p class="question">Finns era bilder fortfarande i tjänsten Finna? Finns samma bilder både i Finna och på Helsingforsbilder.fi?</p>
                    <p>Helsingfors stadsmuseums bilder finns fortfarande också i den nationella tjänsten Finna på adressen hkm.finna.fi. Utöver bilder kan man i Finna även bekanta sig med annat material med Helsingfors som tema, från plastpåsar till hårtorkar och från resebiljetter till konstverk. Man kan också söka information om byggnadernas historia i Helsingfors.</p>
                """
            }
    ]
}, {
    "name": u"Terms",
    "identifier": u"hkm_siteinfo_terms",
    "texts": [
            {
                "language": "fi",
                "title": u"Käyttöehdot",
                "content": u"""
                    <p>Aineistojen käyttöä koskevat seuraavat ehdot:</p>
                    <p><strong>Kuvat:</strong> Kuvat on lisensoitu Creative Commons CC BY 4.0 -lisenssillä. Jos haluat julkaista kuvan tai käyttää kuvaa julkisessa yhteydessä, noudata kuvan yhteydessä ilmoitettuja käyttöehtoja ja lisenssiä. Jos käytät kuvaa julkisesti, kuvaajan nimi (jos tiedossa) ja Helsingin kaupunginmuseo on mainittava. Kuvan käyttäjällä on vastuu tekijänoikeuksien ja yksityisyyden suojan kunnioittamisesta. Esimerkiksi henkilökuvien käyttö markkinoinnissa ja/tai mainonnassa on kielletty ilman kuvassa olevan henkilön suostumusta. Ota yhteys Helsingin kaupunginmuseoon, jos tieto kuvan käyttöoikeuksista puuttuu tai olet epävarma oikeudestasi käyttää kuvaa.</p>
                    <p><strong>Kuvailutiedot:</strong> Hakutulosten yhteydessä esitettäviä kuvailutietoja voi pääsääntöisesti käyttää vapaasti. Poikkeuksen muodostavat kuvailutietoihin sisältyvät henkilönimet, joiden julkaisemisessa käyttäjällä on vastuu yksityisyyden suojan kunnioittamisessa.</p>
                """
            },
        {
                "language": "en",
                "title": u"Terms of use",
                "content": u"""
                    <p>The following terms and conditions apply to the use of material</p>
                    <p><strong>Images:</strong> The photographs published by Helsinki City Museum in the Helsinkiphotos.fi service have been licensed with the “Creative Commons Attribution 4.0 International” or CC BY 4.0 license. In brief, it means that you may use and edit the photographs for any purpose as long as you credit the source of the photograph. The license does not remove the user’s responsibility. For instance, a person’s right to decide on the commercial use of their name, photograph or other identifiable part of their identity, privacy protection rights and moral rights may limit the use of the material.</p>
                    <p><strong>Metadata:</strong> The metadata and descriptions presented with the search results are as a rule freely available, with the the exception of personal information such as names. For instance, a person’s right to decide on the commercial use of their name or other identifiable part of their identity and privacy protection rights may limit the use of the material.</p>
                """
            }, {
                "language": "sv",
                "title": u"Användningsvillkor",
                "content": u"""
                    <p>För användningen av materialet gäller följande villkor:</p>
                    <p><strong>Bilder:</strong> Bilderna är licensierade med licensen Creative Commons Attribution 4.0 Internationell (CC BY 4.0). Om du vill publicera en bild eller använda bilden i offentligheten måste du följa de användningsvillkor som anges. Om du använder en bild offentligt, bör du nämna upphovsman och källa. Licensen ger eller ger dig inte alla de nödvändiga villkoren för ditt tänkta användande av verket. Till exempel, andra rättigheter som publicitet, integritetslagstiftning, eller ideella rättigheter kan begränsa hur du kan använda verket. Om informationen om användningsrättigheter saknas eller om du är osäker på om du har rätt att använda en bild, ska du kontakta Helsingfors stadsmusem.</p>
                    <p><strong>Metadata:</strong> I regel kan metadata i anknytning till sökresultat användas fritt. Andra rättigheter som publicitet eller integritetslagstiftning kan begränsa hur du kan använda metadatan.</p>
                """
            }
    ]
}, {
    "name": u"Privacy",
    "identifier": u"hkm_siteinfo_privacy",
    "texts": [
            {
                "language": "fi",
                "title": u"Asiakastietojen käsittely palvelussa Helsinkikuvia.fi",
                "content": u"""
                    <p class="privacy-bigtitle">Tietosuoja</p>
                    <p class="privacy-bigtitle">Helsinkikuvia.fi-asiakasrekisterin seloste</p>
                    <p class="privacy-smalltitle"><a href="https://www.hel.fi/static/liitteet-2019/Kaupunginkanslia/Rekisteriselosteet/Kuva/Kaupunginmuseon%20kuvapalvelurekisteri%20(Helsinkikuvia.fi).pdf">Linkki palvelun rekisteriselosteeseen</a></p>
                    <p class="privacy-smalltitle">Rekisterin yll&auml;pit&auml;j&auml;</p>
                    <p>Helsingin kaupunginmuseo</p>
                    <p>Aleksanterinkatu 16</p>
                    <p>&nbsp;</p>
                    <p>00170 HELSINKI</p>
                    <p>puh. 09 3103 6497</p>
                    <p>kuvakokoelmat@hel.fi</p>
                """
            },
        {
                "language": "en",
                "title": u"Handling customer data in Helsinkiphotos.fi",
                "content": u"""
                    <p class="privacy-bigtitle">Privacy and register details</p>
                    <p class="privacy-bigtitle">Description of the client register data file for Helsinkiphotos.fi service</p>
                    <p class="privacy-smalltitle"><a href="https://www.hel.fi/static/liitteet-2019/Kaupunginkanslia/Rekisteriselosteet/Kuva/City%20Museum%20image%20service%20data%20file%20(Helsinkiphotos.fi).pdf">Link to client register data file</a></p>
                    <p class="privacy-smalltitle">Data file controller</p>
                    <p>Helsinki City Museum</p>
                    <p>Aleksanterinkatu 16</p>
                    <p>P.O. Box 4300</p>
                    <p>00099 CITY OF HELSINKI</p>
                    <p>tel. 09 3103 6497</p>
                    <p>kuvakokoelmat@hel.fi</p>
                """
            },
        {
                "language": "sv",
                "title": u"Hantering av kunduppgifter i Helsingforsbilder.fi",
                "content": u"""
                    <p class="privacy-bigtitle">Dataskydd</p>
                    <p class="privacy-bigtitle">Registerbeskrivning f&ouml;r Helsingforsbilder.fi-tj&auml;nstens kundregister</p>
                    <p class="privacy-smalltitle"><a href="https://www.hel.fi/static/liitteet-2019/Kaupunginkanslia/Rekisteriselosteet/Kuva/Stadsmuseets%20bildtj%C3%A4nstregister%20(Helsinkikuvia.fi).pdf">L&auml;nken till registerbeskrivning</a></p>
                    <p class="privacy-smalltitle">Registeransvarig</p>
                    <p>Helsingfors stadsmuseum</p>
                    <p>Alexandersgatan 16</p>
                    <p>PB 4300</p>
                    <p>00999 HELSINGFORS STAD</p>
                    <p>+358 9 3103 6497</p>
                    <p>kuvakokoelmat@hel.fi</p>
                """
            }
    ]
}
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Collection.objects.filter(show_in_landing_page=True).count() == 0:
            self.stdout.write("Initializing first Collection and Record")
            admin = User.objects.filter(is_superuser=True).first()

            collection = Collection.objects.create(owner=admin, title="Oletuskokoelma", description="",
                                                   is_public=True, is_featured=True, show_in_landing_page=True)
            collection.save()

            record = Record.objects.create(creator=admin, collection=collection, record_id="hkm.HKMS000005:000000eg")
            record.save()

            self.stdout.write(self.style.SUCCESS("Initializing first Collection and Record - Done"))

        self.stdout.write("Initializing page contents (if necessary)")

        for page in pages:
            if PageContent.objects.filter(identifier=page["identifier"]).count() == 0:
                page_content = PageContent.objects.create(name=page["name"], identifier=page["identifier"])
                for text in page["texts"]:
                    page_content.set_current_language(text["language"])
                    page_content.title = text["title"]
                    page_content.content = text["content"]
                    page_content.save()

        self.stdout.write(self.style.SUCCESS("Initializing page contents (if necessary) - Done"))

        self.stdout.write("Initializing print products (if necessary)")

        if PrintProduct.objects.count() == 0:
            self.stdout.write("Initializing first print product")
            print_product = PrintProduct.objects.create(name=PrintProduct.PRODUCT_LAYOUTS_LIST[0][0], width="12",
                                                        height="21", paper_quality="Great", is_museum_only=False)
            print_product.save()

            self.stdout.write(self.style.SUCCESS("Initializing first print product - Done"))

        self.stdout.write(self.style.SUCCESS("Initializing print products (if necessary) - Done"))

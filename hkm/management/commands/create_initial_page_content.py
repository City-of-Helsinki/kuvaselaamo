from django.core.management.base import BaseCommand

from hkm.models.models import Collection, PageContent, PrintProduct, Record, User

pages = [
    {
        "name": "About",
        "identifier": "hkm_siteinfo_about",
        "texts": [
            {
                "language": "fi",
                "title": "Tietoa palvelusta",
                "content": """
                <p>Helsinkikuvia.fi-palvelu tarjoaa Helsinki-aiheisia valokuvia Helsingin kaupunginmuseon kokoelmista. Valokuvia voi ladata omalle laitteelleen korkearesoluutioisina eli painokelpoisina tai pienempinä, verkkoon sopivina kuvina.</p>
                <p>Kuvat on julkaistu CC BY 4.0 -lisenssillä. Se merkitsee, että kuvia voi käyttää haluamallaan tavalla maksutta, kunhan mainitsee kuvan yhteydessä kuvaajan nimen ja Helsingin kaupunginmuseon. Lisenssi sallii myös kuvien kaupallisen käytön, jos lainsäädäntö ei sitä estä. Esimerkiksi henkilökuvien käyttö markkinoinnissa ja mainonnassa on kielletty ilman kuvassa olevan henkilön suostumusta.</p>
                <p>Helsinkikuvia.fi-palvelussa voi hakea kuvia erilaisilla hakusanoilla, selata museon luomia kuva-albumeita eri aiheista tai luoda omia albumeita ja lisätä niihin suosikkikuviaan.</p>
                <p>Helsinkikuvia.fi-palvelussa on julkaistu Helsingin kaupunginmuseon valokuvakokoelman kaikki digitoidut kuvat, tällä hetkellä noin 65 000 kuvaa. Lisää tulee saataville sitä mukaa kuin kuvien digitointi etenee. Jos kaipaat kuvaa, jota ei löydy Helsinkikuvia.fi-palvelusta, ota yhteys Helsingin kaupunginmuseon Kuvaselaamoon.</p>
                <p>Helsinkikuvia.fi-palvelun kuvat ovat saatavilla myös kansallisessa Finna-palvelussa osoitteessa hkm.finna.fi. Valokuvien lisäksi Finnassa voi tutkia muutakin Helsinki-aiheista aineistoa muovipusseista hiustenkuivajiin ja matkalipuista taideteoksiin. Sieltä voi myös hakea tietoa helsinkiläisten rakennusten historiasta.</p>
            """,
            },
            {
                "language": "en",
                "title": "Information about the service",
                "content": """
                    <p>Helsinkiphotos.fi is an image service that provides a user-friendly way to access the Helsinki City Museum’s vast collection of photographs. At Helsinkiphotos.fi, anyone can browse, search and download detailed, high resolution photographs suitable for print materials or lower resolution images more suitable for web and social media use.</p>
                    <p>The photographs in the service are published under Creative Commons BY 4.0 license. In brief, CC BY means that you may use and edit the photographs for any purpose as long as you credit the source of the photograph, in this case Helsinki City Museum and the photographer. The photographs may be used commercially, with certain restrictions. For instance, a person’s right to decide on the commercial use of their name, photograph or other identifiable part of their identity, privacy protection rights and moral rights may limit the use of the material.</p>
                    <p>The Helsinkiphotos.fi service also allows users to conduct Finnish-language searches, browse curated photo albums or create their own albums by logging into the service.</p>
                    <p>Currently, the service has approximately 65,000 digitized photographs. More images are being digitized and added to the system constantly. If you need a digital image that is not currently found in the Helsinkiphotos.fi service, please contact the museum’s Picture Browsery.</p>
                    <p>The photographs of the Helsinki City Museum collection are still available in the national Finna service at hkm.finna.fi. In addition to photographs, you can also browse other material related to Helsinki in Finna, everything from plastic bags to hairdryers and bus tickets to works of art. You can also search the history of the buildings of Helsinki.</p>
            """,
            },
            {
                "language": "sv",
                "title": "Information om tjänsten",
                "content": """
                    <p>Helsingfors stadsmuseums foton från olika tidsperioder med Helsingfors som tema kan användas fritt i och med att tjänsten Helsingforsbilder.fi öppnas. Bland fotona finns bland annat alla Signe Branders älskade bilder på Helsingfors för hundra år sedan samt Simo och Eeva Ristas omfattande och betydelsefulla samling om en föränderlig stad på 1970-talet.</p>
                    <p>Museet har bilder ända från 1840-talet, så det är till exempel möjligt att gå igenom spårvagnarnas historia i bilder ända från 1800-talet till 2000-talet. Nu presenteras cirka 65 000 bilder för allmänheten, och fler blir tillgängliga i och med att digitaliseringen framskrider. Endast en bråkdel av bilderna i museets samlingar är digitaliserade.</p>
                    <p>Museet lämnar ut bilderna med CC BY 4.0 licens. Man kan ladda ner bilder och använda dem fritt och utan avgift på nätet och i olika applikationer, och även till exempel i böcker, presentartiklar eller tryckta på tapet, bara man anger fotografens namn och Helsingfors stadsmuseum i samband med bilden. Licensen tillåter kommersiell användning av bilderna om lagstiftningen inte hindrar detta. Till exempel är det förbjudet att använda bilder på personer i marknadsföring och reklam utan tillåtelse av personer som är med på bilden.</p>
                    <p>Tjänsten omfattar i praktiken alla bilder som stadsmuseet har digitaliserat, dvs. omvandlat till digital form. Om du behöver en digital version av en bild som inte har digitaliserats, kan du beställa den via stadsmuseets Bildapotek. För digitaliseringar uppbärs en avgift enligt museets prislista. Den bild som du beställt publiceras oftast med en liten fördröjning i tjänsten Helsingforsbilder.fi och är efter det tillgänglig för alla.</p>
                    <p>Helsingfors stadsmuseums bilder finns fortfarande också i den nationella tjänsten Finna på adressen hkm.finna.fi. Utöver bilder kan man i Finna även bekanta sig med annat material med Helsingfors som tema, från plastpåsar till hårtorkar och från resebiljetter till konstverk. Man kan också söka information om byggnadernas historia i Helsingfors.</p>
            """,
            },
        ],
    },
    {
        "name": "QA",
        "identifier": "hkm_siteinfo_QA",
        "texts": [
            {
                "language": "fi",
                "title": "Kysymyksiä ja vastauksia",
                "content": """
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
                """,
            },
            {
                "language": "en",
                "title": "Questions and answers",
                "content": """
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
                """,
            },
            {
                "language": "sv",
                "title": "Frågor och svar",
                "content": """
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
                """,
            },
        ],
    },
    {
        "name": "Terms",
        "identifier": "hkm_siteinfo_terms",
        "texts": [
            {
                "language": "fi",
                "title": "Käyttöehdot",
                "content": """
                    <p>Aineistojen käyttöä koskevat seuraavat ehdot:</p>
                    <p><strong>Kuvat:</strong> Kuvat on lisensoitu Creative Commons CC BY 4.0 -lisenssillä. Jos haluat julkaista kuvan tai käyttää kuvaa julkisessa yhteydessä, noudata kuvan yhteydessä ilmoitettuja käyttöehtoja ja lisenssiä. Jos käytät kuvaa julkisesti, kuvaajan nimi (jos tiedossa) ja Helsingin kaupunginmuseo on mainittava. Kuvan käyttäjällä on vastuu tekijänoikeuksien ja yksityisyyden suojan kunnioittamisesta. Esimerkiksi henkilökuvien käyttö markkinoinnissa ja/tai mainonnassa on kielletty ilman kuvassa olevan henkilön suostumusta. Ota yhteys Helsingin kaupunginmuseoon, jos tieto kuvan käyttöoikeuksista puuttuu tai olet epävarma oikeudestasi käyttää kuvaa.</p>
                    <p><strong>Kuvailutiedot:</strong> Hakutulosten yhteydessä esitettäviä kuvailutietoja voi pääsääntöisesti käyttää vapaasti. Poikkeuksen muodostavat kuvailutietoihin sisältyvät henkilönimet, joiden julkaisemisessa käyttäjällä on vastuu yksityisyyden suojan kunnioittamisessa.</p>
                """,
            },
            {
                "language": "en",
                "title": "Terms of use",
                "content": """
                    <p>The following terms and conditions apply to the use of material</p>
                    <p><strong>Images:</strong> The photographs published by Helsinki City Museum in the Helsinkiphotos.fi service have been licensed with the “Creative Commons Attribution 4.0 International” or CC BY 4.0 license. In brief, it means that you may use and edit the photographs for any purpose as long as you credit the source of the photograph. The license does not remove the user’s responsibility. For instance, a person’s right to decide on the commercial use of their name, photograph or other identifiable part of their identity, privacy protection rights and moral rights may limit the use of the material.</p>
                    <p><strong>Metadata:</strong> The metadata and descriptions presented with the search results are as a rule freely available, with the the exception of personal information such as names. For instance, a person’s right to decide on the commercial use of their name or other identifiable part of their identity and privacy protection rights may limit the use of the material.</p>
                """,
            },
            {
                "language": "sv",
                "title": "Användningsvillkor",
                "content": """
                    <p>För användningen av materialet gäller följande villkor:</p>
                    <p><strong>Bilder:</strong> Bilderna är licensierade med licensen Creative Commons Attribution 4.0 Internationell (CC BY 4.0). Om du vill publicera en bild eller använda bilden i offentligheten måste du följa de användningsvillkor som anges. Om du använder en bild offentligt, bör du nämna upphovsman och källa. Licensen ger eller ger dig inte alla de nödvändiga villkoren för ditt tänkta användande av verket. Till exempel, andra rättigheter som publicitet, integritetslagstiftning, eller ideella rättigheter kan begränsa hur du kan använda verket. Om informationen om användningsrättigheter saknas eller om du är osäker på om du har rätt att använda en bild, ska du kontakta Helsingfors stadsmusem.</p>
                    <p><strong>Metadata:</strong> I regel kan metadata i anknytning till sökresultat användas fritt. Andra rättigheter som publicitet eller integritetslagstiftning kan begränsa hur du kan använda metadatan.</p>
                """,
            },
        ],
    },
    {
        "name": "Privacy",
        "identifier": "hkm_siteinfo_privacy",
        "texts": [
            {
                "language": "fi",
                "title": "Asiakastietojen käsittely palvelussa Helsinkikuvia.fi",
                "content": """
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
                """,
            },
            {
                "language": "en",
                "title": "Handling customer data in Helsinkiphotos.fi",
                "content": """
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
                """,
            },
            {
                "language": "sv",
                "title": "Hantering av kunduppgifter i Helsingforsbilder.fi",
                "content": """
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
                """,
            },
        ],
    },
    {
        "name": "Saavutettavuusseloste",
        "identifier": "hkm_siteinfo_accessibility",
        "texts": [
            {
                "language": "fi",
                "title": "Saavutettavuusseloste",
                "content": """
                    <h1>Saavutettavuusseloste</h1>

                    <p>Tämä saavutettavuusseloste koskee Helsingin kaupungin "Helsinkikuvia"-verkkosivustoa. Sivuston osoite on https://www.helsinkikuvia.fi.</p>

                    <h2>Sivustoa koskevat lain säädökset</h2>

                    <p>Tämä sivusto on julkaistu aiemmin kuin 23.9.2018. Sivuston tulee täyttää lain edellyttämät saavutettavuuden vaatimukset 23.9.2020 päättyvän siirtymäajan jälkeen.</p>

                    <h2>Kaupungin tavoite</h2>

                    <p>Digitaalisten palveluiden saavutettavuudessa Helsingin tavoitteena on pyrkiä vähintään WCAG ohjeiston mukaiseen AA- tai sitä parempaan tasoon, mikäli se on kohtuudella mahdollista.</p>

                    <h1>Vaatimustenmukaisuustilanne</h1>

                    <p>Tämä verkkosivusto täyttää lain asettamat kriittiset saavutettavuusvaatimukset WCAG v2.1 -tason AA mukaisesti seuraavin havaituin puuttein.</p>

                    <h2>Ei-saavutettava sisältö</h2>

                    <p>Jäljempänä mainittu sisältö ei vielä täytä kaikkia lain asettamia saavutettavuusvaatimuksia.</p>

                    <h3>Havaitut puutteet</h3>

                    <ol>
                        <li>
                        <p>Puutteellinen kielimääritys</p>

                        <p>Kielivalikon kieliltä puuttuu kielimääritys, joka aiheuttaa tilanteen, jossa ruudunlukija lausuu kielet väärin. (WCAG2.1: 3.1.2 Osien kieli)</p>

                        <p>Korjaustapa: Kielivalikon kielille ja sivuston hakukentälle tulee asettaa kieltä vastaava kielimääritys.</p>
                        </li>
                        <li>
                        <p>Valokuva-albumien selaaminen englanninkielisellä sivustolla on haastavaa ruudunlukuohjelman käyttäjälle</p>

                        <p>Sivuston valokuva-albumien ja kuvien tekstit ovat ainoastaan suomeksi, vaikka sivusto on muuten englanniksi. Ruudunlukuohjelma lausuu sisällön väärin. (WCAG2.1: 3.1.2 Osien kieli)</p>
                        </li>
                        <li>
                        <p>Sivun title-elementtiä ei ole yksilöity kaikille sivuille</p>
                        </li>
                    </ol>

                    <p>Korjaustapa: Valokuva-albumien nimet ja muut kuvien kuvaustekstit tulee joko</p>

                    <p>kääntää sen kielen mukaiseksi, minkä käyttäjä on valinnut sivustolle tai</p>

                    <p>vaihtoehtoisesti valokuva-albumisivun kielimääritys tulee asettaa suomenkielisten</p>

                    <p>tekstien osalta aina suomeksi.</p>

                    <p>Sivustolla oleva title-elementin nimiöinti ei aina päivity, kun uusi sivu ladataan. (WCAG2.1: 2.4.2 Sivuotsikot)</p>

                    <p>Korjaustapa: Varmistetaan, että sivuston jokaiselle sivulle on asetettu sitä kuvaava title-elementti.</p>

                    <ol>
                        <li>
                        <p>Epäloogista otsikointia</p>

                        <p>Sivuston otsikointi ei etene kaikkialla loogisesti. (WCAG2.1: 1.3.1 Informaatio ja suhteet)</p>

                        <p>Korjaustapa: Varmistetaan, että sivuston otsikointi etenee kaikkialla johdonmukaisesti. Otsikointi aloitetaan h1-tason otsikolla.</p>
                        </li>
                        <li>
                        <p>Sivusto sisältää avustavalle teknologialle nimeämättömiä sekä puutteellisesti kuvattuja painikkeita</p>

                        <p>Sivustolla on painikkeita, joita ei ole nimetty lainkaan avustavalle teknologialle, esimerkiksi ruudunlukuohjelmalle. (WCAG2.1: 4.1.2 Nimi, rooli, arvo)</p>

                        <p>Korjaustapa: Varmistetaan, että kaikki sivuston painikkeet on nimetty teknisesti ruudunlukuohjelmia ja muita avustavan teknologian ratkaisuja varten.</p>
                        </li>
                        <li>
                        <p>Heikkoja kontrasteja</p>
                        </li>
                    </ol>

                    <h3>Puutteiden korjaus</h3>

                    <p>Sivustolla on käytetty tekstin värejä, joiden kontrasti suhteessa pohjaväriin ei ole riittävä. (WCAG2: 1.4.3 Kontrasti (minimi))</p>

                    <p>Korjaustapa: Tekstin ja sen taustan kontrastin suhde tulisi olla vähintään 4,5:1 ja suurempaa tekstikokoa käytettäessä 3:1.</p>

                    <p>Havaitut puutteet pyritään korjaamaan siten, että sivuston käyttö ruudunlukijalla sekä avustavilla tekniikoilla, on mahdollista. Sivuston otsikointia tarkistetaan, sekä title-elementit määritetään kaikille elementeille. Sivuston ulkoasulle ollaan tekemässä uudistusta, missä värikontrastit on tarkastettu siten, että no ovat vähintään 4,5:1. Korjaus pyritään suorittamaan mahdollisimman pian järjestelmäpäivityksen yhteydessä 2020 loppuun mennessä.</p>

                    <h2>Tiedon saanti saavutettavassa muodossa</h2>

                    <p>Mainituista puutteista johtuen saavuttamatta jäävää sisältöä voi pyytää tämän sivuston ylläpitäjältä.</p>

                    <p>Helsingin kaupunki, Kulttuuri ja vapaa-aika Ratkaisutoimisto<br />
                    kuva-accessibility@hel.fi</p>

                    <h2>Saavutettavuusselosteen laatiminen</h2>

                    <p>Tämä seloste on laadittu 18.03.2020 ja päivitetty 4.9.2020</p>

                    <h2>Saavutettavuuden arviointi</h2>

                    <p>Saavutettavuuden arvioinnissa on noudatettu Helsingin kaupungin työohjetta ja menetelmiä, jotka pyrkivät varmistamaan sivuston saavutettavuuden kaikissa työvaiheissa.</p>

                    <p>Saavutettavuus on tarkistettu ulkopuolisen asiantuntijan suorittamana auditointina sekä itsearviona.</p>

                    <p>Saavutettavuus on tarkistettu käyttäen ohjelmallista saavutettavuustarkistusta sekä sivuston ja sisällön manuaalista tarkistusta. Ohjelmallinen tarkistus on suoritettu käyttäen Siteimproven saavutettavuuden automaattista testaustyökalua ja selainlaajennusta.</p>

                    <p>Ulkopuolisen asiantuntija-auditoinnin on suorittanut Helsingin kaupungin palvelukeskus-liikelaitos.</p>

                    <h2>Saavutettavuusselosteen päivittäminen</h2>

                    <p>Sivuston saavutettavuudesta huolehditaan jatkuvalla valvonnalla tekniikan tai sisällön muuttuessa, sekä määräajoin suoritettavalla tarkistuksella. Tätä selostetta päivitetään sivuston muutosten ja saavutettavuuden tarkistusten yhteydessä.</p>

                    <h2>Palaute ja yhteystiedot</h2>

                    <p>Sivuston saavutettavuudesta vastaa Helsingin kaupunki, Kulttuuri ja vapaa-aika Ratkaisutoimisto</p>

                    <h2>Ilmoittaminen ei-saavutettavasta sisällöstä</h2>

                    <p>Mikäli käyttäjä kokee, etteivät saavutettavuuden vaatimukset kuitenkaan täyty, voi tästä tehdä ilmoituksen sähköpostilla helsinki.palaute@hel.fi tai palautelomakkeella www.hel.fi/palaute.</p>

                    <h2>Tietojen pyytäminen saavutettavassa muodossa</h2>

                    <p>Mikäli käyttäjä ei koe saavansa sivuston sisältöä saavutettavassa muodossa, voi käyttäjä pyytää näitä tietoja sähköpostilla helsinki.palaute@hel.fi tai palautelomakkeella www.hel.fi/palaute. Tiedusteluun pyritään vastaamaan kohtuullisessa ajassa.</p>

                    <h2>Saavutettavuuden oikeussuoja, Täytäntöönpanomenettely</h2>

                    <p>Mikäli henkilö kokee, ettei hänen ilmoitukseensa tai tiedusteluunsa ole vastattu tai vastaus ei ole tyydyttävä, voi asiasta tehdä ilmoituksen Etelä-Suomen aluehallintovirastoon. Etelä-Suomen aluehallintoviraston sivulla kerrotaan tarkasti, miten asia käsitellään.</p>

                    <p><strong>Etelä-Suomen aluehallintovirasto</strong><br>
                    Saavutettavuuden valvonnan yksikko<br>
                    www.saavutettavuusvaatimukset.fi<br>
                    saavutettavuus@avi.fi
                    </p>

                    <p>Puhelinvaihde: 0295 016 000 Avoinna: ma-pe klo 8.00 &ndash; 16.15</p>

                    <p>Helsingin kaupunki ja saavutettavuus</p>

                    <p>Helsingin kaupungin tavoitteena on olla kaikille esteetön ja saavutettava kaupunki. Kaupungin tavoitteena on, että Helsingissä on kaikkien kaupunkilaisten mahdollisimman helppo liikkua ja toimia ja että kaikki sisältö ja palvelut olisivat kaikkien saavutettavissa.</p>

                    <p>Kaupunki edistää digitaalisten palveluiden saavutettavuutta yhdenmukaistamalla julkaisutyötä ja järjestämällä saavutettavuuteen keskittyvää koulutusta henkilökunnalleen.</p>

                    <p>Sivustojen saavutettavuuden tasoa seurataan jatkuvasti sivustoja ylläpidettäessä. Havaittuihin puutteisiin reagoidaan välittömästi. Tarvittavat muutokset pyritään suorittamaan mahdollisimman nopeasti.</p>

                    <h2>Vammaiset ja avustavien teknologioiden käyttäjät</h2>

                    <p>Kaupunki tarjoaa neuvontaa ja tukea vammaisille ja avustavien teknologioiden käyttäjille. Tukea on saatavilla kaupungin sivuilla ilmoitetuista neuvontasivuilta sekä puhelinneuvonnasta.</p>

                    <h2>Saavutettavuusselosteen hyväksyntä</h2>

                    <p>Tämän selosteen on hyväksynyt 4.9.2020</p>

                    <p>Kulttuurin ja Vapaa-aja toimiala Helsingin kaupunki</p>
                """,
            },
            {
                "language": "sv",
                "title": "Tillgänglighetsutlåtande",
                "content": """
                    <h1>Tillg&auml;nglighetsutl&aring;tande</h1>

                    <p>Detta tillg&auml;nglighetsutl&aring;tande g&auml;ller Helsingfors stads webbplats &rdquo;Helsinkikuvia&rdquo;. Webbplatsens adress &auml;r http://www.helsinkikuvia.fi</p>

                    <h2>Lagbest&auml;mmelser som g&auml;ller webbplatsen</h2>

                    <p>Denna webbplats har offentliggjorts tidigare &auml;n 23.9.2018. Webbplatsen ska uppfylla lagens krav p&aring; tillg&auml;nglighet efter &ouml;verg&aring;ngstiden som slutar 23.9.2020.</p>

                    <h2>Stadens m&aring;l</h2>

                    <p>N&auml;r det g&auml;ller tillg&auml;nglighet till digitala tj&auml;nster har Helsingfors stad som m&aring;l att uppn&aring; minst niv&aring; AA eller b&auml;ttre enligt WCAG-anvisningarna, om det &auml;r rimligt.</p>

                    <h2>Fullg&ouml;randestatus</h2>

                    <p>Denna webbplats uppfyller lagstadgade kritiska tillg&auml;nglighetskrav enligt niv&aring; AA i WCAG v2.1 med f&ouml;ljande observerade brister.</p>

                    <h2>Icke tillg&auml;ngligt inneh&aring;ll</h2>

                    <p>Nedan angivet inneh&aring;ll uppfyller &auml;nnu ej alla lagstadgade tillg&auml;nglighetskrav.</p>

                    <h3>Observerade brister</h3>

                    <p>1. Bristande spr&aring;kinst&auml;llning</p>

                    <p>Spr&aring;ken i spr&aring;kmenyn saknar spr&aring;kinst&auml;llningar med f&ouml;ljden att sk&auml;rml&auml;sare l&auml;ser spr&aring;ken fel. (WCAG2.1: 3.1.2 Spr&aring;k i olika avsnitt)</p>

                    <p>Korrigeringss&auml;tt: Spr&aring;ken i spr&aring;kmenyn samt s&ouml;kf&auml;lten p&aring; sidorna ska f&ouml;rses med spr&aring;kinst&auml;llningar som motsvarar spr&aring;ket.</p>

                    <p>2. Bl&auml;ddring i fotoalbum p&aring; de engelska sidorna st&auml;ller problem f&ouml;r anv&auml;ndare av sk&auml;rml&auml;sningsprogram.</p>

                    <p>Texter i fotoalbum och p&aring; bilder finns endast p&aring; finska fast sidan i &ouml;vrigt &auml;r p&aring; engelska. Sk&auml;rml&auml;sningsprogrammet uttrycker inneh&aring;llet fel. (WCAG2.1: 3.1.2 Spr&aring;k i olika avsnitt)</p>

                    <p>Korrigeringss&auml;tt: Namn p&aring; fotoalbum samt &ouml;vriga beskrivande texter f&ouml;r bilder ska antingen &ouml;vers&auml;ttas till spr&aring;ket som anv&auml;ndaren valt f&ouml;r sidorna eller annars ska spr&aring;kinst&auml;llningen f&ouml;r sidan med fotoalbum visavi texter p&aring; finska alltid st&auml;llas f&ouml;r finska.</p>

                    <p>3. Sidans titleelement har inte specifierats f&ouml;r alla sidor</p>

                    <p>Etiketten f&ouml;r titleelement p&aring; sidan uppdateras inte alltid n&auml;r en ny sida laddas. (WCAG2.1: 2.4.2 Sidrubriker)</p>

                    <p>Korrigeringss&auml;tt: Det ska kontrolleras att det f&ouml;r varje sida p&aring; webbplatsen har speciferats ett titleelement som beskriver sidan i fr&aring;ga.</p>

                    <p>4. Ologiska rubriker</p>

                    <p>Rubrikerna p&aring; sidorna l&ouml;per inte logiskt &ouml;verallt. (WCAG2.1: 1.3.1 Information och relationer)</p>

                    <p>Korrigeringss&auml;tt: Det ska kontrolleras att rubrikerna p&aring; sidorna l&ouml;per konsekvent &ouml;verallt. Rubrikerna b&ouml;rjar med en rubrik p&aring; h1-niv&aring;.</p>

                    <p>5. Sidorna har knappar som b&aring;de saknar specifikation f&ouml;r assisterande teknologi och &auml;r bristf&auml;lligt beskrivna.</p>

                    <p>Sidorna har knappar som inte alls har specifierats f&ouml;r assisterande teknologi, s&aring;som sk&auml;rml&auml;sningsprogram. (WCAG2.1: 4.1.2 Namn, roll, v&auml;rde)</p>

                    <p>Korrigeringss&auml;tt: Det ska kontrolleras att knapparna p&aring; alla sidor tekniskt har specifierats f&ouml;r sk&auml;rml&auml;sningsprogram och &ouml;vriga l&ouml;sningar med assisterande teknologi.</p>

                    <p>6. D&aring;liga kontraster</p>

                    <p>Textf&auml;rger med otillr&auml;cklig kontrast i relation till bakgrundsf&auml;rgen har anv&auml;nts p&aring; sidorna. (WCAG2: 1.4.3 Kontrast (minimum))</p>

                    <p>Korrigeringss&auml;tt: F&ouml;rh&aring;llandet mellan texten och bakgrunden ska vara minst 4,5:1, och f&ouml;r st&ouml;rre textstorlek 3:1.</p>

                    <h3>&nbsp;</h3>

                    <h3>&nbsp;</h3>

                    <h3>R&auml;ttning av brister</h3>

                    <p>Vi str&auml;var efter att &aring;tg&auml;rda observerade brister s&aring; att det blir m&ouml;jligt att anv&auml;nda webbplatsen med sk&auml;rml&auml;sare och assisterande teknologi. Rubrikerna p&aring; sidorna ska kontrolleras och titlelement definieras f&ouml;r alla element. Sidornas utseende kommer att f&ouml;rnyas och d&aring; kontrolleras f&auml;rgkontrasterna s&aring; att f&ouml;rh&aring;llandet &auml;r minst 4,5:1. Vi str&auml;var efter att g&ouml;ra korrigeringen s&aring; snart som m&ouml;jligt vid systemuppdateringar f&ouml;re slutet av 2020.</p>

                    <h3>&nbsp;</h3>

                    <h3>F&aring; uppgifter i tillg&auml;nglig form</h3>

                    <p>Inneh&aring;ll som inte kan n&aring;s p&aring; grund av n&auml;mnda brister kan beg&auml;ras fr&aring;n uppr&auml;tth&aring;llaren av denna webbplats.</p>

                    <p>Kultur- och fritidssektorn, Helsingfors stad</p>

                    <p>ville.sjofarare@hel.fi</p>

                    <p>&nbsp;</p>

                    <h2>Utarbetande av tillg&auml;nglighetsutl&aring;tande</h2>

                    <p>Detta utl&aring;tande har utarbetats 18.3.2020 och &auml;r senast uppdaterad 4.9.2020.</p>

                    <h3>Bed&ouml;mning av tillg&auml;nglighet</h3>

                    <p>Vid bed&ouml;mning av tillg&auml;nglighet har f&ouml;ljts Helsingfors stads arbetsanvisning och metoder som siktar till att s&auml;kerst&auml;lla webbplatsens tillg&auml;nglighet i alla arbetsfaser.</p>

                    <p>Tillg&auml;ngligheten &auml;r kontrollerad genom revision av en extern expert samt som egen bed&ouml;mning.</p>

                    <p>Tillg&auml;ngligheten &auml;r kontrollerad med hj&auml;lp av automatisk tillg&auml;nglighetskontroll samt manuell kontroll av webbplatsen och inneh&aring;llet. Automatiska kontroller har utf&ouml;rts med anv&auml;ndning av bed&ouml;mningsverktyget Lighthouse i webbl&auml;saren Google Chrome, webbl&auml;sartill&auml;gget axe fr&aring;n Deque Systems Inc. samt webbl&auml;sartill&auml;gget Siteimprove.</p>

                    <p>Missf&ouml;rh&aring;llanden som bed&ouml;mningsverktygen rapporterat har kontrollerats och vid behov korrigerats.</p>

                    <p>Den externa expertrevisionen har utf&ouml;rts av Servicecentralen Helsinki.</p>

                    <h3>Uppdatering av tillg&auml;nglighetsutl&aring;tande</h3>

                    <p>Webbplatsens tillg&auml;nglighet kontrolleras genom kontinuerlig tillsyn n&auml;r tekniken eller inneh&aring;llet f&ouml;r&auml;ndras, samt granskning med regelbundna intervall. Detta utl&aring;tande uppdateras i samband med &auml;ndringar av webbplatsen samt granskningar av tillg&auml;nglighet.</p>

                    <h2>&Aring;terkoppling och kontaktuppgifter</h2>

                    <p>F&ouml;r webbplatsens tillg&auml;nglighet svarar</p>

                    <p>Kultur- och fritidssektorn, Helsingfors stad</p>

                    <p>ville.sjofarare@hel.fi</p>

                    <h3>&nbsp;</h3>

                    <h3>Anm&auml;lan om ej tillg&auml;ngligt inneh&aring;ll</h3>

                    <p>Om anv&auml;ndaren upplever att kraven p&aring; tillg&auml;nglighet &auml;nd&aring; inte uppfylls kan detta anm&auml;las per e-post <a href="mailto:helsinki.palaute@hel.fi">helsinki.palaute@hel.fi</a> eller med responsformul&auml;r p&aring; <a href="https://www.hel.fi/helsinki/sv/stad-och-forvaltning/delta/feedback">www.hel.fi/palaute</a> .</p>

                    <h3>Beg&auml;ran om uppgifter i tillg&auml;nglig form</h3>

                    <p>Om anv&auml;ndaren inte upplever sig f&aring; webbplatsens inneh&aring;ll i tillg&auml;nglig form, kan anv&auml;ndaren beg&auml;ra dessa uppgifter per e-post <a href="mailto:helsinki.palaute@hel.fi">helsinki.palaute@hel.fi</a> eller med responsformul&auml;r p&aring; <a href="https://www.hel.fi/helsinki/sv/stad-och-forvaltning/delta/feedback">www.hel.fi/palaute</a> . Str&auml;van &auml;r att svara p&aring; f&ouml;rfr&aring;gan inom rimlig tid.</p>

                    <h2>R&auml;ttsskydd f&ouml;r tillg&auml;nglighet, Verkst&auml;llighetsf&ouml;rfarande</h2>

                    <p>Om en person upplever att svar inte har erh&aring;llits p&aring; hans eller hennes anm&auml;lan eller f&ouml;rfr&aring;gan, eller om svaret inte &auml;r tillfredsst&auml;llande, kan saken anm&auml;las till regionf&ouml;rvaltningsverket i S&ouml;dra Finland. P&aring; webbplatsen f&ouml;r regionf&ouml;rvaltningsverket i S&ouml;dra Finland finns detaljerad information om hur saken behandlas.</p>

                    <p>Regionf&ouml;rvaltningsverket i S&ouml;dra Finland<br />
                    Enheten f&ouml;r tillg&auml;nglighetstillsyn<br />
                    <a href="https://www.xn--tillgnglighetskrav-ptb.fi/">https://www.xn--tillgnglighetskrav-ptb.fi/</a><br />
                    <a href="mailto:webbtillganglighet@rfv.fi">webbtillganglighet@rfv.fi</a><br />
                    Telefonv&auml;xel 0295 016&nbsp;000<br />
                    &Ouml;ppet: m&aring;&ndash;fr kl. 8.00&ndash;16.15</p>

                    <h2>Helsingfors stad och tillg&auml;nglighet</h2>

                    <p>Helsingfors stad har som m&aring;l att vara en tillg&auml;nglig stad f&ouml;r alla. Stadens m&aring;l &auml;r att det ska vara s&aring; l&auml;tt som m&ouml;jligt f&ouml;r alla stadsbor att r&ouml;ra sig och verka i Helsingfors och att alla inneh&aring;ll och tj&auml;nster ska vara tillg&auml;ngliga f&ouml;r alla.</p>

                    <p>Staden fr&auml;mjar tillg&auml;ngligheten f&ouml;r digitala tj&auml;nster genom att f&ouml;renhetliga publiceringsarbetet och ordna utbildning om tillg&auml;nglighet f&ouml;r sin personal.</p>

                    <p>Tillg&auml;nglighetsniv&aring;n f&ouml;r webbplatser f&ouml;ljs upp kontinuerligt n&auml;r webbplatserna underh&aring;lls. Observerade brister hanteras omedelbart. V&aring;r str&auml;van &auml;r att genomf&ouml;ra n&ouml;dv&auml;ndiga &auml;ndringar s&aring; snabbt som m&ouml;jligt.</p>

                    <h3>Handikappade och hj&auml;lpmedelsanv&auml;ndare</h3>

                    <p>Staden erbjuder r&aring;dgivning och st&ouml;d f&ouml;r handikappade och hj&auml;lpmedelsanv&auml;ndare. St&ouml;d kan f&aring;s p&aring; de r&aring;dgivningssidor som anges p&aring; stadens sidor och p&aring; telefonr&aring;dgivningen.</p>

                    <h2>Godk&auml;nnande av tillg&auml;nglighetsutl&aring;tande</h2>

                    <p>Detta utl&aring;tande har godk&auml;nts 4.9.2020.</p>

                    <p>&nbsp;</p>

                    <p>Kultur- och fritidssektorn</p>

                    <p>Helsingfors stad</p>

                    <p>&nbsp;</p>
                """,
            },
            {
                "language": "en",
                "title": "Accessibility statement",
                "content": """
                <h1>Accessibility statement</h1>

                <p>This accessibility statement applies to the website &rdquo;Helsinkikuvia&rdquo; of the City of Helsinki. The site address is http://www.helsinkikuvia.fi</p>

                <h2>Statutory provisions applicable to the website</h2>

                <p>This website was published prior to 23 September 2018. The website must fulfil the statutory accessibility requirements after the transitional period ending on 23 September 2020.</p>

                <h2>The objective of the city</h2>

                <p>As regards the accessibility of digital services, Helsinki aims to reach at least Level AA or above as set forth in the WCAG guidelines in so far as is reasonably practical.</p>

                <h2>Compliance status</h2>

                <p>This website meets the statutory critical accessibility requirements in accordance with Level AA of the WCAG v2.1 with the following deficiencies.</p>

                <h2>Non-accessible content</h2>

                <p>The content mentioned below does not yet meet all of the statutory accessibility requirements.</p>

                <h3>Deficiencies found</h3>

                <p>1. Insufficient language determination</p>

                <p>The languages in the language menu are missing language determinations, which causes the screen reader to pronounce the words incorrectly. (WCAG2.1: 3.1.2 Language of Parts)</p>

                <p>Corrective measures: The languages of the language menu and the search field of the site must have a corresponding language determination.</p>

                <p>2. Browsing the photo albums on the English version of the site is challenging for users of screen readers.</p>

                <p>The texts on the photo albums and photos on the site are only in Finnish, even though the site is otherwise in English. The screen reader pronounces the content incorrectly. (WCAG2.1: 3.1.2 Language of Parts)</p>

                <p>Corrective measures: The names of the photo albums and the descriptive texts of the other photos must be translated according to the language the user has selected for the website. Alternatively, the language determined for the photo album page should always be Finnish when the texts are in Finnish.</p>

                <p>3. The site&rsquo;s title element has not been identified for all pages.</p>

                <p>The label of the title element is not always updated when a new page is loaded. (WCAG2.1: 2.4.2 Page Titled)</p>

                <p>Corrective measures: Ensuring that each page on the site has a descriptive title element.</p>

                <p>4. Illogical titles</p>

                <p>The titles of the site are not proceeding logically in all parts. (WCAG2.1: 1.3.1 Info and Relationships)</p>

                <p>Corrective measures: Ensuring that the site&rsquo;s titles proceed consistently everywhere. The titles should start with an h1 level title.</p>

                <p>5. The site has buttons that are unnamed for assistive technology and insufficiently described.</p>

                <p>The site has buttons that have not been named at all for assistive technology, such as screen readers. (WCAG2.1: 4.1.2 Name, Role, Value)</p>

                <p>Corrective measures: Ensuring that all buttons on the site have been named technically for screen readers and other assistive solutions.</p>

                <p>6. Weak contrast</p>

                <p>The site has text colours in which the contrast is insufficient in relation to the background colour. (WCAG2: 1.4.3 Contrast (Minimum))</p>

                <p>Corrective measures: The contrast ratio between the text and its background should be at least 4.5:1, and 3:1 when using large-scale text.</p>

                <h3>&nbsp;</h3>

                <h3>Correcting deficiencies</h3>

                <p>The aim is to correct any shortcomings detected by ensuring that accessing the website with screen readers and assistive technologies is possible. The titles of the site will be revised and title elements will be determined for all elements. The website&rsquo;s layout will undergo changes where the contrasts will have been revised so that they are at least at 4.5:1. The changes will be made as soon as possible in connection with a system update by the end of 2020.</p>

                <h3>&nbsp;</h3>

                <h3>Obtaining information in an accessible form</h3>

                <p>Due to these deficiencies, you can request the non-accessible content from the administrator of this website.</p>

                <p>Culture and Leisure Division, City of Helsinki</p>

                <p>kuva-accessibility@hel.fi</p>

                <p>&nbsp;</p>

                <h2>Preparing an accessibility statement</h2>

                <p>This statement was prepared on 18/3/2020 and was last updated on 4/9/2020.</p>

                <h3>Assessment of accessibility</h3>

                <p>The working instruction and procedures of the City of Helsinki were followed when evaluating the accessibility of the site, with the aim of ensuring that websites are accessible in all stages of the work process.</p>

                <p>Accessibility was evaluated by means of an audit by a third-party expert as well as self-evaluation.</p>

                <p>Accessibility was evaluated using a programmatic accessibility auditing tool as well as by manually reviewing the site and content. Programmatic evaluations were carried out using the Siteimprove browser extension.</p>

                <p>Defects reported by the evaluation tools were reviewed and, if necessary, corrected.</p>

                <p>The third-party expert audit was carried out by Service Centre Helsinki.</p>

                <h3>Updating the accessibility statement</h3>

                <p>When website technology or content changes, its accessibility must be ensured through constant monitoring and periodic checks. This statement will be updated in conjunction with website changes and accessibility evaluations.</p>

                <h2>Feedback and contact information</h2>

                <p>The entity responsible for site accessibility:</p>

                <p>Culture and Leisure Division, City of Helsinki</p>

                <p>kuva-accessibility@hel.fi</p>

                <p>&nbsp;</p>

                <h3>Reporting non-accessible content</h3>

                <p>If a user feels that accessibility requirements have not been met, they can report the issue by e-mail to <a href="mailto:helsinki.palaute@hel.fi">helsinki.palaute@hel.fi</a> or through the feedback form at <a href="https://www.hel.fi/helsinki/en/administration/participate/feedback">https://www.hel.fi/helsinki/en/administration/participate/feedback</a> .</p>

                <h3>Requesting information in an accessible format</h3>

                <p>If a user feels that content on a website is not available in an accessible format, they can request for this information by e-mail at <a href="mailto:helsinki.palaute@hel.fi">helsinki.palaute@hel.fi</a> or through the feedback form at <a href="https://www.hel.fi/helsinki/en/administration/participate/feedback">https://www.hel.fi/helsinki/en/administration/participate/feedback</a> . The aim is to reply to the enquiry within a reasonable time frame.</p>

                <h2>Legal protection of accessibility,<br />
                Enforcement procedure</h2>

                <p>If a user feels that their report or enquiry has not received a response or that the response is unsatisfactory, they can report the issue to the Regional State Administrative Agency of Southern Finland. The website of the Regional State Administrative Agency of Southern Finland explains in detail how the matter will be processed.</p>

                <p>Regional State Administrative Agency of Southern Finland<br />
                Accessibility monitoring unit<br />
                <a href="http://www.saavutettavuusvaatimukset.fi">www.saavutettavuusvaatimukset.fi</a> (in Finnish)<br />
                <a href="mailto:saavutettavuus@avi.fi">saavutettavuus@avi.fi</a><br />
                Telephone exchange +358 295 016&nbsp;000<br />
                Open: Mon-Fri at 8:00&ndash;16:15</p>

                <h2>The City of Helsinki and accessibility</h2>

                <p>The objective of the city of Helsinki is to be an accessible city to all. Helsinki aims to ensure that all residents are able to move about and act as effortlessly as possible and that all content and services are accessible to all.</p>

                <p>The city promotes accessibility of digital services by streamlining publishing work and organising accessibility-related training for its staff.</p>

                <p>The accessibility level of websites is monitored constantly during their maintenance. Immediate action will be taken if deficiencies are found. The aim is to carry out the necessary amendments as quickly as possible.</p>

                <h3>The disabled and users of assistive technologies</h3>

                <p>The city provides counselling and support for the disabled and users of assistive technologies. Support is available on guidance sites announced on the city&rsquo;s website and through telephone counselling.</p>

                <h2>Approval of the accessibility statement</h2>

                <p>This statement was approved by 4/9/2020</p>

                <p>Culture and Leisure Division<br />
                City of Helsinki</p>
                """,
            },
        ],
    },
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Collection.objects.filter(show_in_landing_page=True).count() == 0:
            self.stdout.write("Initializing first Collection and Record")
            admin = User.objects.filter(is_superuser=True).first()

            collection = Collection.objects.create(
                owner=admin,
                title="Oletuskokoelma",
                description="",
                is_public=True,
                is_featured=True,
                show_in_landing_page=True,
            )
            collection.save()

            record = Record.objects.create(
                creator=admin,
                collection=collection,
                record_id="hkm.HKMS000005:000000eg",
            )
            record.save()

            self.stdout.write(
                self.style.SUCCESS("Initializing first Collection and Record - Done")
            )

        self.stdout.write("Initializing page contents (if necessary)")

        for page in pages:
            if PageContent.objects.filter(identifier=page["identifier"]).count() == 0:
                page_content = PageContent.objects.create(
                    name=page["name"], identifier=page["identifier"]
                )
                for text in page["texts"]:
                    page_content.set_current_language(text["language"])
                    page_content.title = text["title"]
                    page_content.content = text["content"]
                    page_content.save()

        self.stdout.write(
            self.style.SUCCESS("Initializing page contents (if necessary) - Done")
        )

        self.stdout.write("Initializing print products (if necessary)")

        if PrintProduct.objects.count() == 0:
            self.stdout.write("Initializing first print product")
            print_product = PrintProduct.objects.create(
                name=PrintProduct.PRODUCT_LAYOUTS_LIST[0][0],
                width="12",
                height="21",
                paper_quality="Great",
                is_museum_only=False,
            )
            print_product.save()

            self.stdout.write(
                self.style.SUCCESS("Initializing first print product - Done")
            )

        self.stdout.write(
            self.style.SUCCESS("Initializing print products (if necessary) - Done")
        )

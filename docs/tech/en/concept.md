# Technisches Konzept UsabILIty Hub

## Abstract

Die Idee des UsabILIty Hub ist es Metainformation automatisch übers Web zu empfangen.
So wie wir jetzt Modelle durch die Anbindung der ilimodels.xml von http://models.interlis.ch und mit ihrer ilisite.xml viele andere Repositories erhalten können, können wir diese Metadaten mit der Datei ilidata.xml auf dem UsabILIty Hub (derzeit models.opengis.ch) erhalten.

Einstellungen für ili2db-, QGIS Model Baker- und andere Tools werden in einer Metakonfigurationsdatei (INI-Datei) konfiguriert, ebenso wie Links (Ids) zu Katalogen, Dateien, die Informationen zur Layer-Reihenfolge und Gruppierung enthalten, sowie ein Mapping von Layernamen zu Dateien, die Stil- und Attribut-Form-Konfigurationen enthalten.
Diese Metakonfigurationsdateien können zBs. vom QGIS Model Baker entsprechend dem gewählten Modell gefunden werden (indem ilidata.xml gescannt wird).

## Generelle Informationen:


## Workflows:

### Wie erhält man anhand eines Modelnamens die benötigte Metainformation
a. Anhand eines Modelnamens werden im ilidata.xml Pfade zu Metakonfigurationsfiles gefunden.
b. Diese Metakonfigurationsfiles enthalten IDs. Andhand von diesen IDs werden im ilidata.xml Pfade zu Toppingfiles gefunden.


### Ablauf am Beispiel von QGIS Model Baker
1. User gibt Modellname in der Maske ein
2. Das ilidata.xml wird nach Links zu Metakonfigurationsfile geparsed
3. User wählt ein Metakonfigurationsfile aus, dieses wird heruntergeladen
4. Die Konfigurationen werden aus dem Metakonfigurationsfile gelesen
5. Die Links zu den Toppingfiles werden aus dem Metakonfigurationsfile gelesen
6. Die Informationen werden aus den Toppingfiles gelesen

## Das ilidata.xml
Ein *ilidata.xml* dient als Index für alle benötigten Metainformationen. Das File basiert auf dem Model [`DatasetIdx16`](http://models.interlis.ch/core/DatasetIdx16.ili). 

Es enthält Elemente `DatasetMetadata`. Darin wird auf Files referenziert, die auf demselben Server/Repo liegen, wie das *ilidata.xml*. Es gibt verschiedene Server/Repos die über das `ilisites.xml` verbunden werden können. Die `DatasetMetadata` werden anhand einer Systemübergreifenden id identifiziert. Es ist dem Benutzer überlassen, wie diese Id lautet.

### Beispiel `DatasetMetadata`
```
<DatasetIdx16.DataIndex.DatasetMetadata TID="be6623c1-aa64-4a07-931e-fc4f0745f025">
  <id>ch.opengis.ili.config.KbS_LV95_V1_4_config_V1_0</id>
  <version>2021-01-06</version>
  <owner>mailto:david@opengis.ch</owner>
  <title>
    <DatasetIdx16.MultilingualMText>
      <LocalisedText>
        <DatasetIdx16.LocalisedMText>
          <Language>de</Language>
          <Text>Einfaches Styling und Tree (OPENGIS.ch)</Text>
        </DatasetIdx16.LocalisedMText>
      </LocalisedText>
    </DatasetIdx16.MultilingualMText>
  </title>
  <categories>
    <DatasetIdx16.Code_>
      <!--  dieser Eintrag betrifft das Modell KbS_LV95_V1_4  -->
    	<value>http://codes.interlis.ch/model/KbS_LV95_V1_4</value>
      <!--  Konvention: http://codes.interlis.ch/model/{MODELNAME}  -->
    </DatasetIdx16.Code_>
    <DatasetIdx16.Code_>
      <!--  dieser Eintrag betrifft eine Meta-Config  -->
    	<value>http://codes.interlis.ch/type/metaconfig</value>
      <!--  fix Wert fuer Metaconfigs  -->
    </DatasetIdx16.Code_>
    <DatasetIdx16.Code_>
      <!--  Codes können auch generisch sein  -->
    	<value>http://codes.opengis.ch/modelbaker</value>
      <!--  müssen aber eine URL sein  -->
    </DatasetIdx16.Code_>
  </categories>
  <files>
    <DatasetIdx16.DataFile>
      <fileFormat>text/plain;version=2.3</fileFormat>
      <file>
        <DatasetIdx16.File>
          <path>metaconfig/opengisch_KbS_LV95_V1_4.ini</path>
          <!--  realtiver Pfad (zu ilidata.xml) der Metaconfig Datei  -->
        </DatasetIdx16.File>
      </file>
    </DatasetIdx16.DataFile>
  </files>
</DatasetIdx16.DataIndex.DatasetMetadata>
```

### Filterung
Das Element `categories` in den `DatasetMetadata` Elementen enthält eine Liste von `Code_` Elementen. Diese können zu deren Filterung dienen. Im Zusammenhang mit dem UsabILIty Hub werden folgende zwei Kategorien verwenden.

#### Model
The model category is identified by the prefix http://codes.interlis.ch/model/ and contains the modelname.
```
<DatasetIdx16.Code_>
  <value>http://codes.interlis.ch/model/KbS_LV95_V1_4</value>
</DatasetIdx16.Code_>
```

#### Type
The types category is identified by the prefix http://codes.interlis.ch/type/ and contains a type identificator.
```
<DatasetIdx16.Code_>
  <value>http://codes.interlis.ch/type/metaconfig</value>
</DatasetIdx16.Code_>
```

Types used by the UsabILIty Hub implementation are:
- metaconfig
- layertree
- qml
- toml
- catalogue

#### Generic
But the content of `Code_` is not stictly defined and as long as it fits the constraint of being an URI it can contain whatever the tool requires. 

> QGIS Model Baker currently does not use any generic category information 


## Das ilisites.xml
The *ilisites.xml* bases on a Model `IliSite09`. It contains Elements `SiteMetadata` where URLs are defined to other repositories (containing an *ilimodel.xml* file or - as well - an *ilidata.xml*). 
In this way, models can be found across repositories. And as well Metaconfiguration- and Toppingfiles.

### Example of an `IliSite09` element
```
<IliSite09.SiteMetadata.Site TID="1">
  <Name>usability.opengis.ch</Name>
  <Title>Allgemeine metadaten für ili-modelle</Title>
  <shortDescription>Weitere Sites des UsabILItyHubs</shortDescription>
  <Owner>http://usabilityhub.opengis.ch</Owner>
  <technicalContact>mailto:david@opengis.ch</technicalContact>
  <subsidiarySite>
    <IliSite09.RepositoryLocation_>
      <value>https://gitlab.com/signedav/usabilitydave/-/raw/master/www/</value>
    </IliSite09.RepositoryLocation_>
  </subsidiarySite>
</IliSite09.SiteMetadata.Site>
```

### Treestructure

While the tree structure of finding models accross repositories looks like this:
```
models.interlis.ch
  models.interlis.ch/ilimodels.xml -> die models werden geparst
  models.interlis.ch/ilisites.xml -> wird gesucht nach mehreren sites
    models.geo.admin.ch
    	models.geo.admin.ch/ilimodels.xml -> die models werden geparst
		models.geo.admin.ch/ilisites.xml -> wird gesucht nach mehreren sites
    		child site1 
			child site2
			child site3
    models.kkgeo.ch
		models.kkgeo.ch/ilimodels.xml -> die models werden geparst
		models.kkgeo.ch/ilisites.xml -> wird gesucht nach mehreren sites
			kanton 1 site
				kanton 1 models
				kanton 1 ilisites mit noch mehr childs...
			kanton 2 site
```

It's the same for UsabILIty Hub related files like metaconfiguration- and toppingfiles:
```
usabilithub.opengis.ch
  models.opengis.ch/ilidata.xml -> die metaconfigs (oder toppings) werden geparst 
  models.opengis.ch/ilisites.xml -> wird gesucht nach mehreren sites
    models.geo.admin.ch
    	models.geo.admin.ch/ilidata.xml -> die metaconfiguration- und toppingfiles werden geparsed
		models.geo.admin.ch/ilisites.xml -> wird gesucht nach mehreren sites
    another_child.site.ch
    	another_child.site.ch/ilidata.xml -> die metaconfigs (oder toppings) werden gepars
		another_child.site.ch/ilisite.xml -> wird gesucht nach mehreren sites
    		childchild1
			childchild2 
			etc.
	child site 2
	usw
```

## The Metaconfigurationfile (INI)

Ein *Metakonfigurationsfile* ist eine INI-Datei, die Konfigurationen für ein oder mehrere Tools enthält. Dort kann auf Files (*Toppingfiles*, *Kataloge* und andere) referenziert werden.

> Die Tools können die *Metakonfiguration* unterschiedlich handhaben. Dem *ili2db* wird beispielsweise das *Metakonfigurationsfile* übergeben. Dort ist in der *Metakonfiguration* dann auch das Modell definert. 
> Im *QGIS Model Baker* hingegen startet man mit dem Modell: Wenn ein Modell importiert wird, soll auf allen relevanten Servern/Repos nach relevanten *Metakonfigurationsfiles* gesucht werden. Die benötigten `DatasetMetadata` Elemente werden anhand ihres Child-Elements `categories` mit dem Modell-Namen identifiziert (siehe "Das ilidata.xml"). Ausserdem filtert er nach *Metakonfigurationen* andhand der Kategoriecodes für den Filetyp. Wenn mehrere *Metakonfigurationsfiles* gefunden werden, kann der User entscheiden, welches sie verwenden möchte.

### Tool Prefix
Im *Metakonfigurationsfile* können Einträge mit einem Tool-Prefix markiert werden. *ili2db* zum Beispiel verwendet den Prefix `ch.ehi.ili2db` und *QGIS Model Baker* den Prefix `qgis.modelbaker`. Dennoch ist dem Tool überlassen, welche Konfigurationen es verwended. Den Prefix `ch.interlis` der mit `ch.interlis.referenceData` zum Beispiel für die Referenz auf *Kataloge* verwendet wird, lesen zBs. *ili2db* wie auch *QGIS Model Baker*.

### File references
Die Files (*Toppingfiles*, *Kataloge*, etc.) werden entweder anhand der Systemübergreifenden DatasetMetadata-Id referenziert oder sie können einen statischen Filepfad enthalten.

#### Dataset Ids
Wenn ein File über eine DatasetMetadata-Id referenziert wird, heisst das dass die `ilidata.xml` systemübergreifend geparsed werden, um das verlinkte File zu finden. Das bedeuted, dass die *Metakonfiguration* nicht nur auf Files auf demselben Repository/Server referenzieren kann. Prefix für DatasetMetadata-Ids ist `ilidata:` Es wird grunsätzlich Empfohlen, die DatasetMetadata-Id für eine Referenz auf ein File zu verwenden (anstelle vom statischen Filepfad). 

#### Filepfad
Statische Filepfad-Links die mit `file:` referenziert werden, können sowol absolut sein, wie auch relativ. Es kann aber vom verwendeten Tool abhängig sein, zu was der Pfad relativ ist. Deshalb sollte das nur zu Testzwecke verwendet werden.

> Der *QGIS Model Baker* behandelt relative Pfade, relativ zu sich selbst. *ili2db* hingegen relativ zum Verzeichnis wo *ili2db* gestartet wurde. Also ist hierbei Vorsicht geboten.

```
[CONFIGURATION]
baseConfig=ilidata:remoteBaseConfigBasketId;ilidata:otherRemoteBaseConfigBasketId;path/otherBaseConfigLocalFile
org.interlis2.validator.config=ilidata:ilivalidatorConfigBasketId
qgis.modelbaker.layertree=ilidata:ch.opengis.config.KbS_LV95_V1_4_layertree
ch.interlis.referenceData=ilidata:ch.opengis.config.KbS_Codetexte_V1_4

[ch.ehi.ili2db]
defaultSrsCode = 2056
smart2Inheritance = true
strokeArcs = false
importTid = true
createTidCol = false
models = KbS_Basis_V1_4
preScript=ilidata:ch.opengis.config.KbS_LV95_V1_4_prescript
iliMetaAttrs=ilidata:ch.opengis.config.KbS_LV95_V1_4_toml

[qgis.modelbaker.ch]
"Belasteter_Standort (Geo_Lage_Polygon)"=file:toppings_in_modelbakerdir/qml/opengisch_KbS_LV95_V1_4_001_belasteterstandort_polygon.qml
"Belasteter_Standort (Geo_Lage_Punkt)"=ilidata:ch.opengis.topping.opengisch_KbS_LV95_V1_4_001
ZustaendigkeitKataster=ilidata:ch.opengis.configs.KbS_LV95_V1_4_0032
```

Beispielsweise die Id `ch.opengis.configs.KbS_LV95_V1_4_layertree` referenziert auf ein `DatasetMetadata`, das eine YAML-Datei enthält, wo die Layer-Struktur definiert ist. Die Id `ch.opengis.configs.KbS_LV95_V1_4_001` zeigt auf `DatasetMetadata` Elemente, die QML Files für die Styles enthalten.

Die Section `qgis.modelbaker.qml` enthält neben der Verlinkung auch die Zuweisung von Layername zu QML-Files.

### SKIP EVT: QGIS Model Baker spezifische Settings
In dieser *Metakonfiguration* können nun verschiedene *Toppinginformationen* enthalten sein. Den *QGIS Model Baker* betreffen die Einträge mit dem Prefix `qgis.modelbaker` sowie auch einige mit `ch.ehi.ili2db`. Es kann auf weitere Files referenziert werden. Wie zum Beispiel auf Kataloge, Style-QMLs oder auch Layertree-YAMLs. 

## Toppingfiles
Toppingfiles sind Files, auf welche von der Metakonfiguration referenziert wurde und die Konfigurationsinformation des GIS Projektes enthalten. Es können also Formularkonfigurationen, Style-Attribute, Legendendarstellung und Reihenfolge, sowie auch Kataloge sein. Für jedes Tool können individuelle Toppingfiles verwendet werden. Von einem einfachen Zip-File, welches das gesamte Projekt enthält, bis zu einem sorgfältigen Mapping von Layernamen zu QML-Style-Files.

### Beispiel eines YAML Files für die Layerstruktur in QGIS
```
legend:
  - 'top-group':
      group: true
      checked: true
      expanded: true
      mutually-exclusive: true
      mutually-exclusive-child: -1
      child-nodes:
        - 'geom punkt':
            group: false
            checked: true
        - 'geom polygon':
            group: false
            checked: true
        - 'subgroup':
            group: true
            child-nodes:
              - 'subsubgroup':
                  group: true
                  checked: true
                  child-nodes:
                    - 'baum':
                        group: false
                        checked: true
                    - 'subsubsubgroup':
                        group: true
                        checked: true
                        child-nodes:
                          - 'another layer':
                              group: false
                              visbile: false
                    - 'layer in the subgroup':
                        group: false
                        visbile: false
layer-order:
  - 'geom punkt'
  - 'geom polygon'
```

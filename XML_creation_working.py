import xml.etree.cElementTree as ET
import uuid
import datetime
import os
import re
from tkinter.filedialog import askdirectory



print(datetime.datetime.utcnow().isoformat())




# Demande du dossier pour création des fichiers PKL, etc...
directory = askdirectory()

#extraction du nom du dossier
dir_name = (re.search('([^\/]+$)', directory).group(0))

# génération d'UUID
u = uuid

# array des medias trouvés
listed_files = []

# fonction de listage du dossier IMP
def list_files(path):
    for fileName in os.listdir(path):
        filePath = path+'/'+fileName
        if (os.access(filePath, os.F_OK) and fileName[-3:] == 'mxf' or fileName[:3] == 'CPL'):
        	fileSize = os.popen("C:/code/MediaInfo/MediaInfo.exe --Inform=General;%FileSize% " +filePath).read() # http://manpages.ubuntu.com/manpages/precise/man1/mediainfo.1.html
        	fileDuration = os.popen("C:/code/MediaInfo/MediaInfo.exe --Inform=General;%Duration% " +filePath).read()
        	fileHash = os.popen("openssl sha1 -binary "+ filePath + " | openssl base64").read()
        	# print(fileName+" -> "+re.sub("\n", "", fileSize)+" size")
        	# print(fileSize, fileDuration, fileHash)
        	temp_obj = {}
        	temp_obj['title'] = fileName
        	temp_obj['size'] = re.sub("\n", "", fileSize)
        	temp_obj['hash'] = fileHash
        	if fileName[-3:] == 'mxf':
        		temp_obj['type'] = "application/mxf"
        	else:
        		temp_obj['type'] = "text/xml"
        	listed_files.append(temp_obj)
        

list_files(directory)

# l'array des medias du dossier passé en argument
# print(listed_files)
 

################################################################
#                  création du PKL                             #
################################################################

# definiion de la balise principale
PKL_root = ET.Element("PackingList", xmlns="http://www.smpte-ra.org/schemas/429-8/2007/PKL")

# definiion de la balise secondaire incluse dans root
Id = ET.SubElement(PKL_root, "Id").text = "urn:uuid:"+str(u.uuid1())
AnnotationText = ET.SubElement(PKL_root, "AnnotationText").text = dir_name
IssueDate = ET.SubElement(PKL_root, "IssueDate").text = str(datetime.datetime.now().isoformat())
Issuer = ET.SubElement(PKL_root, "Issuer").text = "Videomenthe"
Creator = ET.SubElement(PKL_root, "Creator").text = "Fabien Lenoir"
AssetList = ET.SubElement(PKL_root, "AssetList")

# definition des balises Asset
index = 0
for item in listed_files:
	Asset = ET.SubElement(AssetList, "Asset")
	ET.SubElement(Asset, "Id").text = "urn:uuid:"+str(u.uuid1())
	ET.SubElement(Asset, "AnnotationText").text = listed_files[index]['title']
	ET.SubElement(Asset, "Hash").text = listed_files[index]['hash']
	ET.SubElement(Asset, "Size").text = listed_files[index]['size']
	ET.SubElement(Asset, "Type").text = listed_files[index]['type']
	ET.SubElement(Asset, "OriginalFileName").text = listed_files[index]['title']
	index+=1

PKL_tree = ET.ElementTree(PKL_root)
PKL_tree.write("PKL_"+str(u.uuid1())+".xml")
print("The PKL is created !")

# on imprime le fichier xml généré
# print(ET.tostring(root))

# il reste à voir si on recupère l'umid des fichiers video MXF pour les utiliser en uuid

################################################################
#                  création du CPL                            #
################################################################

# definiion de la balise principale
CPL_ROOT = ET.Element("CompositionPlaylist", {'xmlns':'http://www.smpte-ra.org/schemas/2067-3/2013','xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance'})

# definiion de la balise secondaire incluse dans root
Id = ET.SubElement(CPL_ROOT, "Id").text = "urn:uuid:"+str(u.uuid1())
AnnotationText = ET.SubElement(CPL_ROOT, "Annotation").text = dir_name
IssueDate = ET.SubElement(CPL_ROOT, "IssueDate").text = str(datetime.datetime.now().isoformat())
Issuer = ET.SubElement(CPL_ROOT, "Issuer").text = "Videomenthe"
Creator = ET.SubElement(CPL_ROOT, "Creator").text = "Fabien Lenoir"
ContentOriginator = ET.SubElement(CPL_ROOT, "ContentOriginator").text = "Videomenthe"
ContentTitle = ET.SubElement(CPL_ROOT, "ContentTitle").text = dir_name
ContentKind = ET.SubElement(CPL_ROOT, "ContentKind").text = "short"
ContentVersionList = ET.SubElement(CPL_ROOT, "ContentVersionList")

ContentVersion = ET.SubElement(ContentVersionList, "ContentVersion")
ET.SubElement(ContentVersion, "Id").text = "urn:uuid:"+str(u.uuid1())
ET.SubElement(ContentVersion, "LabelText").text = dir_name

CompositionTimecode = ET.SubElement(CPL_ROOT, "CompositionTimecode")
ET.SubElement(CompositionTimecode, "TimecodeDropFrame").text = "0"
ET.SubElement(CompositionTimecode, "TimecodeRate").text = "60"
ET.SubElement(CompositionTimecode, "TimecodeStartAddress").text = "00:00:00:00"

EditRate = ET.SubElement(CPL_ROOT, "EditRate").text = "6000"

LocaleList = ET.SubElement(CPL_ROOT, "localeList")
ET.SubElement(LocaleList, "LanguageList").text = "a completer"
ET.SubElement(LocaleList, "RegionList").text = "a completer"
ET.SubElement(LocaleList, "ContentMaturityRatingList").text = "a completer"

ExtensionProperties = ET.SubElement(CPL_ROOT, "ExtensionProperties")
SegmentList = ET.SubElement(CPL_ROOT, "SegmentList")



CPL_tree = ET.ElementTree(CPL_ROOT)
CPL_tree.write("CPL_"+str(u.uuid1())+".xml")
print("The CPL is created !")



################################################################
#                  création de l'Asset Map                     #
################################################################
# il faut que ce soit le dernier a être généré afin d'avoir les CPL, OPL et PKL avant

ASSETMAP_root = ET.Element("AssetMap", xmlns="http://www.smpte-ra.org/schemas/429-8/2007/AM")

# definiion de la balise secondaire incluse dans root
Id = ET.SubElement(ASSETMAP_root, "Id").text = "urn:uuid:"+str(u.uuid1())
Creator = ET.SubElement(ASSETMAP_root, "Creator").text = "Fabien Lenoir"
VolumeCount = ET.SubElement(ASSETMAP_root, "VolumeCount").text = "1"
IssueDate = ET.SubElement(ASSETMAP_root, "IssueDate").text = str(datetime.datetime.now().isoformat())
Issuer = ET.SubElement(ASSETMAP_root, "Issuer").text = "Videomenthe"

AssetList = ET.SubElement(ASSETMAP_root, "AssetList")

# definition des balises Asset
for item in listed_files:
	Asset = ET.SubElement(AssetList, "Asset")
	ET.SubElement(Asset, "Id").text = "urn:uuid:"+str(u.uuid1())
	ET.SubElement(Asset, "PackingList").text = "true"
	ET.SubElement(Asset, "ChunkList").text = "rien pour l'insant"
		
ASSETMAP_tree = ET.ElementTree(ASSETMAP_root)
ASSETMAP_tree.write("ASSETMAP.xml")
print("The ASSETMAP is created !")
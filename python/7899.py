import base64
import json
import urllib.parse

def modify_proxies():
    with open('ws_tls/proxies/wstls', 'r') as f:
        proxies = f.readlines()

    modified_proxies = []
    for proxy in proxies:
        proxy = proxy.strip()
        if proxy.startswith('vmess://'):
            base64_str = proxy.split('vmess://')[1]
            proxy_info = base64.b64decode(base64_str).decode('utf-8')
            proxy_dict = json.loads(proxy_info)

            proxy_dict['add'] = '127.0.0.1'
            proxy_dict['port'] = '7899'

            modified_proxy = 'vmess://' + base64.b64encode(json.dumps(proxy_dict).encode('utf-8')).decode('utf-8')
            modified_proxies.append(modified_proxy)
        elif proxy.startswith('vless://'):
            proxy_info = proxy.split('vless://')[1]
            proxy_info = urllib.parse.unquote(proxy_info)
        
            uuid, rest = proxy_info.split('@', 1)  # Split at the first occurrence of '@'
            ip_port, rest = rest.split('?', 1)  # Split at the first occurrence of '?'
            modified_proxy = 'vless://' + uuid + '@127.0.0.1:7899?' + rest
            modified_proxies.append(modified_proxy)


    with open('ws_tls/7899/7899', 'w') as f:
        for proxy in modified_proxies:
            f.write(proxy + '\n')

if __name__ == '__main__':
    modify_proxies()

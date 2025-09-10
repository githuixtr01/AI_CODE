"""
Threat intelligence enrichment for scan results using public APIs.
"""
import requests

THREAT_API_ENDPOINTS = {
    'shodan': 'https://api.shodan.io/shodan/host/{ip}?key={api_key}',
    'virustotal': 'https://www.virustotal.com/api/v3/ip_addresses/{ip}',
    'abuseipdb': 'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}',
}

def enrich_with_threat_intel(ip, apis: dict) -> dict:
    """
    ip: IP address to enrich
    apis: dict with keys 'shodan', 'virustotal', 'abuseipdb' and their API keys
    Returns: dict with enrichment data
    """
    results = {}
    # Shodan
    if 'shodan' in apis and apis['shodan']:
        try:
            url = THREAT_API_ENDPOINTS['shodan'].format(ip=ip, api_key=apis['shodan'])
            resp = requests.get(url, timeout=10)
            if resp.ok:
                results['shodan'] = resp.json()
        except Exception as e:
            results['shodan_error'] = str(e)
    # VirusTotal
    if 'virustotal' in apis and apis['virustotal']:
        try:
            url = THREAT_API_ENDPOINTS['virustotal'].format(ip=ip)
            headers = {"x-apikey": apis['virustotal']}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.ok:
                results['virustotal'] = resp.json()
        except Exception as e:
            results['virustotal_error'] = str(e)
    # AbuseIPDB
    if 'abuseipdb' in apis and apis['abuseipdb']:
        try:
            url = THREAT_API_ENDPOINTS['abuseipdb'].format(ip=ip)
            headers = {"Key": apis['abuseipdb'], "Accept": "application/json"}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.ok:
                results['abuseipdb'] = resp.json()
        except Exception as e:
            results['abuseipdb_error'] = str(e)
    return results

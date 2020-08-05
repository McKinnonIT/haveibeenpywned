from haveibeenpywned import Pywned

pywned = Pywned()
pywned.api_key = "your_hibp_api_key"
pywned.get_all_breaches_for_account("your@email.com")

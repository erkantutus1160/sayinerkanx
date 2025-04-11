import requests

def check_security_headers(url):
    print("[*] HTTP Güvenlik Başlıkları Kontrol Ediliyor...")
    headers = requests.get(url).headers
    results = {}
    security_headers = [
        "X-Frame-Options",
        "X-XSS-Protection",
        "X-Content-Type-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "Referrer-Policy"
    ]
    for h in security_headers:
        results[h] = "✅ Var" if h in headers else "❌ Yok"
    return results


def test_xss(url):
    print("[*] XSS testi yapılıyor...")
    payload = "<script>alert('XSS')</script>"
    test_url = f"{url}?q={payload}"
    response = requests.get(test_url)
    if payload in response.text:
        return "❌ XSS Zafiyeti Tespit Edildi!"
    return "✅ XSS Zafiyeti Bulunamadı."


def test_sqli(url):
    print("[*] SQLi testi yapılıyor...")
    payload = "' OR '1'='1"
    test_url = f"{url}?id={payload}"
    response = requests.get(test_url)
    if "SQL" in response.text or "mysql" in response.text.lower():
        return "❌ SQL Injection Zafiyeti Tespit Edildi!"
    return "✅ SQL Injection Zafiyeti Bulunamadı."


def scan(url):
    results = {}
    results["headers"] = check_security_headers(url)
    results["xss"] = test_xss(url)
    results["sqli"] = test_sqli(url)
    return results

if __name__ == "__main__":
    target = input("Hedef URL: ")
    report = scan(target)
    print("\n--- TARAMA SONUCU ---")
    for section, result in report.items():
        print(f"\n{section.upper()}:")
        if isinstance(result, dict):
            for k, v in result.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {result}")
